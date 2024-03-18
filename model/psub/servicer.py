from ..action_chains import (
    servicer_join_ac,
    relay_requests_ac,
    servicer_leave_ac,
    servicers_stake_ac,
    jailing_slashing_ac,
)


def s_update_servicers(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Servicers", state["Servicers"])


def p_servicers_join(_params, substep, state_history, state) -> dict:
    servicer_join_ac(state, _params)
    return {}


def p_relay_requests(_params, substep, state_history, state) -> dict:
    # Calculate the number of sessions that we will be simulating
    number_relays = _params["average_session_per_application"] * len(
        state["Applications"]
    ) # for session granularity we use average_session_per_application=1 to loop over all apps
    
    # Keep track of total relays
    total_relays = 0
    processed_relays = 0
    # The relay log will contain how many relays were done and the list of servicers
    relay_log = {}
    # The servicer relays logs
    servicer_relay_log = {}
    for i in range(number_relays):
        out = relay_requests_ac(state, _params, relay_log, servicer_relay_log, i)
        total_relays += out["total_relays"]
        processed_relays += out["processed_relays"]

    # Assert that all relays were correctly assigned
    relay_log_sum = 0
    for relay, _ in relay_log.values():
        relay_log_sum += relay
    assert relay_log_sum == processed_relays
    assert sum(servicer_relay_log.values()) == processed_relays
    return {
        "total_relays": total_relays,
        "processed_relays": processed_relays,
        "relay_log": relay_log,
        "servicer_relay_log": servicer_relay_log,
    }


def p_jailing_slashing(_params, substep, state_history, state) -> dict:
    jailing_slashing_ac(state, _params)
    return {}


def p_servicers_leave(_params, substep, state_history, state) -> dict:
    servicer_leave_ac(state, _params)
    understaked_servicers = [
        x
        for x in state["Servicers"]
        if x.staked_pokt < _params["minimum_stake_servicer"]
    ]
    return {"understaked_servicers": understaked_servicers}


def p_servicers_stake(_params, substep, state_history, state) -> dict:
    servicers_stake_ac(state, _params)
    return {}


def s_update_understaked_servicers(
    _params, substep, state_history, state, _input
) -> tuple:
    return ("understaked_servicers", _input["understaked_servicers"])
