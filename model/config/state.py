from copy import deepcopy
from model.classes import Application, DAO, Gateway, Service, Servicer, Validator
from ..types import StateType
from model.policy import service_linking_policy
from model.mechanisms import link_service_mechanism
from itertools import product
import random

# This is the number of total apps to be used in gaming tests (honest+adversary)
GAMING_APPS_TOTAL = 10
# Same but for nodes
GAMING_NODES_TOTAL = 100

config_option_map = {
    "Test": {
        "Geozones": "Test",
        "Applications": "Test",
        "DAO": "Test",
        "Gateways": "Test",
        "Services": "Test",
        "Servicers": "Test",
        "Validators": "Test",
    },
    "Base": {
        "Geozones": "Base",
        "Applications": "Base",
        "DAO": "Base",
        "Gateways": "Base",
        "Services": "Base",
        "Servicers": "Base",
        "Validators": "Base",
    },

    # Used for: ImplicitQoS
    "Game50-50": {
        "Geozones": "Test",
        "Applications": "Game50-50",
        "DAO": "Test",
        "Gateways": "Test",
        "Services": "Test",
        "Servicers": "Game50-50",
        "Validators": "Test",
    },
}


def build_state(config_option) -> StateType:
    config_option = config_option_map[config_option]
    state = {}

    state["Geozones"] = geo_zones_config[config_option["Geozones"]]
    state["Applications"] = application_config[config_option["Applications"]]
    state["DAO"] = dao_config[config_option["DAO"]]
    state["Gateways"] = gateways_config[config_option["Gateways"]]
    state["Services"] = service_config[config_option["Services"]]
    state["Servicers"] = servicers_config[config_option["Servicers"]]
    state["Validators"] = validators_config[config_option["Validators"]]
    state["height"] = 0
    state["day"] = 0
    state["Sessions"] = []
    state["total_relays"] = None
    state["processed_relays"] = None
    # state["pokt_price_true"] = 0.06 / 1e6
    state["pokt_price_oracle"] = 0.06 / 1e6
    state["n_transactions"] = None
    state["relay_log"] = None
    state["servicer_relay_log"] = None
    state["floating_supply"] = 1521517215 * 1e6
    state["understaked_servicers"] = []
    state["understaked_gateways"] = []
    state["understaked_applications"] = []
    state["POKT_burned"] = 0
    state["POKT_minted"] = 0
    state["period_slashing_costs"] = 0
    state["period_jailing_opportunity_cost"] = 0
    state["relays_to_tokens_multiplier"] = None
    state["gateway_fee_per_relay"] = None
    state["application_fee_per_relay"] = None
    state["relay_multiplier"] = {}
    state["oracle_shutdown"] = False
    state["oracle_distortion"] = None

    state = deepcopy(state)
    return state


geo_zones_config = {
    "Test": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
    "Base": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
}

application_config = {
    "Test": [
        Application(
            name="A1",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
        Application(
            name="A2",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 2",
            number_of_services=2,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=False,
        ),
        Application(
            name="A3",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 3",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
    ],
    "Base": [
        Application(
            name="A1",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
        Application(
            name="A2",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 2",
            number_of_services=2,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=False,
        ),
        Application(
            name="A3",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 3",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
    ],
}

application_config['Game50-50'] = list()
# Add honest apps
for i in range(GAMING_APPS_TOTAL//2):
    application_config['Game50-50'].append(Application(
            name="honest_%d"%i,
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),)
# Add adversary apps
for i in range(GAMING_APPS_TOTAL//2):
    application_config['Game50-50'].append(Application(
            name="malicious_%d"%i,
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            services=[],
            geo_zone="Zone 1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),)
    



dao_config = {"Test": DAO(pokt_holdings=0), "Base": DAO(pokt_holdings=0)}

gateways_config = {
    "Test": [
        Gateway(
            name="P1",
            stake_status="Staked",
            delegators=[],
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
        )
    ],
    "Base": [
        Gateway(
            name="P1",
            stake_status="Staked",
            delegators=[],
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
        )
    ],
}

service_config = {
    "Test": [
        Service(
            name="S{}".format(x),
            gateway_api_prefix="S{}".format(x),
            service_id="S{}".format(x),
            servicers=[],
            join_height=-1,
        )
        for x in range(1, 9)
    ],
    "Base": [
        Service(
            name="S{}".format(x),
            gateway_api_prefix="S{}".format(x),
            service_id="S{}".format(x),
            servicers=[],
            join_height=-1,
        )
        for x in range(1, 9)
    ],
}

servicers_config = {"Test": [], "Base": []}

for i in range(1, 6):
    servicers_config["Test"].append(
        Servicer(
            name="X{}".format(i),
            servicer_salary=0,
            report_card=None,
            test_scores=None,
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            service_url=None,
            services=[],
            geo_zone="Zone {}".format(i % 5 + 1),
            operator_public_key=None,
            pause_height=None,
            stake_status="Staked",
            unstaking_height=None,
            QoS=0.8,
        )
    )


for i in range(1, 11):
    servicers_config["Base"].append(
        Servicer(
            name="X{}".format(i),
            servicer_salary=0,
            report_card=None,
            test_scores=None,
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            service_url=None,
            services=[],
            geo_zone="Zone {}".format(i % 5 + 1),
            operator_public_key=None,
            pause_height=None,
            stake_status="Staked",
            unstaking_height=None,
            QoS=0.8,
        )
    )


servicers_config['Game50-50'] = list()
# Add honest nodes
for i in range(GAMING_NODES_TOTAL//2):
    servicers_config['Game50-50'].append(
        Servicer(
            name="honest_{}".format(i),
            servicer_salary=0,
            report_card=None,
            test_scores = {"last_sample_height": -1,
                        "total_samples": -1,
                        "botom_N": None,
                        "data_accuracy": 1.0,
                        "average_latency": 0.0,
                        },
            pokt_holdings=0,
            staked_pokt=15000 * 1e6,
            service_url=None,
            services=[],
            geo_zone="Zone 1",
            operator_public_key=None,
            pause_height=None,
            stake_status="Staked",
            unstaking_height=None,
            QoS=1.0, # All start as honest
        ),)
# Add adversary servicers
for i in range(GAMING_NODES_TOTAL//2):
    servicers_config['Game50-50'].append(
        Servicer(
            name="malicious_{}".format(i),
            servicer_salary=0,
            report_card=None,
            test_scores={"last_sample_height": -1,
                        "total_samples": -1,
                        "botom_N": None,
                        "data_accuracy": 1.0,
                        "average_latency": 0.0,
                        },
            pokt_holdings=0,
            staked_pokt=15000 * 1e6,
            service_url=None,
            services=[],
            geo_zone="Zone 1",
            operator_public_key=None,
            pause_height=None,
            stake_status="Staked",
            unstaking_height=None,
            QoS=1.0, # All start as honest
        ),)
    

validators_config = {
    "Test": [
        Validator(
            name="Mega Validator",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            service_url=None,
            operator_public_key=None,
            stake_status="Staked",
        )
    ],
    "Base": [
        Validator(
            name="Mega Validator",
            pokt_holdings=15000 * 1e6,
            staked_pokt=15000 * 1e6,
            service_url=None,
            operator_public_key=None,
            stake_status="Staked",
        )
    ],
}


def find_total_service_connections(state):
    return sum(map(lambda x: len(x.services), state["Servicers"]))


def find_service_density(state):
    total_services = find_total_service_connections(state)
    density = total_services / len(state["Services"]) / len(state["Servicers"])
    return density


def enforce_density_service_servicers(state, params):
    pairs = list(product(state["Servicers"], state["Services"]))
    random.shuffle(pairs)
    params_density = deepcopy(params)
    if type(params_density["servicer_service_density_starting"]) == list:
        for key in params_density:
            params_density[key] = params_density[key][0]
    while (
        len(pairs) > 0
        and find_service_density(state)
        < params_density["servicer_service_density_starting"]
    ):
        pair = pairs.pop()
        space = ({"service": pair[1], "servicer": pair[0]},)
        space = service_linking_policy(state, params_density, space)
        if space[0]:
            link_service_mechanism(state, params_density, space)
