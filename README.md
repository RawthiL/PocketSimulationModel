# Pocket Network Simulation Model

## Summary

The enclosed repository serves as a simulation model for testing economic scenarios related to the Pocket Network. It is built off cadCAD under the hood.

## Model Background

This model is the next step in the evolution from the [Pocket Math Spec](https://github.com/BlockScience/PocketMathSpec) which served as a foundational architecture document prior to development.

## Structure of the Model Repository

1. Exploratory Folder: All jupytyer notebooks being used to test and build the system
2. Model Folder
    - Action Chains: The code that pieces together the boundary actions, policies, and mechanisms
    - Boundary Actions, Policies, Mechanisms: All code which implements modular logic
    - Classes: The class definitions for entities used in the model
    - Spaces, Types: The annotations used for functions to make it more readable
    - PSUBs: The partial state update blocks that mostly are used as pass throughs to action chains
    - Config: The utility functions for setting up configurations as well as options for starting state + parameter sets

## Partial State Update Blocks

The following are the partial state update blocks which as a whole represent one timestep in the system. The current timestep is one day. Hence T = 365 in the scenario running would mean 365 days. 

1. Meta Update Block: Updates the time in the system, the price (true and oracle) for POKT in USD, simulates the number of transactions on the network, and sets certain timestep tracking variables to 0
2. Join Block: All logic around servicers, services, gateways, and applications joining.
3. Stake Block: Any logic for staking that happens in the system.
4. Delegation and Service Linking Block: Block which takes care of applications delegating to gateways and servicers linking to services.
5. Relay Request Block: All logic around requests being created and relayed, recording of relays in different groups is also recorded.
6. Jailing & Slashing Block: Block for servicers or gateways being slashed or jailed as well as the inverse actions + penalties.
7. Block & Fee Rewards Block: The logic for both the block rewards as well as the fee rewards.
8. Undelegation & Unservice Block: The block which handles any gateways undelegating or any services being unlinked from.
9. Leave Block: All logic around servicers, services, gateways, and applications leaving. There is also a substep to check which nodes might be understaked and kick certain ones from the system depending on the policy.

## Running Simulations

### run_experiments

To run pre-packaged simulations, import run_experiments and then pass a list of experiment keys like so:

    from model import run_experiments
    df = run_experiments(["test1"])

### auto_run_sets

This option allows for running sets in chunks, saving down the results as CSV files, and picking up where last started off. The chunk size determines how many simulations to run at a time

    from model import run_experiments
    df = auto_run_sets(["test1"], "Data", 10)

### Creating Simulation Configuration

Within model/config/experiment, the experimental_configs dictionary can be modified to add in different experiments. The structure of it is like so:

    experimental_setups = {
        "test1": {
            "config_option_state": "Test",
            "config_option_params": "Test",
            "monte_carlo_n": 1,
            "T": 365,
        }
    }

Where each key represents a set, the config_option_state refers to a specific starting state, config_option_params does the same for parameters, monte_carlo_n defines the number of monte carlo runs, and T defines the number of timesteps for the experiment.

Within model/config/params, the config_option_map is set up to handle the different options for creating parameter sweeps. More detail in the parameters section on specifics.

    config_option_map = {
        "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"}
    }

Likewise, within model/config/state, there is a config_option_map for the specific types of starting state assumptions to implement.

    config_option_map = {
        "Test": {
            "Geozones": "Test",
            "Applications": "Test",
            "DAO": "Test",
            "Gateways": "Test",
            "Services": "Test",
            "Servicers": "Test",
            "Validators": "Test",
        }
    }


## Parameters

Parameters are made from combining three subsets of parameters:

1. System Parameters: All parameters that would be present in the actual implementation
2. Behavior Parameters: All parameters used for assumptions in the model
3. Function Parameters: All parameters which decide functions for either:
    A. Behaviors in which case the functional parameters allow for experimenting with different classes of behavior (i.e. pulling from a random distribution or feeding in a specific signal that is meant to represent the randomness)
    B. Policies: This allows for A/B testing of different implementations of policies, i.e. if one wanted to test out different schemes of reward disbursement based on quality of service or other factors.

## State

The state can be seeded with different starting state representations so that for example one might test the impacts of starting with few servicers versus many.

## Cloud Running

- The container must be built with docker build . -t pocketsimulation --platform linux/x86_64
- To run one experiment locally do: docker run -t pocketsimulation Base
- To run two or more for example: docker run -t pocketsimulation Base test1

## Adaptive Grid Protocol

### Algorithm

1. Run the 30MC simulations with 2 sweep values (call them (x,y)) per protocol parameter
2. Post-processing for KPIs for this scenario
3. One PSuU round, assessing threshold inequalities to arrive at an interim “best” parameter constellation (this may be an ‘automated heuristic’)
4. Exogenous sweep values are not updated, and remain as they originally were. For each parameter, an expansion around either x or y, depending upon which was contained in the “best” constellation. This would be determined by either:
- standard interval defined from the previous parameter sweep values
- sensitivity analysis step to provide the next range
5. Re-run the simulation again with the new adaptive parameter grid (i.e. GOTO #1), until N loops are completed.

### Configuration Files

- For each sweep, there will be a suffix to the label like ag1, ag2, etc. to signify which iteration of the adaptive grid is being used.
- As research progress, adaptive grids will be created sequentially to store all configurations used in determining results