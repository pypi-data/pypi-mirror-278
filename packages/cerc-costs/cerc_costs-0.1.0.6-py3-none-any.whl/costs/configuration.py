"""
Configuration module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
from hub.catalog_factories.costs_catalog_factory import CostsCatalogFactory
from hub.catalog_factories.catalog import Catalog


class Configuration:
  """
  Configuration class
  """

  def __init__(self,
               number_of_years,
               percentage_credit,
               interest_rate,
               credit_years,
               consumer_price_index,
               electricity_peak_index,
               electricity_price_index,
               gas_price_index,
               discount_rate,
               retrofitting_year_construction,
               factories_handler,
               retrofit_scenario,
               fuel_type,
               dictionary
               ):
    self._number_of_years = number_of_years
    self._percentage_credit = percentage_credit
    self._interest_rate = interest_rate
    self._credit_years = credit_years
    self._consumer_price_index = consumer_price_index
    self._electricity_peak_index = electricity_peak_index
    self._electricity_price_index = electricity_price_index
    self._gas_price_index = gas_price_index
    self._discount_rate = discount_rate
    self._retrofitting_year_construction = retrofitting_year_construction
    self._factories_handler = factories_handler
    self._costs_catalog = CostsCatalogFactory(factories_handler).catalog
    self._retrofit_scenario = retrofit_scenario
    self._fuel_type = fuel_type
    self._dictionary = dictionary

  @property
  def number_of_years(self):
    """
    Get number of years
    """
    return self._number_of_years

  @number_of_years.setter
  def number_of_years(self, value):
    """
    Set number of years
    """
    self._number_of_years = value

  @property
  def percentage_credit(self):
    """
    Get percentage credit
    """
    return self._percentage_credit

  @percentage_credit.setter
  def percentage_credit(self, value):
    """
    Set percentage credit
    """
    self._percentage_credit = value

  @property
  def interest_rate(self):
    """
    Get interest rate
    """
    return self._interest_rate

  @interest_rate.setter
  def interest_rate(self, value):
    """
    Set interest rate
    """
    self._interest_rate = value

  @property
  def credit_years(self):
    """
    Get credit years
    """
    return self._credit_years

  @credit_years.setter
  def credit_years(self, value):
    """
    Set credit years
    """
    self._credit_years = value

  @property
  def consumer_price_index(self):
    """
    Get consumer price index
    """
    return self._consumer_price_index

  @consumer_price_index.setter
  def consumer_price_index(self, value):
    """
    Set consumer price index
    """
    self._consumer_price_index = value

  @property
  def electricity_peak_index(self):
    """
    Get electricity peak index
    """
    return self._electricity_peak_index

  @electricity_peak_index.setter
  def electricity_peak_index(self, value):
    """
    Set electricity peak index
    """
    self._electricity_peak_index = value

  @property
  def electricity_price_index(self):
    """
    Get electricity price index
    """
    return self._electricity_price_index

  @electricity_price_index.setter
  def electricity_price_index(self, value):
    """
    Set electricity price index
    """
    self._electricity_price_index = value

  @property
  def gas_price_index(self):
    """
    Get gas price index
    """
    return self._gas_price_index

  @gas_price_index.setter
  def gas_price_index(self, value):
    """
    Set gas price index
    """
    self._gas_price_index = value

  @property
  def discount_rate(self):
    """
    Get discount rate
    """
    return self._discount_rate

  @discount_rate.setter
  def discount_rate(self, value):
    """
    Set discount rate
    """
    self._discount_rate = value

  @property
  def retrofitting_year_construction(self):
    """
    Get retrofitting year construction
    """
    return self._retrofitting_year_construction

  @retrofitting_year_construction.setter
  def retrofitting_year_construction(self, value):
    """
    Set retrofitting year construction
    """
    self._retrofitting_year_construction = value

  @property
  def factories_handler(self):
    """
    Get factories handler
    """
    return self._factories_handler

  @factories_handler.setter
  def factories_handler(self, value):
    """
    Set factories handler
    """
    self._factories_handler = value

  @property
  def costs_catalog(self) -> Catalog:
    """
    Get costs catalog
    """
    return self._costs_catalog

  @property
  def retrofit_scenario(self):
    """
    Get retrofit scenario
    """
    return self._retrofit_scenario

  @property
  def fuel_type(self):
    """
    Get fuel type (0: Electricity, 1: Gas)
    """
    return self._fuel_type

  @property
  def dictionary(self):
    """
    Get hub function to cost function dictionary
    """
    return self._dictionary
