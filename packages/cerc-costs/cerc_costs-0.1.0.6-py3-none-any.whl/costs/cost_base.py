"""
Cost base module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""

from hub.city_model_structure.building import Building

from costs.configuration import Configuration


class CostBase:
  """
  Abstract base class for the costs
  """
  def __init__(self, building: Building, configuration: Configuration):
    self._building = building
    self._configuration = configuration
    self._total_floor_area = 0
    for thermal_zone in building.thermal_zones_from_internal_zones:
      self._total_floor_area += thermal_zone.total_floor_area
    self._archetype = None
    self._capital_costs_chapter = None
    for archetype in self._configuration.costs_catalog.entries().archetypes:
      if configuration.dictionary[str(building.function)] == str(archetype.function):
        self._archetype = archetype
        self._capital_costs_chapter = self._archetype.capital_cost
        break
    if not self._archetype:
      raise KeyError(f'archetype not found for function {building.function}')

    self._rng = range(configuration.number_of_years)

  def calculate(self):
    """
    Raises not implemented exception
    """
    raise NotImplementedError()
