"""
Total operational costs module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
import math
import pandas as pd

from hub.city_model_structure.building import Building
import hub.helpers.constants as cte

from costs.configuration import Configuration
from costs.cost_base import CostBase
from costs.peak_load import PeakLoad


class TotalOperationalCosts(CostBase):
  """
  End of life costs class
  """

  def __init__(self, building: Building, configuration: Configuration):
    super().__init__(building, configuration)
    self._yearly_operational_costs = pd.DataFrame(
      index=self._rng,
      columns=[
        'Fixed_costs_electricity_peak',
        'Fixed_costs_electricity_monthly',
        'Variable_costs_electricity',
        'Fixed_costs_gas',
        'Variable_costs_gas'
      ],
      dtype='float'
    )

  def calculate(self) -> pd.DataFrame:
    """
    Calculate total operational costs
    :return: pd.DataFrame
    """
    building = self._building
    archetype = self._archetype
    total_floor_area = self._total_floor_area
    factor_residential = total_floor_area / 80
    # todo: split the heating between fuels
    fixed_gas_cost_year_0 = 0
    variable_gas_cost_year_0 = 0
    electricity_heating = 0
    domestic_hot_water_electricity = 0
    # todo: each fuel has different units that have to be processed
    if self._configuration.fuel_type == 1:
      fixed_gas_cost_year_0 = archetype.operational_cost.fuels[1].fixed_monthly * 12 * factor_residential
      variable_gas_cost_year_0 = (
          (building.heating_consumption[cte.YEAR][0] + building.domestic_hot_water_consumption[cte.YEAR][0])
          / (1000 * cte.WATTS_HOUR_TO_JULES) * archetype.operational_cost.fuels[1].variable[0]
      )
    if self._configuration.fuel_type == 0:
      electricity_heating = building.heating_consumption[cte.YEAR][0] / 1000
      domestic_hot_water_electricity = building.domestic_hot_water_consumption[cte.YEAR][0] / 1000

    electricity_cooling = building.cooling_consumption[cte.YEAR][0] / 1000
    electricity_lighting = building.lighting_electrical_demand[cte.YEAR][0] / 1000
    electricity_plug_loads = building.appliances_electrical_demand[cte.YEAR][0] / 1000
    electricity_distribution = 0
    total_electricity_consumption = (
        electricity_heating + electricity_cooling + electricity_lighting + domestic_hot_water_electricity +
        electricity_plug_loads + electricity_distribution
    )

    # todo: change when peak electricity demand is coded. Careful with factor residential
    peak_electricity_load = PeakLoad(building).electricity_peak_load
    peak_load_value = peak_electricity_load.max(axis=1)
    peak_electricity_demand = peak_load_value[1] / 1000  # self._peak_electricity_demand adapted to kW
    variable_electricity_cost_year_0 = (
      total_electricity_consumption / cte.WATTS_HOUR_TO_JULES * archetype.operational_cost.fuels[0].variable[0]
    )
    peak_electricity_cost_year_0 = peak_electricity_demand * archetype.operational_cost.fuels[0].fixed_power * 12
    monthly_electricity_cost_year_0 = archetype.operational_cost.fuels[0].fixed_monthly * 12 * factor_residential

    for year in range(1, self._configuration.number_of_years + 1):
      price_increase_electricity = math.pow(1 + self._configuration.electricity_price_index, year)
      price_increase_peak_electricity = math.pow(1 + self._configuration.electricity_peak_index, year)
      price_increase_gas = math.pow(1 + self._configuration.gas_price_index, year)
      self._yearly_operational_costs.at[year, 'Fixed_costs_electricity_peak'] = (
          peak_electricity_cost_year_0 * price_increase_peak_electricity
      )
      self._yearly_operational_costs.at[year, 'Fixed_costs_electricity_monthly'] = (
          monthly_electricity_cost_year_0 * price_increase_peak_electricity
      )
      if not isinstance(variable_electricity_cost_year_0, pd.DataFrame):
        variable_costs_electricity = variable_electricity_cost_year_0 * price_increase_electricity
      else:
        variable_costs_electricity = float(variable_electricity_cost_year_0.iloc[0] * price_increase_electricity)
      self._yearly_operational_costs.at[year, 'Variable_costs_electricity'] = (
        variable_costs_electricity
      )
      self._yearly_operational_costs.at[year, 'Fixed_costs_gas'] = fixed_gas_cost_year_0 * price_increase_gas
      self._yearly_operational_costs.at[year, 'Variable_costs_gas'] = (
          variable_gas_cost_year_0 * price_increase_peak_electricity
      )
      self._yearly_operational_costs.at[year, 'Variable_costs_gas'] = (
          variable_gas_cost_year_0 * price_increase_peak_electricity
      )
    self._yearly_operational_costs.fillna(0, inplace=True)
    return self._yearly_operational_costs
