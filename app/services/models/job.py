from dataclasses import dataclass

from services.lib.datetime import parse_iso8601_date_to_timestamp
from services.lib.money import short_address
from services.lib.texts import link
from services.models.base import BaseModelMixin

CHAIN_ETH = 'ETH'
CHAIN_BNB = 'BNB'


def eth_link(eth_addr, full=False):
    return link(f"https://etherscan.io/address/{eth_addr}",
                eth_addr if full else short_address(eth_addr))


def bnb_link(bnb_addr, full=False):
    return link(f"https://explorer.binance.org/address/{bnb_addr}",
                bnb_addr if full else short_address(bnb_addr))


@dataclass
class BridgeTxInfo:
    chain: str = ''
    block: int = 0
    amount: float = 0
    from_addr: str = ''
    to_addr: str = ''
    hash: str = ''
    time: float = 0

    @property
    def link(self):
        return eth_link(self.address) if self.chain == CHAIN_ETH else bnb_link(self.address)

    @property
    def address(self):
        return self.from_addr if self.from_addr else self.to_addr

    @classmethod
    def from_api_json(cls, j):
        return cls(
            chain=str(j['chain']),
            block=int(j['block']),
            amount=float(j['amount']),
            from_addr=str(j.get('from', '')),
            to_addr=str(j.get('to', '')),
            hash=str(j['hash']),
            time=parse_iso8601_date_to_timestamp(j['time'])
        )


@dataclass
class JobTxInfo(BaseModelMixin):
    ident: str = ''
    status: str = ''
    chain: str = ''
    in_tx_time: float = 0
    out_tx_time: float = 0
    in_tx: BridgeTxInfo = BridgeTxInfo()
    out_tx: BridgeTxInfo = BridgeTxInfo()

    STATUS_ACTIVE = 'ACTIVE'
    STATUS_PENDING = 'PENDING'
    STATUS_COMPLETED = 'COMPLETED'

    @classmethod
    def from_api_json(cls, j):
        return cls(
            ident=str(j['id']),
            status=str(j['status']).upper(),
            chain=str(j['chain']),
            in_tx_time=parse_iso8601_date_to_timestamp(str(j['events']['intx'])),
            out_tx_time=parse_iso8601_date_to_timestamp(str(j['events']['outtx'])),
            in_tx=BridgeTxInfo.from_api_json(j['in']),
            out_tx=BridgeTxInfo.from_api_json(j['out']),
        )

    @property
    def from_chain(self):
        return self.chain

    @property
    def to_chain(self):
        return CHAIN_BNB if self.from_chain == CHAIN_ETH else CHAIN_ETH
