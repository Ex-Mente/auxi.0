#!/usr/bin/env python3
"""
This module provides a set of physical constants that are used frequently.
"""

__version__ = '0.3.6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Johan Zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


# TODO: Add literature references to these constants.

# Universal Constants

c = 299792458.0
"""[m·s-1] speed of light in vacuum, from nist2018-constants"""

G = 6.67403E-11
"""[m3.kg-1.s-2] Newtonian constant of gravitation, from nist2018-constants"""

h = 6.626070150E-34
"""[J.s] Planck constant"""

h_bar = 1.054571817E-34
"""[J.s] reduced Planck constant (h/(2pi)), from nist2018-constants"""


# Physico-chemical Constants

m_u = 1.660538921E-27
"""[kg] atomic mass constant"""

N_A = 6.02214076E23
"""[mol-1] Avogadro's number, from nist2018-constants"""

k_B = 1.380649E-23
"""[J.K-1] Boltzmann constant, from nist2018-constants"""

F = 96485.33212
"""[C·mol-1] Faraday constant, from nist2018-constants"""

R = 8.314462618
"""[J.K-1.mol-1] molar gas constant, from nist2018-constants"""

σ = 5.670374419E-8
"""[W.m-2.K-4] Stefan-Boltzmann constant, from nist2018-constants"""


# Other Constants

g = 9.80665
"""[m.s-2] standard acceleration of gravity on earth, from nist2018-constants"""

T_NTP = 293.15
"""[K] Temperature under normal temperature and pressure (NTP) conditions."""

P_NTP = 101325.0
"""[Pa] Pressure under normal temperature and pressure (NTP) conditions."""

T_STP = 273.15
"""[K] Temperature under standard temperature and pressure (NTP) conditions."""

P_STP = 100000.0
"""[Pa] Pressure under standard temperature and pressure (NTP) conditions."""
