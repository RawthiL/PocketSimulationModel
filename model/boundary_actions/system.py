from ..types import StateType, ParamType
from ..spaces import distribute_fees_space, mint_block_rewards_space
from typing import Tuple, List


def fee_reward_ba(state: StateType, params: ParamType) -> Tuple[distribute_fees_space]:
    return ({"current_height": state["height"]},)


def block_reward_ba(
    state: StateType, params: ParamType
) -> List[Tuple[mint_block_rewards_space]]:
    '''
    Reads the "relay_log" from the estate and creates a list containing all 
    relevant information for rewards distribution.
    '''
    out = []
    for key in state["relay_log"]:
        out.append(
            (
                {
                    "block_producer": state["Validators"][0],
                    "geo_zone": key[1],
                    "service": key[0],
                    "application": key[2],
                    "relays": state["relay_log"][key],
                },
            )
        )


    return out
