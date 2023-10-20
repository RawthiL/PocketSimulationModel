from ..boundary_actions import service_join_ba, service_linking_ba
from ..policy import service_join_policy, service_linking_policy
from ..mechanisms import add_service, link_service_mechanism


def service_join_ac(state, params):
    spaces = service_join_ba(state, params)
    if spaces[0]:
        spaces = service_join_policy(state, params, spaces)
    else:
        return
    add_service(state, params, spaces)

def service_linking_ac(state, params, servicer):
    spaces = service_linking_ba(state, params, servicer)
    for space in spaces:
        spaces_i = service_linking_policy(state, params, spaces_i)
        link_service_mechanism(spaces_i)