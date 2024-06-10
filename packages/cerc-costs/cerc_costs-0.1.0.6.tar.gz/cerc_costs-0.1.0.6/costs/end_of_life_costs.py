"""
End of life costs module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
import math
import pandas as pd
from hub.city_model_structure.building import Building

from costs.configuration import Configuration
from costs.cost_base import CostBase


class EndOfLifeCosts(CostBase):
  """
  End of life costs class
  """
  def __init__(self, building: Building, configuration: Configuration):
    super().__init__(building, configuration)
    self._yearly_end_of_life_costs = pd.DataFrame(index=self._rng, columns=['End_of_life_costs'], dtype='float')

  def calculate(self):
    """
    Calculate end of life costs
    :return: pd.DataFrame
    """
    archetype = self._archetype
    total_floor_area = self._total_floor_area
    for year in range(1, self._configuration.number_of_years + 1):
      price_increase = math.pow(1 + self._configuration.consumer_price_index, year)
      if year == self._configuration.number_of_years:
        self._yearly_end_of_life_costs.at[year, 'End_of_life_costs'] = (
            total_floor_area * archetype.end_of_life_cost * price_increase
        )
    self._yearly_end_of_life_costs.fillna(0, inplace=True)
    return self._yearly_end_of_life_costs
