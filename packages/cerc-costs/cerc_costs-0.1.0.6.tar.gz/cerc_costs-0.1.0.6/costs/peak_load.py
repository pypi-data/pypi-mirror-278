"""
Peak load module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""

import pandas as pd

import hub.helpers.constants as cte


class PeakLoad:
  """
  Peak load class
  """

  def __init__(self, building):
    self._building = building

  @property
  def electricity_peak_load(self):
    """
    Get the electricity peak load in W
    """
    array = [None] * 12
    heating = 0
    cooling = 0
    for system in self._building.energy_systems:
      if cte.HEATING in system.demand_types:
        heating = 1
      if cte.COOLING in system.demand_types:
        cooling = 1
    if cte.MONTH in self._building.heating_peak_load.keys() and cte.MONTH in self._building.cooling_peak_load.keys():
      peak_lighting = self._building.lighting_peak_load[cte.YEAR][0]
      peak_appliances = self._building.appliances_peak_load[cte.YEAR][0]
      monthly_electricity_peak = [0.9 * peak_lighting + 0.7 * peak_appliances] * 12
      conditioning_peak = max(self._building.heating_peak_load[cte.MONTH], self._building.cooling_peak_load[cte.MONTH])
      for i in range(len(conditioning_peak)):
        if cooling == 1 and heating == 1:
          conditioning_peak[i] = conditioning_peak[i]
          continue
        elif cooling == 0:
          conditioning_peak[i] = self._building.heating_peak_load[cte.MONTH][i] * heating
        else:
          conditioning_peak[i] = self._building.cooling_peak_load[cte.MONTH][i] * cooling
        monthly_electricity_peak[i] += 0.8 * conditioning_peak[i]

      electricity_peak_load_results = pd.DataFrame(
        monthly_electricity_peak,
        columns=[f'electricity peak load W']
      )
    else:
      electricity_peak_load_results = pd.DataFrame(array, columns=[f'electricity peak load W'])
    return electricity_peak_load_results
