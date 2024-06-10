"""
Capital costs module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
import math

import pandas as pd
import numpy_financial as npf
from hub.city_model_structure.building import Building
import hub.helpers.constants as cte
from costs.configuration import Configuration
from costs.constants import SKIN_RETROFIT, SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV, SYSTEM_RETROFIT_AND_PV
from costs.cost_base import CostBase


class CapitalCosts(CostBase):
  """
  Capital costs class
  """
  def __init__(self, building: Building, configuration: Configuration):
    super().__init__(building, configuration)
    self._yearly_capital_costs = pd.DataFrame(
      index=self._rng,
      columns=[
        'B2010_opaque_walls',
        'B2020_transparent',
        'B3010_opaque_roof',
        'B10_superstructure',
        'D301010_photovoltaic_system',
        'D3020_heat_generating_systems',
        'D3030_cooling_generation_systems',
        'D3040_distribution_systems',
        'D3080_other_hvac_ahu',
        'D5020_lighting_and_branch_wiring'
      ],
      dtype='float'
    )
    self._yearly_capital_costs.loc[0, 'B2010_opaque_walls'] = 0
    self._yearly_capital_costs.loc[0, 'B2020_transparent'] = 0
    self._yearly_capital_costs.loc[0, 'B3010_opaque_roof'] = 0
    self._yearly_capital_costs.loc[0, 'B10_superstructure'] = 0
    self._yearly_capital_costs.loc[0, 'D3020_heat_generating_systems'] = 0
    self._yearly_capital_costs.loc[0, 'D3030_cooling_generation_systems'] = 0
    self._yearly_capital_costs.loc[0, 'D3040_distribution_systems'] = 0
    self._yearly_capital_costs.loc[0, 'D3080_other_hvac_ahu'] = 0
    self._yearly_capital_costs.loc[0, 'D5020_lighting_and_branch_wiring'] = 0

    self._yearly_capital_incomes = pd.DataFrame(
      index=self._rng,
      columns=[
        'Subsidies construction',
        'Subsidies HVAC',
        'Subsidies PV'
      ],
      dtype='float'
    )
    self._yearly_capital_incomes.loc[0, 'Subsidies construction'] = 0
    self._yearly_capital_incomes.loc[0, 'Subsidies HVAC'] = 0
    self._yearly_capital_incomes.loc[0, 'Subsidies PV'] = 0

  def calculate(self) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate capital cost
    :return: pd.DataFrame, pd.DataFrame
    """
    surface_opaque = 0
    surface_transparent = 0
    surface_roof = 0
    surface_ground = 0
    capital_cost_pv = 0
    capital_cost_opaque = 0
    capital_cost_ground = 0
    capital_cost_transparent = 0
    capital_cost_roof = 0
    capital_cost_heating_equipment = 0
    capital_cost_cooling_equipment = 0
    capital_cost_distribution_equipment = 0
    capital_cost_other_hvac_ahu = 0
    capital_cost_lighting = 0

    for thermal_zone in self._building.thermal_zones_from_internal_zones:
      for thermal_boundary in thermal_zone.thermal_boundaries:
        if thermal_boundary.type == 'Ground':
          surface_ground += thermal_boundary.opaque_area
        elif thermal_boundary.type == 'Roof':
          surface_roof += thermal_boundary.opaque_area
        elif thermal_boundary.type == 'Wall':
          surface_opaque += thermal_boundary.opaque_area * (1 - thermal_boundary.window_ratio)
          surface_transparent += thermal_boundary.opaque_area * thermal_boundary.window_ratio

    peak_heating = self._building.heating_peak_load[cte.YEAR][0] / 1000
    peak_cooling = self._building.cooling_peak_load[cte.YEAR][0] / 1000

    surface_pv = 0
    for roof in self._building.roofs:
      surface_pv += roof.solid_polygon.area * roof.solar_collectors_area_reduction_factor

    self._yearly_capital_costs.fillna(0, inplace=True)
    own_capital = 1 - self._configuration.percentage_credit
    if self._configuration.retrofit_scenario in (SKIN_RETROFIT, SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV):
      chapter = self._capital_costs_chapter.chapter('B_shell')
      capital_cost_opaque = surface_opaque * chapter.item('B2010_opaque_walls').refurbishment[0]
      capital_cost_transparent = surface_transparent * chapter.item('B2020_transparent').refurbishment[0]
      capital_cost_roof = surface_roof * chapter.item('B3010_opaque_roof').refurbishment[0]
      capital_cost_ground = surface_ground * chapter.item('B10_superstructure').refurbishment[0]
      self._yearly_capital_costs.loc[0, 'B2010_opaque_walls'] = capital_cost_opaque * own_capital
      self._yearly_capital_costs.loc[0, 'B2020_transparent'] = capital_cost_transparent * own_capital
      self._yearly_capital_costs.loc[0, 'B3010_opaque_roof'] = capital_cost_roof * own_capital
      self._yearly_capital_costs.loc[0, 'B10_superstructure'] = capital_cost_ground * own_capital

    if self._configuration.retrofit_scenario in (SYSTEM_RETROFIT_AND_PV, SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV):
      chapter = self._capital_costs_chapter.chapter('D_services')
      capital_cost_pv = surface_pv * chapter.item('D301010_photovoltaic_system').initial_investment[0]
      capital_cost_heating_equipment = peak_heating * chapter.item('D3020_heat_generating_systems').initial_investment[0]
      capital_cost_cooling_equipment = peak_cooling * chapter.item('D3030_cooling_generation_systems').initial_investment[0]
      capital_cost_distribution_equipment = peak_cooling * chapter.item('D3040_distribution_systems').initial_investment[0]
      capital_cost_other_hvac_ahu = peak_cooling * chapter.item('D3080_other_hvac_ahu').initial_investment[0]
      capital_cost_lighting = self._total_floor_area * chapter.item('D5020_lighting_and_branch_wiring').initial_investment[0]
      self._yearly_capital_costs.loc[0, 'D301010_photovoltaic_system'] = capital_cost_pv
      self._yearly_capital_costs.loc[0, 'D3020_heat_generating_systems'] = capital_cost_heating_equipment * own_capital
      self._yearly_capital_costs.loc[0, 'D3030_cooling_generation_systems'] = capital_cost_cooling_equipment * own_capital
      self._yearly_capital_costs.loc[0, 'D3040_distribution_systems'] = capital_cost_distribution_equipment * own_capital
      self._yearly_capital_costs.loc[0, 'D3080_other_hvac_ahu'] = capital_cost_other_hvac_ahu * own_capital
      self._yearly_capital_costs.loc[0, 'D5020_lighting_and_branch_wiring'] = capital_cost_lighting * own_capital

    for year in range(1, self._configuration.number_of_years):
      chapter = self._capital_costs_chapter.chapter('D_services')
      costs_increase = math.pow(1 + self._configuration.consumer_price_index, year)
      self._yearly_capital_costs.loc[year, 'B2010_opaque_walls'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_opaque * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'B2020_transparent'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_transparent * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'B3010_opaque_roof'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_roof * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'B10_superstructure'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_ground * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'D3020_heat_generating_systems'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_heating_equipment * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'D3030_cooling_generation_systems'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_cooling_equipment * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'D3040_distribution_systems'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_distribution_equipment * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'D3080_other_hvac_ahu'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_other_hvac_ahu * self._configuration.percentage_credit
        )
      )
      self._yearly_capital_costs.loc[year, 'D5020_lighting_and_branch_wiring'] = (
        -npf.pmt(
          self._configuration.interest_rate,
          self._configuration.credit_years,
          capital_cost_lighting * self._configuration.percentage_credit
        )
      )

      if (year % chapter.item('D3020_heat_generating_systems').lifetime) == 0:
        reposition_cost_heating_equipment = (
            peak_heating * chapter.item('D3020_heat_generating_systems').reposition[0] * costs_increase
        )
        self._yearly_capital_costs.loc[year, 'D3020_heat_generating_systems'] += reposition_cost_heating_equipment

      if (year % chapter.item('D3030_cooling_generation_systems').lifetime) == 0:
        reposition_cost_cooling_equipment = (
            peak_cooling * chapter.item('D3030_cooling_generation_systems').reposition[0] * costs_increase
        )
        self._yearly_capital_costs.loc[year, 'D3030_cooling_generation_systems'] += reposition_cost_cooling_equipment

      if (year % chapter.item('D3080_other_hvac_ahu').lifetime) == 0:
        reposition_cost_hvac_ahu = (
            peak_cooling * chapter.item('D3080_other_hvac_ahu').reposition[0] * costs_increase
        )
        self._yearly_capital_costs.loc[year, 'D3080_other_hvac_ahu'] = reposition_cost_hvac_ahu

      if (year % chapter.item('D5020_lighting_and_branch_wiring').lifetime) == 0:
        reposition_cost_lighting = (
            self._total_floor_area * chapter.item('D5020_lighting_and_branch_wiring').reposition[0] * costs_increase
        )
        self._yearly_capital_costs.loc[year, 'D5020_lighting_and_branch_wiring'] += reposition_cost_lighting

      if self._configuration.retrofit_scenario in (SYSTEM_RETROFIT_AND_PV, SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV):
        if (year % chapter.item('D301010_photovoltaic_system').lifetime) == 0:
          self._yearly_capital_costs.loc[year, 'D301010_photovoltaic_system'] += (
              surface_pv * chapter.item('D301010_photovoltaic_system').reposition[0] * costs_increase
          )
    capital_cost_skin = capital_cost_opaque + capital_cost_ground + capital_cost_transparent + capital_cost_roof
    capital_cost_hvac = (
        capital_cost_heating_equipment +
        capital_cost_cooling_equipment +
        capital_cost_distribution_equipment +
        capital_cost_other_hvac_ahu + capital_cost_lighting
    )

    self._yearly_capital_incomes.loc[0, 'Subsidies construction'] = (
        capital_cost_skin * self._archetype.income.construction_subsidy/100
    )
    self._yearly_capital_incomes.loc[0, 'Subsidies HVAC'] = capital_cost_hvac * self._archetype.income.hvac_subsidy/100
    self._yearly_capital_incomes.loc[0, 'Subsidies PV'] = capital_cost_pv * self._archetype.income.photovoltaic_subsidy/100
    self._yearly_capital_incomes.fillna(0, inplace=True)
    return self._yearly_capital_costs, self._yearly_capital_incomes
