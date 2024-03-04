from ..boundary_actions import (
    servicer_join_ba,
    relay_requests_ba,
    submit_relay_requests_ba,
    servicer_leave_ba,
    servicer_stake_ba,
    jailing_ba,
    unjailing_ba,
)
from ..policy import (
    servicer_join_policy,
    submit_relay_requests_policy,
    servicer_relay_policy,
    servicer_leave_policy,
    servicer_stake_policy,
    jail_node_policy,
    unjail_policy,
)
from ..mechanisms import (
    add_servicer,
    create_new_session,
    modify_gateway_stake,
    modify_application_stake,
    increase_relay_fees,
    modify_servicer_pokt_holdings,
    remove_session,
    unlink_service_mechanism,
    remove_servicer,
    modify_servicer_stake,
    servicer_update_pause_height,
    burn_pokt_mechanism,
)
from ..spaces import modify_gateway_pokt_space
from ..classes import Gateway


def servicer_join_ac(state, params):
    spaces = servicer_join_ba(state, params)
    if spaces[0]:
        spaces = servicer_join_policy(state, params, spaces)
    else:
        return
    if spaces[0]:
        add_servicer(state, params, spaces)
    else:
        return


def relay_requests_ac(state, params, relay_log, servicer_relay_log, idx):
    out = {}
    # Submit request
    spaces = submit_relay_requests_ba(state, params, idx)
    spaces = submit_relay_requests_policy(state, params, spaces)
    out["total_relays"] = spaces[0]["session"]["number_of_relays"]

    if spaces[0]["session"]["number_of_relays"] == 0:
        out["processed_relays"] = 0
        return out

    # If service is shutdown then no relays can go through
    if spaces[0]["session"]["service"].shutdown:
        out["processed_relays"] = 0
        return out

    create_new_session(state, params, spaces[:1])

    # spaces = burn_per_session_policy(state, params, spaces)
    # burn_pokt_mechanism(state, params, spaces[:1])
    # modify_application_stake(state, params, spaces[1:])

    # Relay the request
    spaces = relay_requests_ba(state, params)
    spaces = servicer_relay_policy(state, params, spaces, relay_log, servicer_relay_log)
    out["processed_relays"] = spaces[-1]["session"]["number_of_relays"]
    if type(spaces[0]["public_key"]) == Gateway:
        # Track the fees paid
        spaces[0]["public_key"].fees_paid += -spaces[0]["amount"]
        spaces[0]["public_key"].relays_served += spaces[-1]["session"][
            "number_of_relays"
        ]
        modify_gateway_stake(state, params, spaces[:1])
    else:
        modify_application_stake(state, params, spaces[:1])
    # spaces2 = burn_per_relay_policy(state, params, spaces[1:2])
    # burn_pokt_mechanism(state, params, spaces2[:1])
    # modify_application_stake(state, params, spaces2[1:])
    if spaces[2]:
        remove_session(state, params, spaces[2:3])

    return out


def servicer_leave_ac(state, params):
    spaces = servicer_leave_ba(state, params)
    spaces = servicer_leave_policy(state, params, spaces)

    for spaces_i in spaces[0]:
        unlink_service_mechanism(state, params, spaces_i)
    for spaces_i in spaces[1]:
        remove_servicer(state, params, spaces_i)


def servicers_stake_ac(state, params):
    spaces = servicer_stake_ba(state, params)
    for spaces_i in spaces:
        spaces_i = servicer_stake_policy(state, params, spaces_i)
        modify_servicer_pokt_holdings(state, params, spaces_i[:1])
        modify_servicer_stake(state, params, spaces_i[1:])


def jailing_slashing_ac(state, params):
    # Any of the unjailing stuff
    spaces = unjailing_ba(state, params)
    for spaces_i in spaces:
        spaces_i = unjail_policy(state, params, spaces_i)
        if spaces_i[0]:
            servicer_update_pause_height(state, params, spaces_i)

    # Jailing
    spaces = jailing_ba(state, params)
    for spaces_i in spaces:
        spaces_i = jail_node_policy(state, params, spaces_i)
        servicer_update_pause_height(state, params, spaces_i[:1])
        # Keep track of burned stake from slashing

        # state["period_slashing_costs"] += -spaces_i[1]["amount"]
        spaces_i[1]["public_key"].slashing_from_jailing_history[state["height"]] = (
            spaces_i[1]["amount"]
        )
        spaces_i[1]["public_key"].slashing_history[state["height"]] = spaces_i[1][
            "amount"
        ]
        modify_servicer_stake(state, params, spaces_i[1:2])
        burn_pokt_mechanism(state, params, spaces_i[2:3])
