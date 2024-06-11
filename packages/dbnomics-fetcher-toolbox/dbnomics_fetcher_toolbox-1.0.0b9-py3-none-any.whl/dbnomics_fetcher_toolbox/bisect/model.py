from dataclasses import dataclass

from dbnomics_fetcher_toolbox.types import ResourceFullId


@dataclass(kw_only=True)
class BisectionControllerState:
    bisected_resource_full_ids: list[ResourceFullId]
