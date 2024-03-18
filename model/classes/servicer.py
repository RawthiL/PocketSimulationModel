from ..types import (
    uPOKTType,
    ServicerReportCardType,
    ServicerTestScoresType,
    PublicKeyType,
    GeoZoneType,
    ServiceType,
    ServiceURLType,
    BlockHeightType,
    StakeStatusType,
)
from typing import List


class Servicer:
    id_number = 0

    def __init__(
        self,
        name: str,
        servicer_salary: uPOKTType,
        report_card: ServicerReportCardType,
        test_scores: ServicerTestScoresType,
        pokt_holdings: uPOKTType,
        staked_pokt: uPOKTType,
        service_url: ServiceURLType,
        services: List[ServiceType],
        geo_zone: GeoZoneType,
        operator_public_key: PublicKeyType,
        pause_height: BlockHeightType,
        stake_status: StakeStatusType,
        unstaking_height: BlockHeightType,
        QoS: float,
    ):
        self.id_number = Servicer.id_number
        Servicer.id_number += 1
        self.name = name
        self.public_key = self
        self.servicer_salary = servicer_salary
        self.report_card = report_card
        self.test_scores = test_scores
        self.pokt_holdings = pokt_holdings
        self.staked_pokt = staked_pokt
        self.service_url = service_url
        self.services = services
        self.geo_zone = geo_zone
        self.operator_public_key = operator_public_key
        self.pause_height = pause_height
        self.stake_status = stake_status
        self.unkstaking_height = unstaking_height
        self.QoS = QoS

        self.revenue_expectations = {}
        self.slashing_from_jailing_history = {}
        self.slashing_history = {}
        self.jail_lost_revenue_history = {}
        self.staked_pokt_total_inflow = staked_pokt
        self.total_revenues = 0
        self.shut_down = False

    def services_by_revenue(self):
        out = [
            (service, self.revenue_expectations[service])
            for service in self.revenue_expectations
        ]
        out = sorted(out, key=lambda x: x[1])
        return out

    def __lt__(self, other):
        self.id_number < other.id_number
