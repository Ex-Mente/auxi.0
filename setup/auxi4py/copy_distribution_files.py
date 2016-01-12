# USAGE: you probably want 'setup.py install' - but execute 'setup.py --help'
# for all the details.

# from setuptools import setup, Extension, Command
from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_ext import build_ext
from subprocess import call
import os
import sys
import shutil
import glob
import sys


# =============================================================================
# functions
# =============================================================================

def remove_old_files(path):
    """Remove all files other than the '__init__.py' file from this folder and
    its sub-folders."""

    print('cleaning', path)
    for name in os.listdir(path):
        full_name = os.path.join(path, name)
        if os.path.isdir(full_name):
            remove_old_files(full_name)
        elif name != '__init__.py':
            print('\tremoving', name)
            os.remove(full_name)


def copy_files(source, destination):
    """Copy all the files matching the source pattern to the destination
    folder."""

    for file in glob.glob(source):
        shutil.copy(file, destination)


def files_find_and_replace(source, find_str, replace_str):
    """Find the specified string in all the files matching the source pattern
    and replace it with the replacement string."""

    for file_path in glob.glob(source):
        file = open(file_path, 'r')
        filedata = file.read()
        file.close()

        f = open(file_path, 'w')
        f.write(filedata.replace(find_str, replace_str))
        f.close()


def deleteFileOrFolder(directory):
    if os.path.exists(directory):
        try:
            if os.path.isdir(directory):
                # delete folder
                shutil.rmtree(directory)
            else:
                # delete file
                os.remove(directory)
        except:
            print("Exception ", str(sys.exc_info()))
    else:
        print("not found ", directory)


# =============================================================================
# main program
# =============================================================================

#patchelf_path = sys.argv[1]
#if patchelf_path == "":
#    patchelf_path = input('Enter the path to the patchelf executable: ')
patchelf_path = "~/.local/bin/patchelf"
# create path strings
project_path = os.path.dirname(os.path.abspath(__file__))
dep_path_auxi = os.path.join(project_path, 'auxi')
dep_path__core = os.path.join(dep_path_auxi, 'core')
dep_path__tools_chemistry = os.path.join(dep_path_auxi, 'tools', 'chemistry')
dep_path__modelling_acc_fin = os.path.join(dep_path_auxi, 'modelling', 'accounting', 'financial')
dep_path__modelling_acc_stock = os.path.join(dep_path_auxi, 'modelling', 'accounting', 'stock')
dep_path__modelling_business = os.path.join(dep_path_auxi, 'modelling', 'business')
dep_path__simulation = os.path.join(dep_path_auxi, 'simulation')
dep_path__simulation_io = os.path.join(dep_path__simulation, 'io')

dep_path_thermo_data_files = os.path.join(dep_path__tools_chemistry, 'data')

boost_py_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_python-py34.so.1.54.0"
boost_dt_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.54.0"
boost_fs_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.54.0"
boost_sy_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_system.so.1.54.0"

# delete old files from package structure and add new ones
print("REMOVE OLD FILES")
remove_old_files(dep_path_auxi)
deleteFileOrFolder(dep_path_thermo_data_files)
print()

core_mod_path = os.path.join(project_path, r"../../src/auxi4py/core/bin/gcc-c++11/release/core.so")
stoi_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/stoichiometry/bin/gcc-c++11/release/stoichiometry.so")
thermochem_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/thermochemistry/bin/gcc-c++11/release/thermochemistry.so")
financial_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/accounting/financial/bin/gcc-c++11/release/_financial.so")
stock_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/accounting/stock/bin/gcc-c++11/release/_stock.so")
business_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/business/bin/gcc-c++11/release/_business.so")

core_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/core/bin/gcc-c++11/release/libcore.so"),
boost_py_lib_path,
boost_dt_lib_path,
boost_fs_lib_path,
boost_sy_lib_path,
core_mod_path
]

stoi_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/stoichiometry/bin/gcc-c++11/release/libstoichiometry.so"),
boost_fs_lib_path,
stoi_mod_path
]

thermochem_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/thermochemistry/bin/gcc-c++11/release/libthermochemistry.so"),
thermochem_mod_path
]

financial_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/modelling/accounting/financial/bin/gcc-c++11/release/libfinancial.so"),
financial_mod_path
]

stock_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/modelling/accounting/stock/bin/gcc-c++11/release/libstock.so"),
stock_mod_path
]

business_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/modelling/business/bin/gcc-c++11/release/libbusiness.so"),
business_mod_path
]


print('COPY DEPENDENCIES')
for dep in core_dependencies_paths:
    shutil.copy(dep, dep_path__core)
for dep in stoi_dependencies_paths:
    shutil.copy(dep, dep_path__tools_chemistry)
for dep in thermochem_dependencies_paths:
    shutil.copy(dep, dep_path__tools_chemistry)
for dep in financial_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_acc_fin)
for dep in stock_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_acc_stock)
for dep in business_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_business)

new_core_mod_path = os.path.join(dep_path__core, "core.so")
new_stoichiometry_mod_path = os.path.join(dep_path__tools_chemistry, "stoichiometry.so")
new_thermochem_mod_path = os.path.join(dep_path__tools_chemistry, "thermochemistry.so")
new_thermochem_lib_path = os.path.join(dep_path__tools_chemistry, "libthermochemistry.so")
new_financial_mod_path = os.path.join(dep_path__modelling_acc_fin, "_financial.so")
new_stock_mod_path = os.path.join(dep_path__modelling_acc_stock, "_stock.so")
new_business_mod_path = os.path.join(dep_path__modelling_business, "_business.so")

call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN' " + new_core_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_stoichiometry_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_lib_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../../core' "+ new_financial_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../../core' "+ new_stock_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core:$ORIGIN/../accounting/financial:$ORIGIN/../accounting/stock' "+ new_business_mod_path], shell=True)

print('COPY REPORTS')
shutil.copy(r"../../src/auxi4py/modelling/accounting/financial/reports/balance_sheet_report.py", dep_path__modelling_acc_fin)
shutil.copy(r"../../src/auxi4py/modelling/accounting/financial/reports/income_statement_report.py", dep_path__modelling_acc_fin)
shutil.copy(r"../../src/auxi4py/modelling/accounting/financial/reports/financial_transactions_report.py", dep_path__modelling_acc_fin)
shutil.copy(r"../../src/auxi4py/modelling/accounting/financial/reports/classes_report.py", dep_path__modelling_acc_fin)

print('COPY INVESTIGATION')
copy_files(r"../../src/auxi4py/simulation/py/*.py", dep_path__simulation)
copy_files(r"../../src/auxi4py/simulation/py/io/*.py", dep_path__simulation_io)

print('COPY DATA FILES')
thermo_data_files_path = r"../../src/auxi/tools/chemistry/thermochemistry/data/"
if not os.path.exists(thermo_data_files_path):
    os.makedirs(thermo_data_files_path)
shutil.copytree(thermo_data_files_path, dep_path_thermo_data_files)

print()

# build the distribution
setup(name="auxi",
      version="0.0.0",
      description="auxi for Python",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core",
                "auxi.modelling", "auxi.modelling.business", "auxi.modelling.accounting.financial", "auxi.modelling.accounting.stock", "auxi.simulation",
                "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*'],
                    'auxi.modelling.accounting.financial': ['*.a', '*.so*', '*_report.py'],
                    'auxi.modelling.accounting.stock': ['*.a', '*.so*', '*_report.py'],
                    'auxi.modelling.business': ['*.a', '*.so*', '*_report.py'],
                    'auxi.simulation': ['*.py', r'io/*'],
                    'auxi.tools.chemistry': ['*.so*', r'data/*']}#,
     #               'auxi' : [r'datafiles/*']}
)

print("Done")
