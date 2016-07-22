"""
This package provides tools to do calculations related to heat transfer.
"""

from math import radians, cos
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from auxi.core.objects import Object, NamedObject
from auxi.tools.transportphenomena import dimensionlessquantities as dq
from auxi.tools import physicalconstants as const


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class EmpiricalCorrelation(Object):
    """
    Abstract base class for empirical correlations to calculate natural
    convection heat transfer.
    """

    def __init__(self, fluid, references):
        self._fluid = fluid
        self.references = references


class IsothermalFlatSurface(EmpiricalCorrelation):
    """
    Contains configuration and calculations for an isothermal flat surface.

    :param fluid: material physical properties of a fluid
    :param isgas: Specify if the surface is a gas (default is True)
    :param references: The references used for the configurations
      (default is None)
    """

    class Region(NamedObject):
        """
        Defines a region in the 2D Ra-theta coordinate system. A region is used
        to determine which equation should be used to determine the isothermal
        flat surface.

        :param name: name of the region
        :param theta_min: minimum theta value
        :param theta_min_incl: should the minimum theta be included?
        :param theta_max: maximum theta value
        :param theta_max_incl: should the maximum theta be included?
        :param Ra_min: minimum Ra value (default is None)
        :param Ra_min_incl: should the minimum Ra be included? (default is True)
        :param Ra_max: maximum Ra value (default is None)
        :param Ra_max_incl: should the maximum Ra be included? (default is True)
        :param description: description of the region (default is None)
        """

        def __init__(self, name,
                     theta_min, theta_min_incl,
                     theta_max, theta_max_incl,
                     Ra_min=None, Ra_min_incl=True,
                     Ra_max=None, Ra_max_incl=True,
                     description=None):
            super().__init__(name, description)

            self.theta_min = theta_min
            self.theta_min_incl = theta_min_incl
            if self.theta_min_incl:
                self._theta_min = self._theta_min_incl
            else:
                self._theta_min = self._theta_min_excl

            self.theta_max = theta_max
            self.theta_max_incl = theta_max_incl
            if self.theta_max_incl:
                self._theta_max = self._theta_max_incl
            else:
                self._theta_max = self._theta_max_excl

            self.Ra_min = Ra_min
            self.Ra_min_incl = Ra_min_incl
            if self.Ra_min is None:
                self._Ra_min = self._Ra_min_none
            elif self.Ra_min_incl:
                self._Ra_min = self._Ra_min_incl
            else:
                self._Ra_min = self._Ra_min_excl

            self.Ra_max = Ra_max
            self.Ra_max_incl = Ra_max_incl
            if self.Ra_max is None:
                self._Ra_max = self._Ra_max_none
            elif self.Ra_max_incl:
                self._Ra_max = self._Ra_max_incl
            else:
                self._Ra_max = self._Ra_max_excl

        def _theta_min_incl(self, theta):
            return theta >= self.theta_min

        def _theta_min_excl(self, theta):
            return theta > self.theta_min

        def _theta_max_incl(self, theta):
            return theta <= self.theta_max

        def _theta_max_excl(self, theta):
            return theta < self.theta_max

        def _Ra_min_none(self, Ra):
            return True

        def _Ra_min_incl(self, Ra):
            return Ra >= self.Ra_min

        def _Ra_min_excl(self, Ra):
            return Ra > self.Ra_min

        def _Ra_max_none(self, Ra):
            return True

        def _Ra_max_incl(self, Ra):
            return Ra <= self.Ra_max

        def _Ra_max_excl(self, Ra):
            return Ra < self.Ra_max

        def contains_point(self, theta, Ra):
            """
            Determines if a theta and Ra value falls inside the region.

            :param theta: theta value
            :param Ra: Ra value

            :returns: True of False
            """

            if not self._theta_min(theta):
                return False
            if not self._theta_max(theta):
                return False
            if not self._Ra_min(Ra):
                return False
            if not self._Ra_max(Ra):
                return False
            return True

        def plot_region(self):
            """
            Plots the region to a graph
            """

            theta_diff = self.theta_max - self.theta_min
            Ra_min_plot = self.Ra_min
            Ra_max_plot = self.Ra_max
            if self.Ra_min is None:
                Ra_min_plot = 3
                Ra_diff = Ra_max_plot - Ra_min_plot
            elif self.Ra_max is None:
                Ra_max_plot = 12
                Ra_diff = Ra_max_plot - Ra_min_plot
            else:
                Ra_diff = Ra_max_plot - Ra_min_plot

            plt.xlim(-90, 90)
            plt.ylim(3, 12)

            plt.xlabel('angle [°]')
            plt.ylabel('Ra')

            currentAxis = plt.gca()

            if self.description == "In_Eq_Region":
                currentAxis.add_patch(Rectangle((self.theta_min, Ra_min_plot),
                                                theta_diff, Ra_diff,
                                                facecolor="grey"))
            else:
                currentAxis.add_patch(Rectangle((self.theta_min, Ra_min_plot),
                                                theta_diff, Ra_diff,
                                                facecolor="red"))

            mid_theta = (self.theta_max + self.theta_min-5) / 2.0
            mid_Ra = (Ra_max_plot + Ra_min_plot-0.6) / 2.0
            currentAxis.annotate(self.name, xy=(mid_theta, mid_Ra),
                                 xytext=(mid_theta, mid_Ra), fontsize=14)

    def __init__(self, fluid, isgas=True, references=None):
        super().__init__(fluid, references)

        self._isgas = isgas

        self.equation_dict = {}

        ifs = IsothermalFlatSurface
        eq_dict = self.equation_dict

        region = self.Region("r1", -90, True, -60, True, None, False, 4, False)
        eq_dict[region] = ifs._Nu_x__9_22
        region = self.Region("r2", -90, True, -60, True, 4, True, 7, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__9_22
        region = self.Region("r3", -90, True, -60, True, 7, False, 11, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__9_23
        region = self.Region("r4", -90, True, -60, True, 11, False, None,
                             False)
        eq_dict[region] = ifs._Nu_x__9_23
        region = self.Region("r5", -60, False, -52, True, None, False, 7, True)
        eq_dict[region] = ifs._Nu_x__9_22
        region = self.Region("r6", -60, False, -52, True, 7, False, None,
                             False)
        eq_dict[region] = ifs._Nu_x__9_23
        region = self.Region("r7", -52, False, -45, False, None, False, 7,
                             True)
        eq_dict[region] = ifs._Nu_x__8_27_g
        region = self.Region("r8", -52, False, -45, False, 7, False, None,
                             False)
        eq_dict[region] = ifs._Nu_x__8_27_g
        region = self.Region("r9", -45, True, 0, False, None, False, 5, False)
        eq_dict[region] = ifs._Nu_x__8_27_g
        region = self.Region("r10", -45, True, 0, False, 5, True, 9, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__8_27_g
        region = self.Region("r11", -45, True, 0, False, 9, True, None, True)
        eq_dict[region] = ifs._Nu_x__8_27_g
        region = self.Region("r12", 0, True, 0, True, None, False, 5, True)
        eq_dict[region] = ifs._Nu_x__8_26
        region = self.Region("r13", 0, True, 0, True, 5, False, 11, False,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__8_26
        region = self.Region("r14", 0, True, 0, True, 11, False, None, False)
        eq_dict[region] = ifs._Nu_x__8_26
        region = self.Region("r15", 0, False, 88, False, None, False, 5, False)
        eq_dict[region] = ifs._Nu_x__8_27
        region = self.Region("r16", 0, True, 88, False, 5, True, 11, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__8_27
        region = self.Region("r17", 0, False, 88, False, 11, False, None,
                             False)
        eq_dict[region] = ifs._Nu_x__8_27
        region = self.Region("r18", 88, False, 90, True, None, False, 6, False)
        eq_dict[region] = ifs._Nu_x__8_38
        region = self.Region("r19", 88, True, 90, True, 6, True, 9, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__8_38
        region = self.Region("r20", 88, True, 89, False, 9, False, None, False)
        eq_dict[region] = ifs._Nu_x__8_38
        region = self.Region("r21", 89, True, 90, True, 9, True, 11, True,
                             "In_Eq_Region")
        eq_dict[region] = ifs._Nu_x__8_38
        region = self.Region("r22", 88, False, 90, True, 11, False, None,
                             False)
        eq_dict[region] = ifs._Nu_x__8_38

        self.regions = list(self.equation_dict.keys())

    def _Nu_x__8_26(self, Ra, Pr):
        return (0.678 * Ra**0.25) * (Pr / (0.952 + Pr)) ** 0.25

    def _Nu_x__8_27(self, Ra, Pr):
        return (0.68 + (0.67 * Ra**0.25) / ((1.0 + (0.492 / Pr) **
                (9.0/16.0)) ** (4.0/9.0)))

    def _Nu_x__8_27_g(self, Ra, Pr):
        return (0.68 + (0.67 * Ra**0.25) / ((1.0 + (0.492 / Pr) **
                (9.0/16.0)) ** (4.0/9.0)))

    def _Nu_x__8_38(self, Ra, Pr):
        return 0.58 * Ra**0.2

    def _Nu_x__9_22(self, Ra, Pr):
        return 0.59 * Ra**0.25

    def _Nu_x__9_23(self, Ra, Pr):
        return 0.1 * Ra**(1/3.0)

    def Nu_x(self, L, theta, Ts, **statef):
        """
        Calculate the local Nusselt number.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: float
        """

        Tf = statef['T']
        thetar = radians(theta)

        if self._isgas:
            self.Tr = Ts - 0.38 * (Ts - Tf)
            beta = self._fluid.beta(T=Tf)
        else:  # for liquids
            self.Tr = Ts - 0.5 * (Ts - Tf)
            beta = self._fluid.beta(T=self.Tr)

        if Ts > Tf:  # hot surface
            if 0.0 < theta < 45.0:
                g = const.g*cos(thetar)
            else:
                g = const.g
        else:  # cold surface
            if -45.0 < theta < 0.0:
                g = const.g*cos(thetar)
            else:
                g = const.g

        nu = self._fluid.nu(T=self.Tr)
        alpha = self._fluid.alpha(T=self.Tr)

        Gr = dq.Gr(L, Ts, Tf, beta, nu, g)
        Pr = dq.Pr(nu, alpha)
        Ra = Gr * Pr

        eq = [self.equation_dict[r]
              for r in self.regions if r.contains_point(theta, Ra)][0]

        return eq(self, Ra, Pr)

    def Nu_L(self, L, theta, Ts, **statef):
        """
        Calculate the average Nusselt number.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param **statef: [K] bulk fluid temperature

        :returns: float
        """

        return self.Nu_x(L, theta, Ts, **statef) / 0.75

    def h_x(self, L, theta, Ts, **statef):
        """
        Calculate the local heat transfer coefficient.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: [W/m2/K] float
        """

        Nu_x = self.Nu_x(L, theta, Ts, **statef)
        k = self._fluid.k(T=self.Tr)
        return Nu_x * k / L

    def h_L(self, L, theta, Ts, **statef):
        """
        Calculate the average heat transfer coefficient.

        :param L: [m] characteristic length of the heat transfer surface
        :param theta: [°] angle of the surface with the vertical
        :param Ts: [K] heat transfer surface temperature
        :param Tf: [K] bulk fluid temperature

        :returns: [W/m2/K] float
        """

        Nu_L = self.Nu_L(L, theta, Ts, **statef)
        k = self._fluid.k(T=self.Tr)
        return Nu_L * k / L

    def plot_regions(self):
        """
        Plot all the regions.
        """
        for region in self.regions:
            region.plot_region()
        plt.show()
