from typing import Protocol, Self, TypeAlias

__all__ = ["BisectionPartition", "PartitionId"]


PartitionId: TypeAlias = str


class BisectionPartition(Protocol):
    def bisect(self) -> tuple[Self, Self]: ...

    @property
    def depth(self) -> int: ...

    @property
    def id(self) -> PartitionId: ...

    @property
    def should_bisect_before_process(self) -> bool: ...
