from ..types import StateType, ParamType, SessionType, ApplicationEntityType
from ..spaces import (
    application_join_space,
    application_entity_space,
    application_delegate_to_gateway_space,
    submit_relay_request_space,
    new_session_space,
    application_leave_space,
    application_undelegation_space,
    application_stake_space,
    modify_application_pokt_space,
)
from typing import Tuple, Union, Dict
from ..classes import Application
import random


def application_join_policy(
    state: StateType, params: ParamType, domain: Tuple[application_join_space]
) -> Tuple[Union[application_entity_space, None]]:
    space: application_join_space = domain[0]

    if space["stake_amount"] < params["minimum_application_stake"]:
        return (None,)

    uses_gateway = random.random() < params["uses_gateway_probability"]

    # Create entity
    application = Application(
        name=space["name"],
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
        services=[],
        geo_zone=space["geo_zone"],
        number_of_services=space["number_servicers"],
        stake_status="Staked",
        unstaking_height=None,
        delegate=None,
        uses_gateway=uses_gateway,
    )
    return ({"application": application},)


def gateway_delegation_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_gateway_space],
) -> Tuple[
    Union[application_delegate_to_gateway_space, None],
    Union[application_delegate_to_gateway_space, None],
]:
    space: application_delegate_to_gateway_space = domain[0]
    # Pass through

    return (space, space)


def submit_relay_requests_policy(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> Tuple[new_session_space, new_session_space]:
    if params["submit_relay_requests_policy_function"] == "test":
        return submit_relay_requests_policy_test(state, params, domain)
    elif params["submit_relay_requests_policy_function"] == "V1":
        return submit_relay_requests_policy_v1(state, params, domain)
    else:
        assert False, "Invalid submit_relay_requests_function"


def submit_relay_requests_policy_test(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> Tuple[new_session_space, new_session_space]:
    num_servicers = domain[0]["application_address"].number_of_services
    servicers = random.sample(
        [x for x in state["Servicers"] if not x.pause_height], num_servicers
    )
    service = random.choice(state["Services"])
    session: SessionType = {
        "application": domain[0]["application_address"],
        "fishermen": None,
        "geo_zone": domain[0]["application_address"].geo_zone,
        "id": None,
        "num_session_blocks": None,
        "service": service,
        "servicers": servicers,
        "session_height": None,
        "session_number": None,
        "number_of_relays": 10,
    }
    return ({"session": session}, {"session": session})


def submit_relay_requests_policy_v1(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> Tuple[new_session_space, new_session_space]:
    """During each Session, the amount of POKT an Application has staked is mapped to "Service Tokens" that represent 
    the amount of work a Servicer can provide using the SessionTokenBucketCoefficient governance parameter.

    The Token Bucket rate limiting algorithm is used to determine the maximum number of requests a Servicer can relay,
    and be rewarded for, thereby disincentivizing it to process relays for the Application once the cap is reached.

    At the beginning of the session, each Servicer initializes: 
        AppSessionTokens = (AppStakeAmount * SessionTokenBucketCoefficient) / NumServicersPerSession.

    When one of the Servicers in the session is out of session tokens, the Application can continue to use other 
    Servicers until every they are all exhausted.
    
    The mechanism described above enables future iterations of the protocol where different types of request may vary 
    the required number of AppSessionTokens per request. The selection of servicers is random but assigns higher
    probability for higher QoS servicers.
    """
    num_servicers = domain[0]["application_address"].number_of_services
    servicers = random.sample(state["Servicers"], num_servicers)
    service = random.choice(state["Services"])

    number_of_relays = domain[0]["number_of_relays"]
    if service in state["relay_multiplier"]:
        number_of_relays = number_of_relays * state["relay_multiplier"][service]

    max_relays_allowed = int(
        domain[0]["application_address"].staked_pokt
        * params["session_token_bucket_coefficient"]
    )
    number_of_relays = max(min(number_of_relays, max_relays_allowed), 0)

    # Check there is going to be enough money to pay!
    if domain[0]["application_address"].delegate:
        max_relays_allowed = (
            domain[0]["application_address"].delegate.staked_pokt
            // state["gateway_fee_per_relay"]
        )
    else:
        max_relays_allowed = (
            domain[0]["application_address"].staked_pokt
            // state["application_fee_per_relay"]
        )
    number_of_relays = max(min(number_of_relays, max_relays_allowed), 0)

    session: SessionType = {
        "application": domain[0]["application_address"],
        "fishermen": None,
        "geo_zone": domain[0]["application_address"].geo_zone,
        "id": None,
        "num_session_blocks": None,
        "service": service,
        "servicers": servicers,
        "session_height": None,
        "session_number": None,
        "number_of_relays": number_of_relays,
    }
    return ({"session": session}, {"session": session})


def application_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[application_leave_space]
) -> Tuple[
    Dict[ApplicationEntityType, Union[application_undelegation_space, None]],
    application_leave_space,
]:
    applications = domain[0]["applications"]
    space1: Dict[
        ApplicationEntityType, Union[application_undelegation_space, None]
    ] = {}
    space2 = domain[0]
    for application in applications:
        if applications[application]:
            if application.delegate:
                space1[application] = {
                    "application_public_key": application,
                    "gateway_public_key": application.delegate,
                }
            else:
                space1[application] = None
        else:
            space1[application] = None

    space2 = domain[0]

    return (space1, space2)


def gateway_undelegation_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_undelegation_space],
) -> Tuple[Union[application_undelegation_space, None],]:
    # Quick check
    if domain[0]["application_public_key"].delegate != domain[0]["gateway_public_key"]:
        return (None,)
    return domain


def application_stake_policy(
    state: StateType, params: ParamType, domain: Tuple[application_stake_space]
) -> Tuple[modify_application_pokt_space, modify_application_pokt_space]:
    application = domain[0]["public_key"]
    amount = domain[0]["stake_amount"]
    space1: modify_application_pokt_space = {
        "amount": -amount,
        "public_key": application,
    }
    space2: modify_application_pokt_space = {
        "amount": amount,
        "public_key": application,
    }
    return (space1, space2)
