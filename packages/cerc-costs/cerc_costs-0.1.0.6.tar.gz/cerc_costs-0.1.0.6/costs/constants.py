"""
Constants module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributor Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
Code contributor Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""

# constants
CURRENT_STATUS = 0
SKIN_RETROFIT = 1
SYSTEM_RETROFIT_AND_PV = 2
SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV = 3
RETROFITTING_SCENARIOS = [
  CURRENT_STATUS,
  SKIN_RETROFIT,
  SYSTEM_RETROFIT_AND_PV,
  SKIN_RETROFIT_AND_SYSTEM_RETROFIT_AND_PV
]
