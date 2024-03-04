from copy import deepcopy
from ..types import (
    ParamType,
    SystemParamsType,
    BehaviorParamsType,
    FunctionalParamsType,
)
from typing import Dict
from itertools import product

# A map of simulation configurations to the three components (system, behaviors, and functional parameterization)
config_option_map = {
    "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"},
    "Base": {"System": "Base", "Behaviors": "Base", "Functional": "Base"},
    "BaseDynamic": {"System": "BaseDynamic", "Behaviors": "Base", "Functional": "Base"},
    "BaseEvent": {"System": "Base", "Behaviors": "BaseEvent", "Functional": "Base"},

    "ImplicitQoS": {"System": "ImplicitQoS", "Behaviors": "Test", "Functional": "Test"},
}


def build_params(config_option: str, singles: bool = False) -> ParamType:
    # Find the mapping of configuration option to the system, behaviors, and functional parameterization selections
    if config_option in config_option_map:
        config_option = config_option_map[config_option]
        # Pull the relevant parameterizations
        a = system_param_config[config_option["System"]]
        b = behavior_param_config[config_option["Behaviors"]]
        c = functional_param_config[config_option["Functional"]]

        # Combine parameterizations
        params = {**a, **b, **c}
    else:
        params = config_option_map_sweep[config_option]

    # Add a check which makes it only single dimension lists
    assert all(
        [len(x) == 1 for x in params.values()]
    ), "All the lengths must be 1 for this set of cadCAD simulations"

    # Deepcopy to avoid changing source
    params = deepcopy(params)

    if singles:
        for x in params:
            params[x] = params[x][0]

    return params


def create_sweep(prefix, sweep, config_option_map_sweep):
    cartesian_product = list(product(*sweep.values()))
    key_str_list = [f"{prefix}{i+1}" for i in range(len(cartesian_product))]
    for i in range(len(cartesian_product)):
        vals = cartesian_product[i]
        config_option_map_sweep["{}{}".format(prefix, i + 1)] = {}
        for k, x in zip(sweep.keys(), vals):
            config_option_map_sweep["{}{}".format(prefix, i + 1)][k] = [x]

    assert CORE_PARAM_KEYS == sorted(
        list(config_option_map_sweep["{}{}".format(prefix, i + 1)].keys())
    ), "Non-matching parameter keys, something was added!"
    return key_str_list


system_param_config: Dict[str, SystemParamsType] = {
    "Test": {
        "granularity" : ["day"],
        "minimum_stake_servicer": [15000 * 1e6],
        "minimum_stake_period_servicer": [10],
        "minimum_pause_time": [10],
        "max_chains_servicer": [15],
        # "salary_block_frequency": [None],
        # "minimum_test_score_threshold": [None],
        # "minimum_report_card_threshold": [None],
        # "servicer_unbounding_period": [None],
        "relays_to_tokens_multiplier": [161.29],
        "slash_fraction_downtime": [0.000001000000000000],
        # "replay_attack_burn_multiplier": [3],
        # "max_jailed_blocks": [37960],
        # "downtime_jail_duration": [3600000000000],  # In nanoseconds
        "minimum_servicers_per_session": [1],
        "maximum_servicers_per_session": [5],
        # "application_unstaking_time": [None],
        "application_fee_per_relay": ["GFPR*1.25"],
        "minimum_application_stake": [15000 * 1e6],
        "app_burn_per_session": [0],
        "app_burn_per_relay": [0],
        "block_proposer_allocation": [0.05],
        "dao_allocation": [0.1],
        "stake_per_app_delegation": [15000 * 1e6],
        "gateway_fee_per_relay": [27.42],
        "gateway_minimum_stake": [150000 * 1e6],
        # "gateway_unstaking_time": [None],
        # "session_block_frequency": [None],
        "session_token_bucket_coefficient": [100],
        "dao_fee_percentage": [0.9],
        "validator_fee_percentage": [0.1],
        "maturity_relay_cost": [0.000001971 * 0.75],
        "maturity_relay_charge": [0.000001971],
        "min_bootstrap_gateway_fee_per_relay": [0.00000085],
        "max_bootstrap_servicer_cost_per_relay": [0.000005],
        "servicer_bootstrap_unwind_start": [1.5],
        "servicer_bootstrap_end": [10],
        "gateway_bootstrap_unwind_start": [3],  # In billion
        "gateway_bootstrap_end": [20],  # In billion
        "transaction_fee": [0.01],
        "supply_grow_cap": [0.05],
        # "supported_services": [None],
        "oracle_treatment_time_mean": [10],
        "kpi_3_R": [1.632 * 10**-5],
    },
    "Base": {
        "granularity" : ["day"],
        "minimum_stake_servicer": [15000 * 1e6],
        "minimum_stake_period_servicer": [10],
        "minimum_pause_time": [10],
        "max_chains_servicer": [15],
        "relays_to_tokens_multiplier": [161.29],
        "slash_fraction_downtime": [0.000001000000000000],
        # "downtime_jail_duration": [3600000000000],  # In nanoseconds
        "minimum_servicers_per_session": [1],
        "maximum_servicers_per_session": [5],
        "application_fee_per_relay": ["GFPR*1.25"],
        "minimum_application_stake": [15000 * 1e6],
        "app_burn_per_session": [0],
        "app_burn_per_relay": [0],
        "block_proposer_allocation": [0.05],
        "dao_allocation": [0.1],
        "stake_per_app_delegation": [15000 * 1e6],
        "gateway_fee_per_relay": [27.42],
        "gateway_minimum_stake": [150000 * 1e6],
        "session_token_bucket_coefficient": [100],
        "dao_fee_percentage": [0.9],
        "validator_fee_percentage": [0.1],
        "transaction_fee": [0.01],
        "min_bootstrap_gateway_fee_per_relay": [0.00000085],
        "maturity_relay_charge": [0.000001971],
        "gateway_bootstrap_unwind_start": [3],  # In billion
        "gateway_bootstrap_end": [20],  # In billion
        "supply_grow_cap": [0.05],
        "servicer_bootstrap_end": [10],
        "max_bootstrap_servicer_cost_per_relay": [0.000005],
        "servicer_bootstrap_unwind_start": [1.5],
        "maturity_relay_cost": [0.000001971 * 0.75],
        "oracle_treatment_time_mean": [10],
        "kpi_3_R": [1.632 * 10**-5],
    },
}

system_param_config["BaseDynamic"] = deepcopy(system_param_config["Base"])
system_param_config["BaseDynamic"]["relays_to_tokens_multiplier"] = ["Dynamic"]
system_param_config["BaseDynamic"]["gateway_fee_per_relay"] = ["Dynamic"]


system_param_config["ImplicitQoS"] = deepcopy(system_param_config["Test"])
system_param_config["ImplicitQoS"]["granularity"] = ["session"]



behavior_param_config: Dict[str, BehaviorParamsType] = {
    "Test": {
        "application_max_number": [20],
        "servicer_max_number": [20],
        "service_max_number": [10],
        "gateway_max_number": [25],
        "service_max_number_link": [8],
        "application_leave_probability": [0.01],
        "gateway_leave_probability": [0.01],
        "service_leave_probability": [0.0025],
        "servicer_leave_probability": [0.01],
        "service_unlinking_probability": [0.01],
        "gateway_undelegation_probability": [0.01],
        "relays_per_session_gamma_distribution_shape": [500],
        "relays_per_session_gamma_distribution_scale": [50],
        "average_session_per_application": [24],
        "servicer_jailing_probability": [0.001],
        "uses_gateway_probability": [0.5],
        "applications_use_min_servicers": [1],
        "applications_use_max_servicers": [3],
        "lambda_ewm_revenue_expectation": [0.9],
        "service_linking_probability_normal": [0.01],
        "service_linking_probability_just_joined": [0.5],
        "kick_bottom_probability": [0.5],
        "oracle_price_kde_bandwidth": [0.30745369958511376],
        "oracle_price_interarrival_time_flag": [1],
        "event": [None],
        "servicer_service_density_starting": [None],
    },
    "Base": {
        "application_max_number": [20],
        "servicer_max_number": [20],
        "service_max_number": [10],
        "gateway_max_number": [25],
        "service_max_number_link": [15],
        "application_leave_probability": [0.02],
        "gateway_leave_probability": [0.005],
        "service_leave_probability": [0.0025],
        "servicer_leave_probability": [0.015],
        "service_unlinking_probability": [0.01],
        "gateway_undelegation_probability": [0.01],
        "relays_per_session_gamma_distribution_shape": [5],
        "relays_per_session_gamma_distribution_scale": [300000],
        "average_session_per_application": [24],
        "servicer_jailing_probability": [0.001],
        "uses_gateway_probability": [0.5],
        "applications_use_min_servicers": [1],
        "applications_use_max_servicers": [3],
        "lambda_ewm_revenue_expectation": [0.9],
        "service_linking_probability_normal": [0.01],
        "service_linking_probability_just_joined": [0.5],
        "kick_bottom_probability": [0.5],
        "oracle_price_kde_bandwidth": [0.30745369958511376],
        "oracle_price_interarrival_time_flag": [1],
        "event": [None],
        "servicer_service_density_starting": [None],
    },
}

behavior_param_config["BaseEvent"] = deepcopy(behavior_param_config["Base"])
behavior_param_config["BaseEvent"]["event"] = ["servicer_shutdown_by_geozone_random"]

functional_param_config: Dict[str, FunctionalParamsType] = {
    "Test": {
        "application_join_function": ["simple_unfiform"],
        "servicer_join_function": ["simple_unfiform"],
        "service_join_function": ["simple_unfiform"],
        "gateway_join_function": ["simple_unfiform"],
        "service_linking_function": ["basic"],
        "gateway_delegation_function": ["basic"],
        "relay_requests_function": ["test"],
        "submit_relay_requests_function": ["basic_gamma"],
        "submit_relay_requests_policy_function": ["V1"],
        "application_leave_function": ["basic"],
        "service_leave_function": ["basic"],
        "servicer_leave_function": ["basic"],
        "gateway_leave_function": ["basic"],
        "service_unlinking_function": ["basic"],
        "gateway_undelegation_function": ["basic"],
        "servicer_stake_function": ["basic"],
        "application_stake_function": ["basic"],
        "jailing_function": ["basic"],
        "gateway_stake_function": ["basic"],
    },
    "Base": {
        "application_join_function": ["simple_unfiform"],
        "servicer_join_function": ["simple_unfiform"],
        "service_join_function": ["simple_unfiform"],
        "gateway_join_function": ["simple_unfiform"],
        "service_linking_function": ["basic"],
        "gateway_delegation_function": ["basic"],
        "relay_requests_function": ["test"],
        "submit_relay_requests_function": ["basic_gamma"],
        "submit_relay_requests_policy_function": ["V1"],
        "application_leave_function": ["basic"],
        "service_leave_function": ["basic"],
        "servicer_leave_function": ["basic"],
        "gateway_leave_function": ["basic"],
        "service_unlinking_function": ["basic"],
        "gateway_undelegation_function": ["basic"],
        "servicer_stake_function": ["basic"],
        "application_stake_function": ["basic"],
        "jailing_function": ["basic"],
        "gateway_stake_function": ["basic"],
    },
}
config_option_map_sweep = {}

test_sweep = build_params("Base")
CORE_PARAM_KEYS = sorted(list(test_sweep.keys()))
test_sweep["application_max_number"] = [20, 30, 40]
test_sweep["servicer_max_number"] = [20, 30, 40]
test_sweep["relays_per_session_gamma_distribution_scale"] = [200000, 300000, 400000]

create_sweep("Test", test_sweep, config_option_map_sweep)


implicit_qos_sweep = build_params("Base")
CORE_PARAM_KEYS = sorted(list(implicit_qos_sweep.keys()))
implicit_qos_sweep["application_max_number"] = [20, 30, 40]
implicit_qos_sweep["servicer_max_number"] = [20, 30, 40]
implicit_qos_sweep["relays_per_session_gamma_distribution_scale"] = [200000, 300000, 400000]

create_sweep("ImplicitQoS", implicit_qos_sweep, config_option_map_sweep)



gateway_viability_sweep_ag1_ = build_params("Base")
gateway_viability_sweep_ag1_["session_token_bucket_coefficient"] = [25, 400]
gateway_viability_sweep_ag1_["gateway_fee_per_relay"] = [10, 100]
gateway_viability_sweep_ag1_["application_fee_per_relay"] = [10, 100]
gateway_viability_sweep_ag1_["gateway_minimum_stake"] = [100000 * 1e6, 200000 * 1e6]
gateway_viability_sweep_ag1_["minimum_application_stake"] = [
    10000 * 1e6,
    20000 * 1e6,
]
gateway_viability_sweep_ag1_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag1_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]

create_sweep(
    "gateway_viability_sweep_ag1_",
    gateway_viability_sweep_ag1_,
    config_option_map_sweep,
)


network_failures_service_ag1_ = build_params("Base")
network_failures_service_ag1_["slash_fraction_downtime"] = [1e-10, 1e-1]
network_failures_service_ag1_["max_chains_servicer"] = [1, 20]
network_failures_service_ag1_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag1_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]


create_sweep(
    "network_failures_service_ag1_",
    network_failures_service_ag1_,
    config_option_map_sweep,
)


gateway_viability_sweep_ag2_ = build_params("Base")
gateway_viability_sweep_ag2_["session_token_bucket_coefficient"] = [25, 212.5]
gateway_viability_sweep_ag2_["gateway_fee_per_relay"] = [10, 55.0]
gateway_viability_sweep_ag2_["application_fee_per_relay"] = [10, 55.0]
gateway_viability_sweep_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
gateway_viability_sweep_ag2_["minimum_application_stake"] = [
    10000000000.0,
    15000000000.0,
]
gateway_viability_sweep_ag2_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag2_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]
create_sweep(
    "gateway_viability_sweep_ag2_",
    gateway_viability_sweep_ag2_,
    config_option_map_sweep,
)

gateway_viability_sweep_ag3_ = build_params("Base")
gateway_viability_sweep_ag3_["session_token_bucket_coefficient"] = [25, 118.75]
gateway_viability_sweep_ag3_["gateway_fee_per_relay"] = [10, 32.5]
gateway_viability_sweep_ag3_["application_fee_per_relay"] = [10, 32.5]
gateway_viability_sweep_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
gateway_viability_sweep_ag3_["minimum_application_stake"] = [
    12500000000.0,
    15000000000.0,
]
gateway_viability_sweep_ag3_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag3_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]
create_sweep(
    "gateway_viability_sweep_ag3_",
    gateway_viability_sweep_ag3_,
    config_option_map_sweep,
)

gateway_viability_sweep_ag4_ = build_params("Base")
gateway_viability_sweep_ag4_["session_token_bucket_coefficient"] = [71.875, 118.75]
gateway_viability_sweep_ag4_["gateway_fee_per_relay"] = [10, 21.25]
gateway_viability_sweep_ag4_["application_fee_per_relay"] = [21.25, 32.5]
gateway_viability_sweep_ag4_["gateway_minimum_stake"] = [112500000000.0, 125000000000.0]
gateway_viability_sweep_ag4_["minimum_application_stake"] = [
    12500000000.0,
    13750000000.0,
]
gateway_viability_sweep_ag4_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag4_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]
create_sweep(
    "gateway_viability_sweep_ag4_",
    gateway_viability_sweep_ag4_,
    config_option_map_sweep,
)

gateway_viability_sweep_ag5_ = build_params("Base")
gateway_viability_sweep_ag5_["session_token_bucket_coefficient"] = [71.875, 95.3125]
gateway_viability_sweep_ag5_["gateway_fee_per_relay"] = [10, 15.625]
gateway_viability_sweep_ag5_["application_fee_per_relay"] = [26.875, 32.5]
gateway_viability_sweep_ag5_["gateway_minimum_stake"] = [118750000000.0, 125000000000.0]
gateway_viability_sweep_ag5_["minimum_application_stake"] = [
    13125000000.0,
    13750000000.0,
]
gateway_viability_sweep_ag5_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag5_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]
create_sweep(
    "gateway_viability_sweep_ag5_",
    gateway_viability_sweep_ag5_,
    config_option_map_sweep,
)

gateway_viability_sweep_ag6_ = build_params("Base")
gateway_viability_sweep_ag6_["session_token_bucket_coefficient"] = [71.875, 83.59375]
gateway_viability_sweep_ag6_["gateway_fee_per_relay"] = [10, 12.8125]
gateway_viability_sweep_ag6_["application_fee_per_relay"] = [26.875, 29.6875]
gateway_viability_sweep_ag6_["gateway_minimum_stake"] = [121875000000.0, 125000000000.0]
gateway_viability_sweep_ag6_["minimum_application_stake"] = [
    13437500000.0,
    13750000000.0,
]
gateway_viability_sweep_ag6_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag6_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]
create_sweep(
    "gateway_viability_sweep_ag6_",
    gateway_viability_sweep_ag6_,
    config_option_map_sweep,
)

servicer_viability_ag1_ = build_params("Base")
servicer_viability_ag1_["service_leave_probability"] = [0.0]
servicer_viability_ag1_["service_join_function"] = ["off"]
servicer_viability_ag1_["event"] = ["service_join"]
servicer_viability_ag1_["relays_to_tokens_multiplier"] = [100, 200]
servicer_viability_ag1_["gateway_fee_per_relay"] = [10, 100]
servicer_viability_ag1_["application_fee_per_relay"] = [10, 100]
servicer_viability_ag1_["gateway_minimum_stake"] = [100000 * 1e6, 200000 * 1e6]
servicer_viability_ag1_["minimum_application_stake"] = [
    10000 * 1e6,
    20000 * 1e6,
]
servicer_viability_ag1_["dao_allocation"] = [0.05, 0.15]
servicer_viability_ag1_["validator_fee_percentage"] = [0.01, 0.1]
servicer_viability_ag1_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag1_["kick_bottom_probability"] = [0.01, 0.05, 0.1]

servicer_viability_ag2_ = build_params("Base")
servicer_viability_ag2_["relays_to_tokens_multiplier"] = [100, 150.0]
servicer_viability_ag2_["gateway_fee_per_relay"] = [10, 55.0]
servicer_viability_ag2_["application_fee_per_relay"] = [10, 55.0]
servicer_viability_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
servicer_viability_ag2_["minimum_application_stake"] = [10000000000.0, 15000000000.0]
servicer_viability_ag2_["dao_allocation"] = [0.05, 0.1]
servicer_viability_ag2_["validator_fee_percentage"] = [0.01, 0.055]
servicer_viability_ag2_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag2_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag2_", servicer_viability_ag2_, config_option_map_sweep
)

servicer_viability_ag3_ = build_params("Base")
servicer_viability_ag3_["relays_to_tokens_multiplier"] = [100, 125.0]
servicer_viability_ag3_["gateway_fee_per_relay"] = [10, 32.5]
servicer_viability_ag3_["application_fee_per_relay"] = [10, 32.5]
servicer_viability_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
servicer_viability_ag3_["minimum_application_stake"] = [12500000000.0, 15000000000.0]
servicer_viability_ag3_["dao_allocation"] = [0.07500000000000001, 0.1]
servicer_viability_ag3_["validator_fee_percentage"] = [0.0325, 0.055]
servicer_viability_ag3_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag3_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag3_", servicer_viability_ag3_, config_option_map_sweep
)

servicer_viability_ag4_ = build_params("Base")
servicer_viability_ag4_["relays_to_tokens_multiplier"] = [100, 112.5]
servicer_viability_ag4_["gateway_fee_per_relay"] = [10, 21.25]
servicer_viability_ag4_["application_fee_per_relay"] = [10, 21.25]
servicer_viability_ag4_["gateway_minimum_stake"] = [100000000000.0, 112500000000.0]
servicer_viability_ag4_["minimum_application_stake"] = [12500000000.0, 13750000000.0]
servicer_viability_ag4_["dao_allocation"] = [0.08750000000000001, 0.1]
servicer_viability_ag4_["validator_fee_percentage"] = [0.0325, 0.04375]
servicer_viability_ag4_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag4_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag4_", servicer_viability_ag4_, config_option_map_sweep
)

servicer_viability_ag5_ = build_params("Base")
servicer_viability_ag5_["relays_to_tokens_multiplier"] = [100, 106.25]
servicer_viability_ag5_["gateway_fee_per_relay"] = [10, 15.625]
servicer_viability_ag5_["application_fee_per_relay"] = [10, 15.625]
servicer_viability_ag5_["gateway_minimum_stake"] = [106250000000.0, 112500000000.0]
servicer_viability_ag5_["minimum_application_stake"] = [12500000000.0, 13125000000.0]
servicer_viability_ag5_["dao_allocation"] = [0.08750000000000001, 0.09375]
servicer_viability_ag5_["validator_fee_percentage"] = [0.0325, 0.038125]
servicer_viability_ag5_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag5_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag5_", servicer_viability_ag5_, config_option_map_sweep
)

servicer_viability_ag6_ = build_params("Base")
servicer_viability_ag6_["relays_to_tokens_multiplier"] = [103.125, 106.25]
servicer_viability_ag6_["gateway_fee_per_relay"] = [10, 12.8125]
servicer_viability_ag6_["application_fee_per_relay"] = [10, 12.8125]
servicer_viability_ag6_["gateway_minimum_stake"] = [109375000000.0, 112500000000.0]
servicer_viability_ag6_["minimum_application_stake"] = [12500000000.0, 12812500000.0]
servicer_viability_ag6_["dao_allocation"] = [0.08750000000000001, 0.09062500000000001]
servicer_viability_ag6_["validator_fee_percentage"] = [0.0353125, 0.038125]
servicer_viability_ag6_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag6_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag6_", servicer_viability_ag6_, config_option_map_sweep
)

create_sweep(
    "servicer_viability_ag1_",
    servicer_viability_ag1_,
    config_option_map_sweep,
)

network_viability_ag1_ = build_params("Base")
network_viability_ag1_["relays_to_tokens_multiplier"] = [100, 200]
network_viability_ag1_["gateway_fee_per_relay"] = [10, 100]
network_viability_ag1_["application_fee_per_relay"] = [10, 100]
network_viability_ag1_["gateway_minimum_stake"] = [100000 * 1e6, 200000 * 1e6]
network_viability_ag1_["minimum_application_stake"] = [
    10000 * 1e6,
    20000 * 1e6,
]
network_viability_ag1_["dao_allocation"] = [0.05, 0.15]
network_viability_ag1_["validator_fee_percentage"] = [0.01, 0.1]
network_viability_ag1_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag1_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]


network_viability_ag1_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]

create_sweep(
    "network_viability_ag1_",
    network_viability_ag1_,
    config_option_map_sweep,
)

network_failures_oracle_ag1_ = build_params("Base")
network_failures_oracle_ag1_["relays_to_tokens_multiplier"] = [100, 200]
network_failures_oracle_ag1_["gateway_fee_per_relay"] = [10, 100]
network_failures_oracle_ag1_["application_fee_per_relay"] = [10, 100]
network_failures_oracle_ag1_["gateway_minimum_stake"] = [100000 * 1e6, 200000 * 1e6]
network_failures_oracle_ag1_["minimum_application_stake"] = [
    10000 * 1e6,
    20000 * 1e6,
]
network_failures_oracle_ag1_["dao_allocation"] = [0.05, 0.15]
network_failures_oracle_ag1_["validator_fee_percentage"] = [0.01, 0.1]
network_failures_oracle_ag1_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag1_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]

create_sweep(
    "network_failures_oracle_ag1_",
    network_failures_oracle_ag1_,
    config_option_map_sweep,
)


network_failures_service_ag2_ = build_params("Base")
network_failures_service_ag2_["slash_fraction_downtime"] = [1e-10, 0.05000000005]
network_failures_service_ag2_["max_chains_servicer"] = [1, 10.5]
network_failures_service_ag2_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag2_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]
create_sweep(
    "network_failures_service_ag2_",
    network_failures_service_ag2_,
    config_option_map_sweep,
)


servicer_viability_ag2_ = build_params("Base")
servicer_viability_ag2_["relays_to_tokens_multiplier"] = [100, 150.0]
servicer_viability_ag2_["gateway_fee_per_relay"] = [10, 55.0]
servicer_viability_ag2_["application_fee_per_relay"] = [55.0, 100]
servicer_viability_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
servicer_viability_ag2_["minimum_application_stake"] = [10000000000.0, 15000000000.0]
servicer_viability_ag2_["dao_allocation"] = [0.1, 0.15]
servicer_viability_ag2_["validator_fee_percentage"] = [0.055, 0.1]
servicer_viability_ag2_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag2_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag2_", servicer_viability_ag2_, config_option_map_sweep
)

network_viability_ag2_ = build_params("Base")
network_viability_ag2_["relays_to_tokens_multiplier"] = [150.0, 200]
network_viability_ag2_["gateway_fee_per_relay"] = [10, 55.0]
network_viability_ag2_["application_fee_per_relay"] = [55.0, 100]
network_viability_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
network_viability_ag2_["minimum_application_stake"] = [10000000000.0, 15000000000.0]
network_viability_ag2_["dao_allocation"] = [0.05, 0.1]
network_viability_ag2_["validator_fee_percentage"] = [0.055, 0.1]
network_viability_ag2_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag2_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]
network_viability_ag2_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]
create_sweep("network_viability_ag2_", network_viability_ag2_, config_option_map_sweep)

network_failures_oracle_ag2_ = build_params("Base")
network_failures_oracle_ag2_["relays_to_tokens_multiplier"] = [100, 150.0]
network_failures_oracle_ag2_["gateway_fee_per_relay"] = [10, 55.0]
network_failures_oracle_ag2_["application_fee_per_relay"] = [10, 55.0]
network_failures_oracle_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
network_failures_oracle_ag2_["minimum_application_stake"] = [
    15000000000.0,
    20000000000.0,
]
network_failures_oracle_ag2_["dao_allocation"] = [0.05, 0.1]
network_failures_oracle_ag2_["validator_fee_percentage"] = [0.055, 0.1]
network_failures_oracle_ag2_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag2_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag2_",
    network_failures_oracle_ag2_,
    config_option_map_sweep,
)

servicer_viability_ag3_ = build_params("Base")
servicer_viability_ag3_["relays_to_tokens_multiplier"] = [100, 125.0]
servicer_viability_ag3_["gateway_fee_per_relay"] = [10, 32.5]
servicer_viability_ag3_["application_fee_per_relay"] = [77.5, 100]
servicer_viability_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
servicer_viability_ag3_["minimum_application_stake"] = [10000000000.0, 12500000000.0]
servicer_viability_ag3_["dao_allocation"] = [0.1, 0.125]
servicer_viability_ag3_["validator_fee_percentage"] = [0.055, 0.0775]
servicer_viability_ag3_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag3_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag3_", servicer_viability_ag3_, config_option_map_sweep
)

servicer_viability_ag4_ = build_params("Base")
servicer_viability_ag4_["relays_to_tokens_multiplier"] = [100, 112.5]
servicer_viability_ag4_["gateway_fee_per_relay"] = [10, 21.25]
servicer_viability_ag4_["application_fee_per_relay"] = [88.75, 100]
servicer_viability_ag4_["gateway_minimum_stake"] = [100000000000.0, 112500000000.0]
servicer_viability_ag4_["minimum_application_stake"] = [10000000000.0, 11250000000.0]
servicer_viability_ag4_["dao_allocation"] = [0.1125, 0.125]
servicer_viability_ag4_["validator_fee_percentage"] = [0.06625, 0.0775]
servicer_viability_ag4_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag4_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag4_", servicer_viability_ag4_, config_option_map_sweep
)

servicer_viability_ag5_ = build_params("Base")
servicer_viability_ag5_["relays_to_tokens_multiplier"] = [100, 106.25]
servicer_viability_ag5_["gateway_fee_per_relay"] = [10, 15.625]
servicer_viability_ag5_["application_fee_per_relay"] = [88.75, 94.375]
servicer_viability_ag5_["gateway_minimum_stake"] = [100000000000.0, 106250000000.0]
servicer_viability_ag5_["minimum_application_stake"] = [10625000000.0, 11250000000.0]
servicer_viability_ag5_["dao_allocation"] = [0.1125, 0.11875]
servicer_viability_ag5_["validator_fee_percentage"] = [0.071875, 0.0775]
servicer_viability_ag5_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag5_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag5_", servicer_viability_ag5_, config_option_map_sweep
)

servicer_viability_ag6_ = build_params("Base")
servicer_viability_ag6_["relays_to_tokens_multiplier"] = [103.125, 106.25]
servicer_viability_ag6_["gateway_fee_per_relay"] = [12.8125, 15.625]
servicer_viability_ag6_["application_fee_per_relay"] = [88.75, 91.5625]
servicer_viability_ag6_["gateway_minimum_stake"] = [100000000000.0, 103125000000.0]
servicer_viability_ag6_["minimum_application_stake"] = [10625000000.0, 10937500000.0]
servicer_viability_ag6_["dao_allocation"] = [0.1125, 0.115625]
servicer_viability_ag6_["validator_fee_percentage"] = [0.071875, 0.07468749999999999]
servicer_viability_ag6_["service_linking_probability_just_joined"] = [0.1, 0.5, 0.9]
servicer_viability_ag6_["kick_bottom_probability"] = [0.01, 0.05, 0.1]
create_sweep(
    "servicer_viability_ag6_", servicer_viability_ag6_, config_option_map_sweep
)

network_failures_service_ag3_ = build_params("Base")
network_failures_service_ag3_["slash_fraction_downtime"] = [1e-10, 0.025000000075]
network_failures_service_ag3_["max_chains_servicer"] = [5.75, 10.5]
network_failures_service_ag3_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag3_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]
create_sweep(
    "network_failures_service_ag3_",
    network_failures_service_ag3_,
    config_option_map_sweep,
)


network_viability_ag3_ = build_params("Base")
network_viability_ag3_["relays_to_tokens_multiplier"] = [175.0, 200]
network_viability_ag3_["gateway_fee_per_relay"] = [10, 32.5]
network_viability_ag3_["application_fee_per_relay"] = [77.5, 100]
network_viability_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
network_viability_ag3_["minimum_application_stake"] = [10000000000.0, 12500000000.0]
network_viability_ag3_["dao_allocation"] = [0.05, 0.07500000000000001]
network_viability_ag3_["validator_fee_percentage"] = [0.0775, 0.1]
network_viability_ag3_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag3_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]
network_viability_ag3_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]
create_sweep("network_viability_ag3_", network_viability_ag3_, config_option_map_sweep)

network_failures_service_ag4_ = build_params("Base")
network_failures_service_ag4_["slash_fraction_downtime"] = [1e-10, 0.012500000087500001]
network_failures_service_ag4_["max_chains_servicer"] = [5.75, 8.125]
network_failures_service_ag4_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag4_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]
create_sweep(
    "network_failures_service_ag4_",
    network_failures_service_ag4_,
    config_option_map_sweep,
)


network_viability_ag4_ = build_params("Base")
network_viability_ag4_["relays_to_tokens_multiplier"] = [187.5, 200]
network_viability_ag4_["gateway_fee_per_relay"] = [10, 21.25]
network_viability_ag4_["application_fee_per_relay"] = [77.5, 88.75]
network_viability_ag4_["gateway_minimum_stake"] = [112500000000.0, 125000000000.0]
network_viability_ag4_["minimum_application_stake"] = [10000000000.0, 11250000000.0]
network_viability_ag4_["dao_allocation"] = [0.0625, 0.07500000000000001]
network_viability_ag4_["validator_fee_percentage"] = [0.08875, 0.1]
network_viability_ag4_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag4_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]
network_viability_ag4_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]
create_sweep("network_viability_ag4_", network_viability_ag4_, config_option_map_sweep)


network_failures_oracle_ag3_ = build_params("Base")
network_failures_oracle_ag3_["relays_to_tokens_multiplier"] = [125.0, 150.0]
network_failures_oracle_ag3_["gateway_fee_per_relay"] = [10, 32.5]
network_failures_oracle_ag3_["application_fee_per_relay"] = [10, 32.5]
network_failures_oracle_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
network_failures_oracle_ag3_["minimum_application_stake"] = [
    15000000000.0,
    17500000000.0,
]
network_failures_oracle_ag3_["dao_allocation"] = [0.05, 0.07500000000000001]
network_failures_oracle_ag3_["validator_fee_percentage"] = [0.0775, 0.1]
network_failures_oracle_ag3_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag3_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag3_",
    network_failures_oracle_ag3_,
    config_option_map_sweep,
)

network_failures_service_ag5_ = build_params("Base")
network_failures_service_ag5_["slash_fraction_downtime"] = [1e-10, 0.00625000009375]
network_failures_service_ag5_["max_chains_servicer"] = [6.9375, 8.125]
network_failures_service_ag5_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag5_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]
create_sweep(
    "network_failures_service_ag5_",
    network_failures_service_ag5_,
    config_option_map_sweep,
)


network_viability_ag5_ = build_params("Base")
network_viability_ag5_["relays_to_tokens_multiplier"] = [187.5, 193.75]
network_viability_ag5_["gateway_fee_per_relay"] = [10, 15.625]
network_viability_ag5_["application_fee_per_relay"] = [83.125, 88.75]
network_viability_ag5_["gateway_minimum_stake"] = [118750000000.0, 125000000000.0]
network_viability_ag5_["minimum_application_stake"] = [10000000000.0, 10625000000.0]
network_viability_ag5_["dao_allocation"] = [0.06875, 0.07500000000000001]
network_viability_ag5_["validator_fee_percentage"] = [0.094375, 0.1]
network_viability_ag5_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag5_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]
network_viability_ag5_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]
create_sweep("network_viability_ag5_", network_viability_ag5_, config_option_map_sweep)


network_failures_oracle_ag4_ = build_params("Base")
network_failures_oracle_ag4_["relays_to_tokens_multiplier"] = [137.5, 150.0]
network_failures_oracle_ag4_["gateway_fee_per_relay"] = [10, 21.25]
network_failures_oracle_ag4_["application_fee_per_relay"] = [10, 21.25]
network_failures_oracle_ag4_["gateway_minimum_stake"] = [112500000000.0, 125000000000.0]
network_failures_oracle_ag4_["minimum_application_stake"] = [
    16250000000.0,
    17500000000.0,
]
network_failures_oracle_ag4_["dao_allocation"] = [0.05, 0.0625]
network_failures_oracle_ag4_["validator_fee_percentage"] = [0.08875, 0.1]
network_failures_oracle_ag4_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag4_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag4_",
    network_failures_oracle_ag4_,
    config_option_map_sweep,
)

network_failures_service_ag6_ = build_params("Base")
network_failures_service_ag6_["slash_fraction_downtime"] = [1e-10, 0.003125000096875]
network_failures_service_ag6_["max_chains_servicer"] = [7.53125, 8.125]
network_failures_service_ag6_["servicer_service_density_starting"] = [0.1, 0.5, 1]
network_failures_service_ag6_["event"] = [
    "servicer_shutdown_by_geozone_random",
    "service_shutdown_random_t1",
    "service_shutdown_random_t7",
    "service_shutdown_random_t500",
]
create_sweep(
    "network_failures_service_ag6_",
    network_failures_service_ag6_,
    config_option_map_sweep,
)


network_viability_ag6_ = build_params("Base")
network_viability_ag6_["relays_to_tokens_multiplier"] = [187.5, 190.625]
network_viability_ag6_["gateway_fee_per_relay"] = [12.8125, 15.625]
network_viability_ag6_["application_fee_per_relay"] = [83.125, 85.9375]
network_viability_ag6_["gateway_minimum_stake"] = [118750000000.0, 121875000000.0]
network_viability_ag6_["minimum_application_stake"] = [10312500000.0, 10625000000.0]
network_viability_ag6_["dao_allocation"] = [0.07187500000000001, 0.07500000000000001]
network_viability_ag6_["validator_fee_percentage"] = [0.09718750000000001, 0.1]
network_viability_ag6_["relays_per_session_gamma_distribution_shape"] = [250, 500, 750]
network_viability_ag6_["service_linking_probability_normal"] = [0.001, 0.01, 0.1]
network_viability_ag6_["event"] = [
    "double_relays_1_service",
    "double_relays_3_services",
    "double_relays_5_services",
]
create_sweep("network_viability_ag6_", network_viability_ag6_, config_option_map_sweep)

network_failures_oracle_ag2_ = build_params("Base")
network_failures_oracle_ag2_["relays_to_tokens_multiplier"] = [100, 150.0]
network_failures_oracle_ag2_["gateway_fee_per_relay"] = [10, 55.0]
network_failures_oracle_ag2_["application_fee_per_relay"] = [10, 55.0]
network_failures_oracle_ag2_["gateway_minimum_stake"] = [100000000000.0, 150000000000.0]
network_failures_oracle_ag2_["minimum_application_stake"] = [
    15000000000.0,
    20000000000.0,
]
network_failures_oracle_ag2_["dao_allocation"] = [0.05, 0.1]
network_failures_oracle_ag2_["validator_fee_percentage"] = [0.01, 0.055]
network_failures_oracle_ag2_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag2_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag2_",
    network_failures_oracle_ag2_,
    config_option_map_sweep,
)

network_failures_oracle_ag3_ = build_params("Base")
network_failures_oracle_ag3_["relays_to_tokens_multiplier"] = [100, 125.0]
network_failures_oracle_ag3_["gateway_fee_per_relay"] = [10, 32.5]
network_failures_oracle_ag3_["application_fee_per_relay"] = [32.5, 55.0]
network_failures_oracle_ag3_["gateway_minimum_stake"] = [100000000000.0, 125000000000.0]
network_failures_oracle_ag3_["minimum_application_stake"] = [
    17500000000.0,
    20000000000.0,
]
network_failures_oracle_ag3_["dao_allocation"] = [0.05, 0.07500000000000001]
network_failures_oracle_ag3_["validator_fee_percentage"] = [0.01, 0.0325]
network_failures_oracle_ag3_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag3_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag3_",
    network_failures_oracle_ag3_,
    config_option_map_sweep,
)

network_failures_oracle_ag4_ = build_params("Base")
network_failures_oracle_ag4_["relays_to_tokens_multiplier"] = [100, 112.5]
network_failures_oracle_ag4_["gateway_fee_per_relay"] = [10, 21.25]
network_failures_oracle_ag4_["application_fee_per_relay"] = [43.75, 55.0]
network_failures_oracle_ag4_["gateway_minimum_stake"] = [112500000000.0, 125000000000.0]
network_failures_oracle_ag4_["minimum_application_stake"] = [
    18750000000.0,
    20000000000.0,
]
network_failures_oracle_ag4_["dao_allocation"] = [0.0625, 0.07500000000000001]
network_failures_oracle_ag4_["validator_fee_percentage"] = [0.01, 0.02125]
network_failures_oracle_ag4_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag4_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag4_",
    network_failures_oracle_ag4_,
    config_option_map_sweep,
)

network_failures_oracle_ag5_ = build_params("Base")
network_failures_oracle_ag5_["relays_to_tokens_multiplier"] = [100, 106.25]
network_failures_oracle_ag5_["gateway_fee_per_relay"] = [10, 15.625]
network_failures_oracle_ag5_["application_fee_per_relay"] = [43.75, 49.375]
network_failures_oracle_ag5_["gateway_minimum_stake"] = [112500000000.0, 118750000000.0]
network_failures_oracle_ag5_["minimum_application_stake"] = [
    19375000000.0,
    20000000000.0,
]
network_failures_oracle_ag5_["dao_allocation"] = [0.0625, 0.06875]
network_failures_oracle_ag5_["validator_fee_percentage"] = [0.015625, 0.02125]
network_failures_oracle_ag5_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag5_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag5_",
    network_failures_oracle_ag5_,
    config_option_map_sweep,
)

network_failures_oracle_ag6_ = build_params("Base")
network_failures_oracle_ag6_["relays_to_tokens_multiplier"] = [100, 103.125]
network_failures_oracle_ag6_["gateway_fee_per_relay"] = [10, 12.8125]
network_failures_oracle_ag6_["application_fee_per_relay"] = [46.5625, 49.375]
network_failures_oracle_ag6_["gateway_minimum_stake"] = [115625000000.0, 118750000000.0]
network_failures_oracle_ag6_["minimum_application_stake"] = [
    19687500000.0,
    20000000000.0,
]
network_failures_oracle_ag6_["dao_allocation"] = [0.065625, 0.06875]
network_failures_oracle_ag6_["validator_fee_percentage"] = [
    0.018437500000000002,
    0.02125,
]
network_failures_oracle_ag6_["oracle_treatment_time_mean"] = [1, 10, 100]
network_failures_oracle_ag6_["event"] = [
    "oracle_shutdown",
    "oracle_delay_poisson",
    "oracle_distortion_unbiased_low_noise_poisson",
    "oracle_distortion_unbiased_high_noise_poisson",
    "oracle_distortion_positive_bias_low_noise_poisson",
    "oracle_distortion_positive_bias_high_noise_poisson",
    "oracle_distortion_negative_bias_low_noise_poisson",
    "oracle_distortion_negative_bias_high_noise_poisson",
]
create_sweep(
    "network_failures_oracle_ag6_",
    network_failures_oracle_ag6_,
    config_option_map_sweep,
)

for key in config_option_map_sweep:
    config_option_map_sweep[key]["dao_fee_percentage"] = [
        1 - config_option_map_sweep[key]["validator_fee_percentage"][0]
    ]
