from abc import ABC

from services.lib.money import pretty_money, short_address, pretty_rune
from services.lib.texts import code, bold, link
from services.models.health import BridgeHealth
from services.models.job import JobTxInfo, eth_link, bnb_link, CHAIN_BNB, CHAIN_ETH


CREATOR_TG = '@account1242'


class BaseLocalization(ABC):  # == English
    STATUS_RECEIVED = 'Received 🆕'
    STATUS_SENDING = 'Sending 🔁'
    STATUS_COMPLETED = 'Completed ✅'
    STATUS_UNKNOWN = 'Unknown 🧶'

    def current_info(self, health: BridgeHealth):

        health_str = '🟢 Nominal' if health.health == health.HEALTH_NOMINAL else f'🔴 {health.health}'
        status_str = '🟢 Live' if health.status == health.STATUS_LIVE else f'🔴 {health.status}'
        return (
            f"{bold('Status:')} {status_str}\n"
            f"{bold('Health:')} {health_str}\n"
            f"\n"
            f"{bold('BNB Bridge:')} {bnb_link(health.bridges.get(CHAIN_BNB, '???'), full=True)}\n"
            f"{bold('ETH Bridge:')} {eth_link(health.bridges.get(CHAIN_ETH, '???'), full=True)}\n"
            f"\n"
            f"{bold('Queue:')} {health.queue.txin} IN → {health.queue.txout} OUT\n"
            f"{bold('Total:')} {health.jobs.total}\n"
            f"{bold('Completed:')} {health.jobs.completed}\n"
            f"{bold('Queued:')} {health.jobs.active}\n"
            f"{bold('BNB TX:')} {health.jobs.bnb_tx}\n"
            f"{bold('ETH TX:')} {health.jobs.eth_tx}\n"
            f"{bold('ETH RUNE:')} {pretty_rune(health.jobs.eth_rune)}\n"
            f"{bold('BNB RUNE:')} {pretty_rune(health.jobs.bnb_rune)}\n"
            f"{bold('Total rune:')} {pretty_rune(health.jobs.total_rune)}"
        )

    def tx_alert_text(self, tx: JobTxInfo):
        hash_str = bold(f'Hash: {tx.ident}')

        str_status = {
            tx.STATUS_COMPLETED: self.STATUS_COMPLETED,
            tx.STATUS_ACTIVE: self.STATUS_SENDING,
            tx.STATUS_PENDING: self.STATUS_RECEIVED
        }.get(tx.status, self.STATUS_UNKNOWN)

        return (
            f"{hash_str}\n"
            f"\n"
            f"{bold('Direction:')} {tx.from_chain} → {tx.to_chain}\n"
            f"{bold('Amount:')} {pretty_money(tx.in_tx.amount)} RUNE\n"
            f"{bold('From:')} {tx.in_tx.link}\n",
            f"{bold('To:')} {tx.out_tx.link}\n"
            f"\n"
            f"{bold(str_status)}",
        )

    @staticmethod
    def error_message(exc, tag):
        # fixme: use CREATOR_TG from the config
        return code(f"Sorry! An error occurred: {str(exc)}. Incident ID is {tag}.") + \
               f"\nFeedback/support: {CREATOR_TG}."
