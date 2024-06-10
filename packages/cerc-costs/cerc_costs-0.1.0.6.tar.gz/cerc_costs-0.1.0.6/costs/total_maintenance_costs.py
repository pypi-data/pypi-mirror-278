"""
Total maintenance costs module
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


class TotalMaintenanceCosts(CostBase):
  """
  Total maintenance costs class
  """
  def __init__(self, building: Building, configuration: Configuration):
    super().__init__(building, configuration)
    self._yearly_maintenance_costs = pd.DataFrame(
      index=self._rng,
      columns=[
        'Heating_maintenance',
        'Cooling_maintenance',
        'PV_maintenance'
      ],
      dtype='float'
    )

  def calculate(self) -> pd.DataFrame:
    """
    Calculate total maintenance costs
    :return: pd.DataFrame
    """
    building = self._building
    archetype = self._archetype
    # todo: change area pv when the variable exists
    roof_area = 0
    for roof in building.roofs:
      roof_area += roof.solid_polygon.area
    surface_pv = roof_area * 0.5

    peak_heating = building.heating_peak_load[cte.YEAR][0]
    peak_cooling = building.cooling_peak_load[cte.YEAR][0]

    maintenance_heating_0 = peak_heating * archetype.operational_cost.maintenance_heating
    maintenance_cooling_0 = peak_cooling * archetype.operational_cost.maintenance_cooling
    maintenance_pv_0 = surface_pv * archetype.operational_cost.maintenance_pv

    for year in range(1, self._configuration.number_of_years + 1):
      costs_increase = math.pow(1 + self._configuration.consumer_price_index, year)
      self._yearly_maintenance_costs.loc[year, 'Heating_maintenance'] = (
          maintenance_heating_0 * costs_increase
      )
      self._yearly_maintenance_costs.loc[year, 'Cooling_maintenance'] = (
          maintenance_cooling_0 * costs_increase
      )
      self._yearly_maintenance_costs.loc[year, 'PV_maintenance'] = (
          maintenance_pv_0 * costs_increase
      )
    self._yearly_maintenance_costs.fillna(0, inplace=True)
    return self._yearly_maintenance_costs
