from dataclasses import KW_ONLY, dataclass, replace
from typing import Generic, Protocol, Self, TypeVar

from dbnomics_fetcher_toolbox.bisect.errors import NoMoreBisectionError
from dbnomics_fetcher_toolbox.bisect.partitions.types import PartitionId

__all__ = ["RangeBisectionPartition"]


class RangeBisectionPartitionValue(Protocol):
    def __add__(self, increment: int) -> Self: ...

    def __sub__(self, other: Self) -> int: ...


TRangeBisectionPartitionValue = TypeVar("TRangeBisectionPartitionValue", bound=RangeBisectionPartitionValue)


@dataclass(frozen=True)
class RangeBisectionPartition(Generic[TRangeBisectionPartitionValue]):
    min_value: TRangeBisectionPartitionValue
    max_value: TRangeBisectionPartitionValue

    _: KW_ONLY
    depth: int = 0
    max_range: int | None = None

    def bisect(self) -> tuple[Self, Self]:
        if self.max_value == self.min_value:
            raise NoMoreBisectionError(partition=self)

        middle_index = self.range // 2
        middle_value = self.min_value + middle_index
        new_depth = self.depth + 1
        left_partition = replace(self, depth=new_depth, max_value=middle_value)
        right_partition = replace(self, depth=new_depth, min_value=middle_value + 1)
        return left_partition, right_partition

    @property
    def id(self) -> PartitionId:
        return f"{self.min_value}__{self.max_value}"

    @property
    def range(self) -> int:
        return self.max_value - self.min_value

    @property
    def should_bisect_before_process(self) -> bool:
        return self.max_range is not None and self.range >= self.max_range
