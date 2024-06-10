"""
Total operational incomes module
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


class TotalOperationalIncomes(CostBase):
  """
  Total operational incomes class
  """
  def __init__(self, building: Building, configuration: Configuration):
    super().__init__(building, configuration)
    self._yearly_operational_incomes = pd.DataFrame(index=self._rng, columns=['Incomes electricity'], dtype='float')

  def calculate(self) -> pd.DataFrame:
    """
    Calculate total operational incomes
    :return: pd.DataFrame
    """
    building = self._building
    archetype = self._archetype
    if cte.YEAR not in building.onsite_electrical_production:
      onsite_electricity_production = 0
    else:
      onsite_electricity_production = building.onsite_electrical_production[cte.YEAR][0]

    for year in range(1, self._configuration.number_of_years + 1):
      price_increase_electricity = math.pow(1 + self._configuration.electricity_price_index, year)
      # todo: check the adequate assignation of price. Pilar
      price_export = archetype.income.electricity_export * cte.WATTS_HOUR_TO_JULES * 1000  # to account for unit change
      self._yearly_operational_incomes.loc[year, 'Incomes electricity'] = (
          onsite_electricity_production * price_export * price_increase_electricity
      )

    self._yearly_operational_incomes.fillna(0, inplace=True)
    return self._yearly_operational_incomes
