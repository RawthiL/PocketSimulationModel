import numpy as np
from datetime import datetime


def p_update_time(_params, substep, state_history, state) -> dict:
    if state["timestep"] == 1:
        print(datetime.now())
    if _params['granularity'] == 'day':
        return {
            "height": state["height"] + int(24*60/15),
            "day": state["day"] + 1,
        }
    elif _params['granularity'] == 'session':
        return {
            "height": state["height"] + 4,
            "day": int(state["height"]//(24*60/15)),
        }
    else:
        raise ValueError("Time step granularity \"%s\" not supported"% state['granularity'])


def s_update_height(_params, substep, state_history, state, _input) -> tuple:
    return ("height", _input["height"])


def s_update_day(_params, substep, state_history, state, _input) -> tuple:
    return ("day", _input["day"])


def p_transactions(_params, substep, state_history, state) -> dict:
    n_transactions = int(
        36692.90516650191 + 0.8457022264621301 * state["processed_relays"]
    )
    return {"n_transactions": n_transactions}


def s_update_n_transactions(_params, substep, state_history, state, _input) -> tuple:
    return ("n_transactions", _input["n_transactions"])


def s_update_relay_log(_params, substep, state_history, state, _input) -> tuple:
    return ("relay_log", _input["relay_log"])


def s_update_servicer_relay_log(
    _params, substep, state_history, state, _input
) -> tuple:
    return ("servicer_relay_log", _input["servicer_relay_log"])


def s_set_to_zero_pokt_burned(_params, substep, state_history, state, _input) -> tuple:
    return ("POKT_burned", 0)


def s_set_to_zero_pokt_minted(_params, substep, state_history, state, _input) -> tuple:
    return ("POKT_minted", 0)


def s_set_to_zero_slashing_cost(
    _params, substep, state_history, state, _input
) -> tuple:
    return ("period_slashing_costs", 0)


def s_set_to_zero_jail_cost(_params, substep, state_history, state, _input) -> tuple:
    return ("period_jailing_opportunity_cost", 0)
