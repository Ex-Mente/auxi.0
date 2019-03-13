#!/usr/bin/env python3
"""
This module provides physical property data sets and models for gases.

Abbreviations:
ds: dataset
ds_dict: datasets
"""

from math import sqrt
from sys import modules
from os.path import realpath, dirname, join
from matplotlib.backends.backend_pdf import PdfPages
import webbrowser
import matplotlib.pyplot as plt
import numpy as np

from auxi.tools.chemistry.stoichiometry import molar_mass as M
from auxi.tools.materialphysicalproperties.core import DataSet, Model
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT
from auxi.tools.materialphysicalproperties.idealgas import \
    BetaT as IgBetaT, RhoT as IgRhoT
from auxi.modelling.process.materials.core import Material
from auxi.tools.materialphysicalproperties.core import StateOfMatter


__version__ = "0.3.6"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman, Marno Grewar"
__credits__ = ["Christoff Kok", "Johan Zietsman", "Marno Grewar"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


def _path(relative_path):
    """
    Calculate the full path of the provided relative path.

    :param relative_path: relative path (str).
    :return: str
    """
    path = modules[__name__].__file__
    path = realpath(path)
    path = dirname(path)

    return join(path, relative_path)


def _create_ds_dict(namelist):
    """
    Create a data set dictionary from the provided list of data set names.

    :param namelist: list of data set names (str).
    :return: {str: DataSet}
    """
    return {n: DataSet(_path(f"data/{n}.csv")) for n in namelist}


def _create_polynomial_model(
    name: str,
    symbol: str,
    degree: int,
    ds: DataSet,
    dss: dict):
    """
    Create a polynomial model to describe the specified property based on the
    specified data set, and save it to a .json file.

    :param name: material name.
    :param symbol: property symbol.
    :param degree: polynomial degree.
    :param ds: the source data set.
    :param dss: dictionary of all datasets.
    """
    ds_name = ds.name.split(".")[0].lower()
    file_name = f"{name.lower()}-{symbol.lower()}-polynomialmodelt-{ds_name}"
    newmod = PolynomialModelT.create(ds, symbol, degree)
    newmod.plot(dss, _path(f"data/{file_name}.pdf"), False)
    newmod.write(_path(f"data/{file_name}.json"))


def _create_air():
    """
    Create a dictionary of datasets and a material object for air.

    :return: (Material, {str, DataSet})
    """
    name = "Air"
    namel = name.lower()
    mm = 28.9645  # g/mol

    ds_dict = _create_ds_dict([
        "dataset-air-lienhard2015",
        "dataset-air-lienhard2018"])
    active_ds = "dataset-air-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(name, "Cp", 13, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "k", 8, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "mu", 8, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "rho", 14, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_argon():
    """
    Create a dictionary of datasets and a material object for argon.

    :return: (Material, {str, DataSet})
    """
    name = "Argon"
    namel = name.lower()
    mm = M("Ar")  # g/mol

    ds_dict = _create_ds_dict([
        "dataset-argon-lienhard2018"])
    active_ds = "dataset-argon-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(name, "Cp", 7, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "k", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "mu", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "rho", 6, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_ammonia():
    """
    Create a dictionary of datasets and a material object for ammonia.

    :return: (Material, {str, DataSet})
    """
    name = "Ammonia"
    namel = name.lower()
    mm = M("NH3")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(name, "Cp", 5, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "k", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "mu", 2, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "rho", 6, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["rho", "Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_carbon_dioxide():
    """
    Create a dictionary of datasets and a material object for carbon dioxide.

    :return: (Material, {str, DataSet})
    """
    name = "Carbon Dioxide"
    namel = name.lower().replace(" ", "-")
    mm = M("CO2")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(namel, "Cp", 5, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "k", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "mu", 2, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "rho", 6, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["rho", "Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_carbon_monoxide():
    """
    Create a dictionary of datasets and a material object for carbon monoxide.

    :return: (Material, {str, DataSet})
    """
    name = "Carbon Monoxide"
    namel = name.lower().replace(" ", "-")
    mm = M("CO")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(namel, "Cp", 5, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "k", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "mu", 3, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "rho", 6, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_nitrogen():
    """
    Create a dictionary of datasets and a material object for nitrogen.

    :return: (Material, {str, DataSet})
    """
    name = "Nitrogen"
    namel = name.lower().replace(" ", "-")
    mm = M("N2")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(namel, "Cp", 5, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "k", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "mu", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "rho", 8, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_oxygen():
    """
    Create a dictionary of datasets and a material object for oxygen.

    :return: (Material, {str, DataSet})
    """
    name = "Oxygen"
    namel = name.lower().replace(" ", "-")
    mm = M("O2")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(namel, "Cp", 5, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "k", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "mu", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "rho", 8, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


def _create_water_vapour():
    """
    Create a dictionary of datasets and a material object for water vapour.

    :return: (Material, {str, DataSet})
    """
    name = "Water Vapour"
    namel = name.lower().replace(" ", "-")
    mm = M("H2O")  # g/mol

    ds_dict = _create_ds_dict([
        f"dataset-{namel}-lienhard2018"])
    active_ds = f"dataset-{namel}-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(namel, "Cp", 7, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "k", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "mu", 4, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(namel, "rho", 8, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict


air, air_datasets = _create_air()
argon, argon_datasets = _create_argon()
ammonia, ammonia_datasets = _create_ammonia()
carbon_dioxide, carbon_dioxide_datasets = _create_carbon_dioxide()
carbon_monoxide, carbon_monoxide_datasets = _create_carbon_monoxide()
nitrogen, nitrogen_datasets = _create_nitrogen()
oxygen, oxygen_datasets = _create_oxygen()
water_vapour, water_vapour_datasets = _create_water_vapour()

materials = {
    "Air": air,
    "Ar": argon,
    "NH3": ammonia,
    "CO2": carbon_dioxide,
    "CO": carbon_monoxide,
    "N2": nitrogen,
    "O2": oxygen,
    "H2O": water_vapour}


class WilkeMuTx(Model):
    """
    A model that describes the variation in the dynamic viscosity of a gas
    mixture as a function of temperature and composition expressed in mole
    fraction.

    Source: davidson1993, page 2, equations 2 and 3.
    """

    def __init__(self):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'x': {'required': True, 'type': 'dict'}}
        super().__init__('Gas', 'Dynamic Viscosity', 'mu', '\\mu', 'Pa.s',
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g.
          {'CO': 0.25, 'CO2': 0.25, 'N2': 0.25, 'O2': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        def phi(i, j, mu_i, mu_j):
            M_i = M(i)
            M_j = M(j)

            result = (1.0 + (mu_i / mu_j)**0.5 * (M_j / M_i)**0.25)**2.0
            result /= (4.0 / sqrt(2.0))
            result /= (1.0 + M_i / M_j)**0.5

            return result

        T = state['T']
        x = state['x']

        # normalise mole fractions
        x_total = sum([
            x for compound, x in x.items()
            if compound in materials])
        x = {
            compound: x[compound]/x_total
            for compound in x.keys()
            if compound in materials}

        result = 0.0  # Pa.s
        mu = {i: materials[i].mu(T=T) for i in x.keys()}
        for i in x.keys():
            sum_i = 0.0
            for j in x.keys():
                if j == i: continue
                sum_i += x[j] * phi(i, j, mu[i], mu[j])

            result += x[i] * mu[i] / (x[i] + sum_i)

        return result  # [Pa.s]

    def plot(self, xs, datasets, path, show=False):
        with PdfPages(path) as pdf:
            T_min = 1.0e100
            T_max = -1.0e100

            for compound, ds in datasets.items():
                T_vals = ds.data['T'].tolist()
                y_vals = ds.data[self.symbol].tolist()
                plt.plot(
                    T_vals, y_vals, "o", alpha=0.4, markersize=4, label=ds.name)

                T_min = min(min(T_vals), T_min)
                T_max = max(max(T_vals), T_max)

                # T_vals2 = np.linspace(T_min, T_max, 80)
                T_vals2 = np.linspace(T_min, 1000.0, 80)
                fx = [self(T=T, x=xs[compound]) for T in T_vals2]
                plt.plot(T_vals2, fx, linewidth=0.3, label=f"{compound} model")

            plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 4))
            plt.legend(loc=0)
            plt.title('$%s$ vs $T$' % self.display_symbol)
            plt.xlabel('$T$ (K)')

            plt.ylabel('$%s$ (%s)' % (self.display_symbol, self.units))

            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

        if show:
            webbrowser.open_new(path)


class HerningZippererMuTx(Model):
    """
    A model that describes the variation in the dynamic viscosity of a gas
    mixture as a function of temperature and composition expressed in mole
    fraction.

    Source: davidson1993, page 2, equations 4.
    """

    def __init__(self):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'x': {'required': True, 'type': 'dict'}}
        super().__init__('Gas', 'Dynamic Viscosity', 'mu', '\\mu', 'Pa.s',
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g.
          {'CO': 0.25, 'CO2': 0.25, 'N2': 0.25, 'O2': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        T = state['T']
        x = state['x']

        # normalise mole fractions
        x_total = sum([
            x for compound, x in x.items()
            if compound in materials])
        x = {
            compound: x[compound]/x_total
            for compound in x.keys()
            if compound in materials}

        mu = {i: materials[i].mu(T=T) for i in x.keys()}

        result = sum([mu[i] * x[i] * sqrt(M(i)) for i in x.keys()])
        result /= sum([x[i] * sqrt(M(i)) for i in x.keys()])

        return result  # [Pa.s]

    def plot(self, xs, datasets, path, show=False):
        with PdfPages(path) as pdf:
            T_min = 1.0e100
            T_max = -1.0e100

            for compound, ds in datasets.items():
                T_vals = ds.data['T'].tolist()
                y_vals = ds.data[self.symbol].tolist()
                plt.plot(
                    T_vals, y_vals, "o", alpha=0.4, markersize=4, label=ds.name)

                T_min = min(min(T_vals), T_min)
                T_max = max(max(T_vals), T_max)

                # T_vals2 = np.linspace(T_min, T_max, 80)
                T_vals2 = np.linspace(T_min, 1000.0, 80)
                fx = [self(T=T, x=xs[compound]) for T in T_vals2]
                plt.plot(T_vals2, fx, linewidth=0.3, label=f"{compound} model")

            plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 4))
            plt.legend(loc=0)
            plt.title('$%s$ vs $T$' % self.display_symbol)
            plt.xlabel('$T$ (K)')

            plt.ylabel('$%s$ (%s)' % (self.display_symbol, self.units))

            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

        if show:
            webbrowser.open_new(path)


class IdealCpTx(Model):
    """
    A model that describes the variation in heat capacity of a gas mixture at
    1 atmosphere pressure as a function of temperature and composition
    expressed in mole fraction.
    """

    def __init__(self):
        state_schema = {"T": {"required": True, "type": "float", "min": 0.0},
                        "x": {"required": True, "type": "dict"}}
        super().__init__("Gas", "Heat Capacity", "Cp", "C_p", "J/kg/K",
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g.
          {"CO": 0.25, "CO2": 0.25, "N2": 0.25, "O2": 0.25}

        :returns: [J/kg/K] heat capacity

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        T = state["T"]
        x = state["x"]

        # normalise mole fractions
        x_total = sum([
            x for compound, x in x.items()
            if compound in materials])
        x = {
            compound: x[compound]/x_total
            for compound in x.keys()
            if compound in materials}

        Cp = {i: materials[i].Cp(T=T) for i in x.keys()}

        result = sum([Cp[i] * x[i] * M(i) for i in x.keys()])
        result /= sum([x[i] * M(i) for i in x.keys()])

        return result  # [Pa.s]

    def plot(self, xs, datasets, path, show=False):
        with PdfPages(path) as pdf:
            T_min = 1.0e100
            T_max = -1.0e100

            for compound, ds in datasets.items():
                T_vals = ds.data["T"].tolist()
                y_vals = ds.data[self.symbol].tolist()
                plt.plot(
                    T_vals, y_vals, "o", alpha=0.4, markersize=4, label=ds.name)

                T_min = min(min(T_vals), T_min)
                T_max = max(max(T_vals), T_max)

                # T_vals2 = np.linspace(T_min, T_max, 80)
                T_vals2 = np.linspace(T_min, 1000.0, 80)
                fx = [self(T=T, x=xs[compound]) for T in T_vals2]
                plt.plot(T_vals2, fx, linewidth=0.3, label=f"{compound} model")

            plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 4))
            plt.legend(loc=0)
            plt.title("$%s$ vs $T$" % self.display_symbol)
            plt.xlabel("$T$ (K)")

            plt.ylabel("$%s$ (%s)" % (self.display_symbol, self.units))

            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

        if show:
            webbrowser.open_new(path)


# WilkeMuTx().plot(
#     {"Air": {"N2": 0.79, "O2": 0.21}},
#     {"Air": air_datasets["dataset-air-lienhard2018"]},
#     "data/gas-mixture-mu-wilket.pdf")
# HerningZippererMuTx().plot(
#     {"Air": {"N2": 0.79, "O2": 0.21}},
#     {"Air": air_datasets["dataset-air-lienhard2018"]},
#     "data/gas-mixture-mu-herningzipperert.pdf")
# IdealCpTx().plot(
#     {"Air": {"N2": 0.79, "O2": 0.21}},
#     {"Air": air_datasets["dataset-air-lienhard2018"]},
#     "data/gas-mixture-cp-idealxt.pdf")
