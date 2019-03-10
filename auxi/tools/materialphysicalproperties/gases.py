#!/usr/bin/env python3
"""
This module provides physical property data sets and models for gases.
"""

from sys import modules
from os.path import realpath, dirname, join

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


def _create_dataset_dict(name_list):
    """
    Create a data set dictionary from the provided list of data set names.

    :param name_list: list of data set names (str).
    :return: {str: DataSet}
    """
    return {n: DataSet(_path(f"data/{n}")) for n in name_list}


def _create_polynomial_model(
    name: str,
    symbol: str,
    degree: int,
    dataset: DataSet):
    """
    Create a polynomial model to describe the specified property based on the
    specified data set, and save it to a .json file.

    :param name: material name.
    :param symbol: property symbol.
    :param degree: polynomial degree.
    :param dataset: the source data set.
    """
    newmod = PolynomialModelT.create(dataset, symbol, degree)
    newmod.plot(dataset, _path("temp.pdf"), False)
    newmod.write(_path(f"data/{name.lower()}-{symbol.lower()}.json")


def _create_air():
    name = "air"

    datasets = _create_dataset_dict([
        "dataset-air-lienhard2015.csv",
        "dataset-air-lienhard2018.csv"])
    active_dataset = "dataset-air-lienhard2018.csv"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model("Air", "Cp", 14, datasets[active_dataset])
    # _create_polynomial_model("Air", "k", 8, datasets[active_dataset])
    # _create_polynomial_model("Air", "mu", 8, datasets[active_dataset])
    # _create_polynomial_model("Air", "rho", 14, datasets[active_dataset])

    material_dict = {"rho": IgRhoT(28.9645, 101325.0),
                "Cp": PolynomialModelT.read(_path(r"data/air-cp.json")),
                "mu": PolynomialModelT.read(_path(r"data/air-mu.json")),
                "k": PolynomialModelT.read(_path(r"data/air-k.json")),
                "beta": IgBetaT()}

    material = Material("Air", StateOfMatter.gas, air_dict)

    return material, datasets


air, air_datasets = _create_air()
