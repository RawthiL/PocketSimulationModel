from typing import NewType, TypedDict, List, Literal
from .Primitives import POKTType, PercentType, NanoSecondsType, GeoZoneType
from .Entity import (
    ApplicationEntityType,
    GatewayEntityType,
    ServiceEntityType,
    ServicerEntityType,
)
from .Data import SessionType

StateType = NewType(
    "State",
    TypedDict(
        "State",
        {
            "Geozones": List[GeoZoneType],
            "Applications": List[ApplicationEntityType],
            "DAO": object,
            "Gateways": List[GatewayEntityType],
            "Services": List[ServicerEntityType],
            "Servicers": List[ServiceEntityType],
            "Validators": List[object],
            "height": int,
            "day": int,
            "Sessions": List[SessionType],
            "total_relays": int,
            "processed_relays": int,
            "pokt_price_true": float,
            "pokt_price_oracle": float,
            "n_transactions": int,
            "relay_log": dict,
            "servicer_relay_log": dict,
            "floating_supply": int,
            "understaked_servicers": List[ServiceEntityType],
            "understaked_gateways": List[GatewayEntityType],
            "understaked_applications": List[GatewayEntityType],
            "POKT_burned": int,
            "POKT_minted": int,
            "period_slashing_costs": int,
            "period_jailing_opportunity_cost": int,
        },
    ),
)


SystemParamsType = NewType(
    "SystemParams",
    TypedDict(
        "System Params",
        {
            "minimum_stake_servicer": List[POKTType],
            "minimum_stake_period_servicer": List[int],
            "minimum_pause_time": List[int],
            "max_chains_servicer": List[int],
            "relays_to_tokens_multiplier": List[POKTType],
            "slash_fraction_downtime": List[PercentType],
            "downtime_jail_duration": List[NanoSecondsType],
            "minimum_servicers_per_session": List[int],
            "maximum_servicers_per_session": List[int],
            "application_fee_per_relay": List[POKTType],
            "minimum_application_stake": List[POKTType],
            "app_burn_per_session": List[POKTType],
            "app_burn_per_relay": List[POKTType],
            "block_proposer_allocation": List[PercentType],
            "dao_allocation": List[PercentType],
            "servicer_allocation": List[PercentType],
            "stake_per_app_delegation": List[POKTType],
            "gateway_fee_per_relay": List[POKTType],
            "gateway_minimum_stake": List[POKTType],
            "session_token_bucket_coefficient": List[int],
            "dao_fee_percentage": List[PercentType],
            "validator_fee_percentage": List[PercentType],
            "transaction_fee": List[PercentType],
        },
    ),
)
BehaviorParamsType = NewType(
    "BehaviorParams",
    TypedDict(
        "Behavior Params",
        {
            "application_max_number": List[int],
            "servicer_max_number": List[int],
            "service_max_number": List[int],
            "gateway_max_number": List[int],
            "service_max_number_link": List[int],
            "application_leave_probability": List[float],
            "gateway_leave_probability": List[float],
            "service_leave_probability": List[float],
            "servicer_leave_probability": List[float],
            "service_unlinking_probability": List[float],
            "gateway_undelegation_probability": List[float],
            "relays_per_session_gamma_distribution_shape": List[float],
            "relays_per_session_gamma_distribution_scale": List[float],
            "average_session_per_application": List[int],
            "servicer_jailing_probability": List[float],
            "uses_gateway_probability": List[float],
            "applications_use_min_servicers": List[int],
            "applications_use_max_servicers": List[int],
            "lambda_ewm_revenue_expectation": List[float],
            "service_linking_probability_normal": List[float],
            "service_linking_probability_just_joined": List[float],
            "kick_bottom_probability": List[float],
            "oracle_price_kde_bandwidth": List[float],
            "oracle_price_interarrival_time_flag": List[int],
        },
    ),
)
FunctionalParamsType = NewType(
    "FunctionalParams",
    TypedDict(
        "Functional Params",
        {
            "application_join_function": List[Literal["simple_unfiform"]],
            "servicer_join_function": List[Literal["simple_unfiform"]],
            "service_join_function": List[Literal["simple_unfiform"]],
            "gateway_join_function": List[Literal["simple_unfiform"]],
            "service_linking_function": List[Literal["test", "basic"]],
            "gateway_delegation_function": List[Literal["test", "basic"]],
            "relay_requests_function": List[Literal["test"]],
            "submit_relay_requests_function": List[Literal["test", "basic_gamma", "app_looper_test"]],
            "submit_relay_requests_policy_function": List[Literal["test", "V1"]],
            "application_leave_function": List[Literal["basic"]],
            "service_leave_function": List[Literal["basic"]],
            "servicer_leave_function": List[Literal["basic"]],
            "gateway_leave_function": List[Literal["basic"]],
            "service_unlinking_function": List[Literal["basic"]],
            "gateway_undelegation_function": List[Literal["basic"]],
            "servicer_stake_function": List[Literal["basic"]],
            "application_stake_function": List[Literal["basic"]],
            "jailing_function": List[Literal["basic"]],
            "gateway_stake_function": List[Literal["basic"]],
        },
    ),
)

ParamType = NewType(
    "Params",
    TypedDict(
        "Params",
        {
            "minimum_stake_servicer": List[POKTType],
            "minimum_stake_period_servicer": List[int],
            "minimum_pause_time": List[int],
            "max_chains_servicer": List[int],
            "relays_to_tokens_multiplier": List[POKTType],
            "slash_fraction_downtime": List[PercentType],
            "downtime_jail_duration": List[NanoSecondsType],
            "minimum_servicers_per_session": List[int],
            "maximum_servicers_per_session": List[int],
            "application_fee_per_relay": List[POKTType],
            "minimum_application_stake": List[POKTType],
            "app_burn_per_session": List[POKTType],
            "app_burn_per_relay": List[POKTType],
            "block_proposer_allocation": List[PercentType],
            "dao_allocation": List[PercentType],
            "servicer_allocation": List[PercentType],
            "stake_per_app_delegation": List[POKTType],
            "gateway_fee_per_relay": List[POKTType],
            "gateway_minimum_stake": List[POKTType],
            "session_token_bucket_coefficient": List[int],
            "dao_fee_percentage": List[PercentType],
            "validator_fee_percentage": List[PercentType],
            "transaction_fee": List[PercentType],
            "application_max_number": List[int],
            "servicer_max_number": List[int],
            "service_max_number": List[int],
            "gateway_max_number": List[int],
            "service_max_number_link": List[int],
            "application_leave_probability": List[float],
            "gateway_leave_probability": List[float],
            "service_leave_probability": List[float],
            "servicer_leave_probability": List[float],
            "service_unlinking_probability": List[float],
            "gateway_undelegation_probability": List[float],
            "relays_per_session_gamma_distribution_shape": List[float],
            "relays_per_session_gamma_distribution_scale": List[float],
            "average_session_per_application": List[int],
            "servicer_jailing_probability": List[float],
            "uses_gateway_probability": List[float],
            "applications_use_min_servicers": List[int],
            "applications_use_max_servicers": List[int],
            "lambda_ewm_revenue_expectation": List[float],
            "service_linking_probability_normal": List[float],
            "service_linking_probability_just_joined": List[float],
            "kick_bottom_probability": List[float],
            "oracle_price_kde_bandwidth": List[float],
            "oracle_price_interarrival_time_flag": List[int],
            "application_join_function": List[Literal["simple_unfiform"]],
            "servicer_join_function": List[Literal["simple_unfiform"]],
            "service_join_function": List[Literal["simple_unfiform"]],
            "gateway_join_function": List[Literal["simple_unfiform"]],
            "service_linking_function": List[Literal["test", "basic"]],
            "gateway_delegation_function": List[Literal["test", "basic"]],
            "relay_requests_function": List[Literal["test"]],
            "submit_relay_requests_function": List[Literal["test", "basic_gamma", "app_looper_test"]],
            "submit_relay_requests_policy_function": List[Literal["test", "V1"]],
            "application_leave_function": List[Literal["basic"]],
            "service_leave_function": List[Literal["basic"]],
            "servicer_leave_function": List[Literal["basic"]],
            "gateway_leave_function": List[Literal["basic"]],
            "service_unlinking_function": List[Literal["basic"]],
            "gateway_undelegation_function": List[Literal["basic"]],
            "servicer_stake_function": List[Literal["basic"]],
            "application_stake_function": List[Literal["basic"]],
            "jailing_function": List[Literal["basic"]],
            "gateway_stake_function": List[Literal["basic"]],
        },
    ),
)
