"""
Cost module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
import datetime

import pandas as pd
import numpy_financial as npf
from hub.city_model_structure.building import Building
from hub.helpers.dictionaries import Dictionaries

from costs.configuration import Configuration
from costs import CapitalCosts, EndOfLifeCosts, TotalMaintenanceCosts, TotalOperationalCosts, TotalOperationalIncomes
from costs.constants import CURRENT_STATUS


class Cost:
  """
  Cost class
  """

  def __init__(self,
               building: Building,
               number_of_years=31,
               percentage_credit=0,
               interest_rate=0.04,
               credit_years=15,
               consumer_price_index=0.04,
               electricity_peak_index=0.05,
               electricity_price_index=0.05,
               gas_price_index=0.05,
               discount_rate=0.03,
               retrofitting_year_construction=2020,
               factories_handler='montreal_custom',
               retrofit_scenario=CURRENT_STATUS,
               dictionary=None):
    if dictionary is None:
      dictionary = Dictionaries().hub_function_to_montreal_custom_costs_function
    self._building = building
    fuel_type = 0
    if "gas" in building.energy_systems_archetype_name:
      fuel_type = 1
    self._configuration = Configuration(number_of_years,
                                        percentage_credit,
                                        interest_rate, credit_years,
                                        consumer_price_index,
                                        electricity_peak_index,
                                        electricity_price_index,
                                        gas_price_index,
                                        discount_rate,
                                        retrofitting_year_construction,
                                        factories_handler,
                                        retrofit_scenario,
                                        fuel_type,
                                        dictionary)

  @property
  def building(self) -> Building:
    """
    Get current building.
    """
    return self._building

  def _npv_from_list(self, list_cashflow):
    return npf.npv(self._configuration.discount_rate, list_cashflow)

  @property
  def life_cycle(self) -> pd.DataFrame:
    """
    Get complete life cycle costs
    :return: DataFrame
    """
    results = pd.DataFrame()
    global_capital_costs, global_capital_incomes = CapitalCosts(self._building, self._configuration).calculate()
    global_end_of_life_costs = EndOfLifeCosts(self._building, self._configuration).calculate()
    global_operational_costs = TotalOperationalCosts(self._building, self._configuration).calculate()
    global_maintenance_costs = TotalMaintenanceCosts(self._building, self._configuration).calculate()
    global_operational_incomes = TotalOperationalIncomes(self._building, self._configuration).calculate()
    df_capital_costs_skin = (
        global_capital_costs['B2010_opaque_walls'] +
        global_capital_costs['B2020_transparent'] +
        global_capital_costs['B3010_opaque_roof'] +
        global_capital_costs['B10_superstructure']
    )
    df_capital_costs_systems = (
        global_capital_costs['D3020_heat_generating_systems'] +
        global_capital_costs['D3030_cooling_generation_systems'] +
        global_capital_costs['D3080_other_hvac_ahu'] +
        global_capital_costs['D5020_lighting_and_branch_wiring'] +
        global_capital_costs['D301010_photovoltaic_system']
    )

    df_end_of_life_costs = global_end_of_life_costs['End_of_life_costs']
    df_operational_costs = (
        global_operational_costs['Fixed_costs_electricity_peak'] +
        global_operational_costs['Fixed_costs_electricity_monthly'] +
        global_operational_costs['Variable_costs_electricity'] +
        global_operational_costs['Fixed_costs_gas'] +
        global_operational_costs['Variable_costs_gas']
    )
    df_maintenance_costs = (
        global_maintenance_costs['Heating_maintenance'] +
        global_maintenance_costs['Cooling_maintenance'] +
        global_maintenance_costs['PV_maintenance']
    )
    df_operational_incomes = global_operational_incomes['Incomes electricity']
    df_capital_incomes = (
        global_capital_incomes['Subsidies construction'] +
        global_capital_incomes['Subsidies HVAC'] +
        global_capital_incomes['Subsidies PV']
    )

    life_cycle_costs_capital_skin = self._npv_from_list(df_capital_costs_skin.values.tolist())
    life_cycle_costs_capital_systems = self._npv_from_list(df_capital_costs_systems.values.tolist())
    life_cycle_costs_end_of_life_costs = self._npv_from_list(df_end_of_life_costs.values.tolist())
    life_cycle_operational_costs = self._npv_from_list(df_operational_costs.values.tolist())
    life_cycle_maintenance_costs = self._npv_from_list(df_maintenance_costs.values.tolist())
    life_cycle_operational_incomes = self._npv_from_list(df_operational_incomes.values.tolist())
    life_cycle_capital_incomes = self._npv_from_list(df_capital_incomes.values.tolist())

    results[f'Scenario {self._configuration.retrofit_scenario}'] = [
      life_cycle_costs_capital_skin,
      life_cycle_costs_capital_systems,
      life_cycle_costs_end_of_life_costs,
      life_cycle_operational_costs,
      life_cycle_maintenance_costs,
      life_cycle_operational_incomes,
      life_cycle_capital_incomes,
      global_capital_costs,
      global_capital_incomes,
      global_end_of_life_costs,
      global_operational_costs,
      global_maintenance_costs,
      global_operational_incomes
    ]

    results.index = [
      'total_capital_costs_skin',
      'total_capital_costs_systems',
      'end_of_life_costs',
      'total_operational_costs',
      'total_maintenance_costs',
      'operational_incomes',
      'capital_incomes',
      'global_capital_costs',
      'global_capital_incomes',
      'global_end_of_life_costs',
      'global_operational_costs',
      'global_maintenance_costs',
      'global_operational_incomes'
    ]
    return results
