from copy import deepcopy

config_option_map = {
    "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"}
}


def build_params(config_option):
    config_option = config_option_map[config_option]
    a = system_param_config[config_option["System"]]
    b = behavior_param_config[config_option["Behaviors"]]
    c = functional_param_config[config_option["Functional"]]
    params = {**a, **b, **c}

    params = deepcopy(params)
    return params


system_param_config = {
    "Test": {
        "minimum_stake_servicer": [15000],
        "minimum_stake_period_servicer": [None],
        "minimum_pause_time": [10],
        "max_chains_servicer": [15],
        "salary_block_frequency": [None],
        "minimum_test_score_threshold": [None],
        "minimum_report_card_threshold": [None],
        "servicer_unbounding_period": [None],
        "relays_to_tokens_multiplier": [161.29],
        "slash_fraction_downtime": [None],
        "replay_attack_burn_multiplier": [None],
        "max_jailed_blocks": [None],
        "downtime_jail_duration": [None],
        "minimum_servicers_per_session": [1],
        "maximum_servicers_per_session": [5],
        "application_unstaking_time": [None],
        "application_fee_per_relay": [27.42],
        "minimum_application_stake": [15000],
        "app_burn_per_session": [0],
        "app_burn_per_relay": [None],
        "block_proposer_allocation": [0.05],
        "dao_allocation": [0.1],
        "servicer_allocation": [0.85],
        "stake_per_app_delegation": [15000],
        "gateway_fee_per_relay": [27.42],
        "gateway_minimum_stake": [150000],
        "gateway_unstaking_time": [None],
        "session_block_frequency": [None],
        "session_token_bucket_coefficient": [100],
        "dao_fee_percentage": [0.1],
        "validator_fee_percentage": [0.9],
        "maturity_relay_cost": [None],
        "maturity_relay_charge": [None],
        "min_bootstrap_gateway_fee_per_relay": [None],
        "max_bootstrap_servicer_cost_per_relay": [None],
        "servicer_bootstrap_unwind_start": [None],
        "servicer_bootstrap_end": [None],
        "gateway_bootstrap_unwind_start": [None],
        "gateway_bootstrap_unwind_end": [None],
        "transaction_fee": [0.01],
        "supported_services": [None],
    }
}


behavior_param_config = {
    "Test": {
        "application_max_number": [20],
        "servicer_max_number": [20],
        "service_max_number": [10],
        "gateway_max_number": [25],
        "service_max_number_link": [3],
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
    }
}


functional_param_config = {
    "Test": {
        "application_join_function": ["simple_unfiform"],
        "servicer_join_function": ["simple_unfiform"],
        "service_join_function": ["simple_unfiform"],
        "gateway_join_function": ["simple_unfiform"],
        "service_linking_function": ["test"],
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
    }
}
