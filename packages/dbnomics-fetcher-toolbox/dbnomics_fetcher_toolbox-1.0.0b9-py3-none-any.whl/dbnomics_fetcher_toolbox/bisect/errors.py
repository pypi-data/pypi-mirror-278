from pathlib import Path
from typing import TYPE_CHECKING, Any

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.controller import BisectionController
    from dbnomics_fetcher_toolbox.bisect.partitions.types import BisectionPartition


class BisectionError(FetcherToolboxError):
    pass


class BisectionControllerError(FetcherToolboxError):
    def __init__(self, *, controller: "BisectionController[Any, Any]", msg: str) -> None:
        super().__init__(msg=msg)
        self.controller = controller


class StateFileError(BisectionControllerError):
    def __init__(self, *, controller: "BisectionController[Any, Any]", msg: str, state_file: Path) -> None:
        super().__init__(controller=controller, msg=msg)
        self.state_file = state_file


class LoadStateFileError(StateFileError):
    def __init__(self, *, controller: "BisectionController[Any, Any]", state_file: Path) -> None:
        msg = f"Could not load state file: {state_file}"
        super().__init__(controller=controller, msg=msg, state_file=state_file)


class SaveStateFileError(StateFileError):
    def __init__(self, *, controller: "BisectionController[Any, Any]", state_file: Path) -> None:
        msg = f"Could not save state file: {state_file}"
        super().__init__(controller=controller, msg=msg, state_file=state_file)


class PartitionBisectionError(BisectionError):
    def __init__(self, *, msg: str, partition: "BisectionPartition") -> None:
        super().__init__(msg=msg)
        self.partition = partition


class NoMoreBisectionError(PartitionBisectionError):
    def __init__(self, *, partition: "BisectionPartition") -> None:
        msg = f"Partition {partition.id!r} can't be bisected anymore"
        super().__init__(msg=msg, partition=partition)
