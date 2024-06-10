# Cerc costs 

Uses the cerc-hub as a base for cost calculation, it's intended to be used after executing the complete monthly energy
balance workflow called building by building

This module processes the object-oriented generalization to be used the cost workflow

# installation

> $ pip install cerc-cost

# usage

> from costs.cost import Cost
>
> Cost(building, retrofit_scenario=[scenario]>).life_cycle
> 

The available scenarios are defined in the constant class as an enum

> # constants
> CURRENT_STATUS = 0
> 
> SKIN_RETROFIT = 1
> 
> SYSTEM_RETROFIT_AND_PV = 2
> 
> SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV = 3
> 
> RETROFITTING_SCENARIOS = [CURRENT_STATUS, SKIN_RETROFIT, SYSTEM_RETROFIT_AND_PV, SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV]
>
