#!/usr/bin/env python3
"""
This module provides physical property data sets and models for gases.

Abbreviations:
ds: dataset
ds_dict: datasets
"""

from sys import modules
from os.path import realpath, dirname, join

from auxi.tools.chemistry.stoichiometry import molar_mass as MM
from auxi.tools.materialphysicalproperties.core import DataSet
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
    mm = MM("Ar")  # g/mol

    ds_dict = _create_ds_dict([
        "dataset-argon-lienhard2018"])
    active_ds = "dataset-argon-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    _create_polynomial_model(name, "Cp", 7, ds_dict[active_ds], ds_dict)
    _create_polynomial_model(name, "k", 3, ds_dict[active_ds], ds_dict)
    _create_polynomial_model(name, "mu", 3, ds_dict[active_ds], ds_dict)
    _create_polynomial_model(name, "rho", 6, ds_dict[active_ds], ds_dict)

    IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

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
