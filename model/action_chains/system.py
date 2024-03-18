from ..boundary_actions import fee_reward_ba, block_reward_ba
from ..policy import (
    fee_reward_policy,
    block_reward_policy_aggregate,
    assign_servicer_salary_policy,
    validator_block_reward_policy,
    dao_block_reward_policy,
)
from ..mechanisms import (
    decrease_relay_fees,
    modify_validator_pokt_holdings,
    modify_dao_pokt_holdings,
    modify_servicer_pokt_holdings,
    burn_pokt_mechanism,
    mint_pokt_mechanism,
)


def fee_reward_ac(state, params):
    spaces = fee_reward_ba(state, params)
    spaces = fee_reward_policy(state, params, spaces)
    for spaces_i in spaces[0]:
        modify_validator_pokt_holdings(state, params, spaces_i)
    modify_dao_pokt_holdings(state, params, spaces[1:2])


def update_revenue_expectations(state, params, servicer_earnings):
    lambda_ewm = params["lambda_ewm_revenue_expectation"]
    for servicer in state["Servicers"]:
        if servicer not in servicer_earnings:
            servicer_earnings[servicer] = {}
        last = servicer.revenue_expectations
        new = {}
        for service in servicer.services:
            val = servicer_earnings[servicer].get(service, 0)
            if service in last:
                new[service] = lambda_ewm * last[service] + (1 - lambda_ewm) * val
            else:
                new[service] = val
        servicer.revenue_expectations = new


def block_reward_ac(state, params):
    servicer_earnings = {}
    # Create one space per (service , geozone) tuple, with the total number of relays processed there
    spaces = block_reward_ba(state, params)
    # Loop all spaces, all (service , geozone) pairs
    for spaces_i in spaces:
        # Calculate, in order [servicers_rewards, total_minted, validator_rewards, dao_rewards]
        spaces_i = block_reward_policy_aggregate(state, params, spaces_i)
        # Update POKT supply and total minted
        mint_pokt_mechanism(state, params, spaces_i[1:2])
        # Mint rewards to all servicers, according their QoS and stake bin
        # Returns a list of each servicer updated with the amount and a list of all the pokt that was not minted due to QoS scores below 1.0 (this is regarded as additional burnt pokt).
        spaces_i2 = assign_servicer_salary_policy(
            state, params, spaces_i[:1], servicer_earnings
        )
        # For each of the servicers in the list
        for spaces_j in spaces_i2:
            # Update pokt holdings on servicers
            modify_servicer_pokt_holdings(state, params, spaces_j[:1])
            # Track total revenue
            spaces_j[0]["public_key"].total_revenues += spaces_j[0]["amount"]
            # Add burnt pokt to the list
            burn_pokt_mechanism(state, params, spaces_j[1:2])
        # Calculate the validators reward and update the holdings
        spaces_i3 = validator_block_reward_policy(state, params, spaces_i[2:3])
        modify_validator_pokt_holdings(state, params, spaces_i3)
        # Calculate the DAO reward and update the holdings
        spaces_i4 = dao_block_reward_policy(state, params, spaces_i[3:4])
        modify_dao_pokt_holdings(state, params, spaces_i4)
    # Calculate/update revenue expectations
    update_revenue_expectations(state, params, servicer_earnings)
