from dataclasses import dataclass, field
from typing import Dict

from services.models.base import BaseModelMixin


@dataclass
class QueueInfo:
    txin: int = 0
    txout: int = 0

    @classmethod
    def from_json(cls, j):
        return cls(
            txin=int(j['txin']),
            txout=int(j['txout']),
        )


@dataclass
class JobsInfo:
    total: int = 0
    active: int = 0
    pending: int = 0
    completed: int = 0
    eth_tx: int = 0
    bnb_tx: int = 0
    eth_rune: int = 0
    bnb_rune: int = 0
    total_rune: int = 0

    @classmethod
    def from_json(cls, j):
        return cls(
            total=int(j['total']),
            active=int(j['active']),
            pending=int(j['pending']),
            eth_tx=int(j['eth_tx']),
            bnb_tx=int(j['bnb_tx']),
            eth_rune=int(j['eth_rune']),
            bnb_rune=int(j['bnb_rune']),
            total_rune=int(j['total_rune']),
        )


@dataclass
class BridgeHealth(BaseModelMixin):
    status: str = ''
    health: str = ''
    bridges: Dict[str, str] = field(default_factory=dict)
    asset_min: int = 0
    asset_max: int = 0
    queue: QueueInfo = QueueInfo()
    jobs: JobsInfo = JobsInfo()
    errors: int = 0
    ignore: int = 0

    @classmethod
    def from_jsons(cls, main_json, stats_json):
        return cls(
            status=main_json['status'],
            health=main_json['health'],
            bridges=main_json['bridges'],
            asset_min=int(main_json['asset']['min']),
            asset_max=int(main_json['asset']['max']),
            queue=QueueInfo.from_json(stats_json['queue']),
            jobs=JobsInfo.from_json(stats_json['jobs']),
            errors=int(stats_json['other']['errors']),
            ignore=int(stats_json['other']['ignore']),
        )