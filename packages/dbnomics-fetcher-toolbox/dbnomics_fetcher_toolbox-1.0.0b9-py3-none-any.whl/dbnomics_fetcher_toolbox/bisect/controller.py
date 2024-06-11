import collections
from abc import ABC, abstractmethod
from dataclasses import replace
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

import daiquiri
import typedload.exceptions
from contexttimer import Timer
from dbnomics_data_model.json_utils import load_json_file, save_json_file
from dbnomics_data_model.json_utils.dumping import dump_as_json_data
from humanfriendly.text import pluralize

from dbnomics_fetcher_toolbox._internal.file_utils import format_file_path_with_size
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_timer
from dbnomics_fetcher_toolbox._internal.json_utils import loader
from dbnomics_fetcher_toolbox.bisect.errors import LoadStateFileError, SaveStateFileError
from dbnomics_fetcher_toolbox.bisect.model import BisectionControllerState
from dbnomics_fetcher_toolbox.bisect.partitions.types import BisectionPartition
from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.sources.json.msgspec import MsgspecJsonSource
from dbnomics_fetcher_toolbox.types import ResourceFullId, ResourceId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.group_downloader import GroupDownloader

__all__ = ["BisectionController"]


logger = daiquiri.getLogger(__name__)

T = TypeVar("T")
TBisectionPartition = TypeVar("TBisectionPartition", bound=BisectionPartition)


class BisectionController(ABC, Generic[T, TBisectionPartition]):
    def __init__(self, *, group_downloader: "GroupDownloader", root_partition: TBisectionPartition) -> None:
        downloader = group_downloader._downloader  # noqa: SLF001
        self._cache_dir = downloader._cache_dir  # noqa: SLF001
        self._fail_fast = downloader._fail_fast  # noqa: SLF001
        self._group_downloader = group_downloader
        self._report = group_downloader._downloader._report  # noqa: SLF001
        self._resume_mode = downloader._resume_mode  # noqa: SLF001
        self._root_partition = root_partition
        self._state_dir = downloader._state_dir / "bisection-controller"  # noqa: SLF001
        self._target_dir = downloader._target_dir  # noqa: SLF001

        self.process_resource = self._group_downloader.process_resource

        previous_state = self._load_previous_state()
        self._bisected_resource_full_ids = [] if previous_state is None else previous_state.bisected_resource_full_ids
        self._deque: collections.deque[TBisectionPartition] = collections.deque([root_partition])
        self._loaded_values: list[T] = []

    def start(self) -> None:
        logger.debug("Starting bisection process...")

        with Timer() as timer:
            partition_index = 0
            while self._deque:
                partition = self._deque.popleft()
                self._process_partition(partition, index=partition_index)
                partition_index += 1

            if len(self._loaded_values) > 1:
                logger.debug("Merging %d loaded values from partitions to a single file...", len(self._loaded_values))
                resource = self._create_partition_resource(partition=None)
                # Update resource ID to avoid considering it as a duplicate of the root partition resource.
                new_resource_id = ResourceId.parse(f"{resource.id}__merged")
                resource = replace(resource, id=new_resource_id)
                merged_values = reduce(self._merge_loaded_values, self._loaded_values)
                self._group_downloader.process_resource(resource, source=MsgspecJsonSource(merged_values))

        logger.debug(
            "End of bisection process: %s processed",
            pluralize(partition_index, "partition was", "partitions were"),
            duration=format_timer(timer),
        )

    def _bisect(self, partition: TBisectionPartition, *, index: int) -> None:
        left_partition, right_partition = partition.bisect()
        logger.debug(
            "Partition #%d %r has been bisected in 2 sub-partitions: %r and %r",
            index,
            partition.id,
            left_partition.id,
            right_partition.id,
            depth=partition.depth,
        )
        self._deque.extendleft([right_partition, left_partition])

    @abstractmethod
    def _create_partition_resource(self, *, partition: TBisectionPartition | None) -> Resource[T]: ...

    def _load_previous_state(self) -> BisectionControllerState | None:
        if not self._resume_mode:
            return None

        state_file = self._state_file
        if not state_file.is_file():
            return None

        try:
            state_json_data = load_json_file(state_file)
        except Exception as exc:
            raise LoadStateFileError(controller=self, state_file=state_file) from exc

        try:
            return loader.load(state_json_data, type_=BisectionControllerState)
        except typedload.exceptions.TypedloadException as exc:
            raise LoadStateFileError(controller=self, state_file=state_file) from exc

    @abstractmethod
    def _merge_loaded_values(self, accumulator: T, value: T) -> T: ...

    def _process_partition(self, partition: TBisectionPartition, *, index: int) -> None:
        resource = self._create_partition_resource(partition=partition)
        resource_full_id = ResourceFullId(self._group_downloader.group_id, resource.id)

        self._report.register_resource_start(resource_full_id)

        if self._resume_mode:
            target_file = self._target_dir / resource.file
            if target_file.is_file():
                message = f"Resume mode: reloading data of partition {str(resource_full_id)!r} from target dir: {format_file_path_with_size(target_file)}"  # noqa: E501
                logger.debug(message)
                loaded_value = resource.parser.parse_file(target_file)
                self._loaded_values.append(loaded_value)
                self._report.register_resource_skip(resource_full_id, message=message)
                return

            cache_file = self._cache_dir / resource.file
            if cache_file.is_file():
                message = f"Resume mode: reloading data of partition {str(resource_full_id)!r} from cache dir: {format_file_path_with_size(cache_file)}"  # noqa: E501
                logger.debug(message)
                with Timer() as timer:
                    loaded_value = resource.parser.parse_file(cache_file)
                self._loaded_values.append(loaded_value)
                self._report.register_resource_success(resource_full_id, output_file=cache_file, timer=timer)
                return

            if resource_full_id in self._bisected_resource_full_ids:
                message = f"Resume mode: bisecting previously bisected partition {str(resource_full_id)!r}"
                logger.debug(message)
                self._report.register_resource_skip(resource_full_id, message=message)
                self._bisect(partition, index=index)
                return

        if partition.should_bisect_before_process:
            logger.debug(
                "Bisecting partition #%d %r before processing it",
                index,
                partition.id,
                depth=partition.depth,
            )
            self._bisect(partition, index=index)
            return

        logger.debug("Starting to process partition #%d %r...", index, partition.id, depth=partition.depth)

        try:
            loaded_value = self._process_partition_resource(resource, partition=partition)
        except Exception as exc:
            if self._fail_fast:
                raise
            if self._should_bisect(exc):
                self._register_partition_resource_bisection(resource)
                self._bisect(partition, index=index)
                return
            logger.exception(
                "Resource of partition #%d %r could not be processed, aborting bisection process",
                index,
                partition.id,
                depth=partition.depth,
            )
            raise

        self._loaded_values.append(loaded_value)

        logger.debug("Partition #%d %r has been processed successfully", index, partition.id, depth=partition.depth)
        return

    @abstractmethod
    def _process_partition_resource(self, resource: Resource[T], *, partition: TBisectionPartition) -> T: ...

    def _register_partition_resource_bisection(self, resource: Resource[T]) -> None:
        resource_full_id = ResourceFullId(self._group_downloader.group_id, resource.id)
        self._bisected_resource_full_ids.append(resource_full_id)

        state = BisectionControllerState(bisected_resource_full_ids=self._bisected_resource_full_ids)
        state_json_data = dump_as_json_data(state)

        state_file = self._state_file
        state_file.parent.mkdir(exist_ok=True, parents=True)

        try:
            save_json_file(state_file, state_json_data)
        except Exception as exc:
            raise SaveStateFileError(controller=self, state_file=state_file) from exc

    @abstractmethod
    def _should_bisect(self, error: Exception) -> bool: ...

    @property
    def _state_file(self) -> Path:
        return self._state_dir / "groups" / str(self._group_downloader.group_id) / "state.json"
