from ..types import StateType, ParamType
from ..spaces import (
    distribute_fees_space,
    decrease_relay_fees_space,
    modify_validator_pokt_space,
    modify_dao_pokt_space,
    mint_block_rewards_space,
    assign_servicer_salary_space,
    mint_pokt_mechanism_space,
    validator_block_reward_space,
    dao_block_reward_space,
    modify_servicer_pokt_space,
    burn_pokt_mechanism_space,
)
from typing import Tuple, List
from math import isclose


def fee_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[distribute_fees_space]
) -> Tuple[List[modify_validator_pokt_space], modify_dao_pokt_space]:
    accumulated_fees = state["n_transactions"] * params["transaction_fee"]
    validator_share = accumulated_fees * params["validator_fee_percentage"]
    dao_share = accumulated_fees * params["dao_fee_percentage"]
    assert isclose(accumulated_fees, validator_share + dao_share)

    # space1: decrease_relay_fees_space = {"POKT Amount": accumulated_fees}
    space1: List[modify_validator_pokt_space] = [
        ({"public_key": state["Validators"][0], "amount": validator_share},)
    ]
    space2: modify_dao_pokt_space = {"amount": dao_share}

    return (space1, space2)


def block_reward_policy_aggregate(
    state: StateType, params: ParamType, domain: Tuple[mint_block_rewards_space]
) -> Tuple[
    assign_servicer_salary_space,
    mint_pokt_mechanism_space,
    validator_block_reward_space,
    dao_block_reward_space,
]:
    '''
    This function takes the data from the block rewards and calculates the total 
    amount of POKT minted per geozone and servicer for all actors:
    - Servicer
    - Validators
    - DAO
    '''
    space = domain[0]

    # Calculate the total reward as the total number of relays times the RTTM
    # TODO : Add service weight here
    reward = int(space["relays"][0] * state["relays_to_tokens_multiplier"])

    # Calculate the servicer allocation as the total minus the validators and DAO shares
    servicer_allocation = (
        1 - params["block_proposer_allocation"] - params["dao_allocation"]
    )
    # Create servicers salary space
    space1: assign_servicer_salary_space = {
        "geo_zone": space["geo_zone"],
        "reward": reward * servicer_allocation,
        "service": space["service"],
        "servicers": space["relays"][1],
    }
    # Create space to keep track of POKT mining
    space2: mint_pokt_mechanism_space = {"mint_amount": reward}
    # Create validators block reward space
    space3: validator_block_reward_space = {
        "public_key": space["block_producer"],
        "reward_amount": reward * params["block_proposer_allocation"],
    }
    # Create DAO rewards
    space4: dao_block_reward_space = {
        "reward_amount": reward * params["dao_allocation"]
    }

    assert isclose(
        space1["reward"] + space3["reward_amount"] + space4["reward_amount"], reward
    )

    return (space1, space2, space3, space4)


def assign_servicer_salary_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[assign_servicer_salary_space],
    servicer_earnings,
) -> List[Tuple[modify_servicer_pokt_space, burn_pokt_mechanism_space]]:
    '''
    Mint the salary to each servicer on the list of servicers. The input space contains:
    - reward : Total POKT to be distributed
    - servicers : List of servicers
    - geo_zone : Used to track income origin
    - service : Used to track income origin
    '''
    # Get the space data 
    space = domain[0]
    # Get the service being used
    service = space["service"]
    # servicers = service.servicers
    # Get actual servicers used in the session
    servicers = space["servicers"]

    geo_servicers = [
        x for x in servicers if x.geo_zone == space["geo_zone"] and not x.pause_height
    ]
    if len(geo_servicers) > 0:
        servicers = geo_servicers
    # This is probably a bad failsafe
    if len(geo_servicers) == 0:
        servicers = [x for x in state["Servicers"] if not x.pause_height]
    out = []

    # Stake buckets
    # Each servicer's stake is mapped to one of 4 buckets of 15K increments that denotes their reward share
    stake_bins = [max(1, min(x.staked_pokt // 15000000000, 4)) for x in servicers]

    # Split the reward evenly among all servicers
    payment_per = space["reward"] // sum(stake_bins)
    for servicer, sb in zip(servicers, stake_bins):
        if servicer not in servicer_earnings:
            servicer_earnings[servicer] = {}
        if service not in servicer_earnings[servicer]:
            servicer_earnings[servicer][service] = int(payment_per * sb)
        else:
            servicer_earnings[servicer][service] += int(payment_per * sb)

        space1: modify_servicer_pokt_space = {
            "amount": payment_per * servicer.QoS,
            "public_key": servicer,
        }
        space2: burn_pokt_mechanism_space = {
            "burn_amount": payment_per * (1 - servicer.QoS)
        }
        out.append((space1, space2))
    return out


def validator_block_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[validator_block_reward_space]
) -> Tuple[modify_validator_pokt_space]:
    out: modify_validator_pokt_space = {
        "amount": domain[0]["reward_amount"],
        "public_key": domain[0]["public_key"],
    }
    return (out,)


def dao_block_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[dao_block_reward_space]
) -> Tuple[modify_dao_pokt_space]:
    out: modify_dao_pokt_space = {"amount": domain[0]["reward_amount"]}
    return (out,)
