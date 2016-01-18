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
dep_path__modelling_fin = os.path.join(dep_path_auxi, 'modelling', 'financial')
dep_path__modelling_stock = os.path.join(dep_path_auxi, 'modelling', 'stock')
dep_path__modelling_business = os.path.join(dep_path_auxi, 'modelling')
dep_path__simulation = os.path.join(dep_path_auxi, 'simulation')
dep_path__simulation_io = os.path.join(dep_path__simulation, 'io')

dep_path_thermo_data_files = os.path.join(dep_path__tools_chemistry, 'data')

boost_py_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_python-py34.so.1.54.0"
boost_dt_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.54.0"
boost_fs_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.54.0"
boost_sy_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_system.so.1.54.0"

win_boost_py_lib = "libboost_date_time-mgw48-mt-1_58.a"
win_boost_dt_lib = "libboost_filesystem-mgw48-mt-1_58.a"
win_boost_fs_lib = "libboost_python3-mgw48-1_58.dll"
win_boost_sy_lib = "libboost_system-mgw48-mt-1_58.a"

win_boost_py_lib_path = os.path.join(project_path, "lib", win_boost_py_lib)
win_boost_dt_lib_path = os.path.join(project_path, "lib", win_boost_dt_lib)
win_boost_fs_lib_path = os.path.join(project_path, "lib", win_boost_fs_lib)
win_boost_sy_lib_path = os.path.join(project_path, "lib", win_boost_sy_lib)

def create_win_libs_symbolic_links(relative_path_to_core, desitination):
    call(["ln -s  " + os.path.join(relative_path_to_core, win_boost_py_lib) + "  " + os.path.join(desitination, win_boost_py_lib)], shell=True)
    call(["ln -s  " + os.path.join(relative_path_to_core, win_boost_dt_lib) + "  " + os.path.join(desitination, win_boost_dt_lib)], shell=True)
    call(["ln -s  " + os.path.join(relative_path_to_core, win_boost_fs_lib) + "  " + os.path.join(desitination, win_boost_fs_lib)], shell=True)
    call(["ln -s  " + os.path.join(relative_path_to_core, win_boost_sy_lib) + "  " + os.path.join(desitination, win_boost_sy_lib)], shell=True)


# delete old files from package structure and add new ones
print("REMOVE OLD FILES")
remove_old_files(dep_path_auxi)
deleteFileOrFolder(dep_path_thermo_data_files)
print()

core_mod_path = os.path.join(project_path, r"../../src/auxi4py/core/bin/gcc-c++11/release/core.so")
stoi_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/stoichiometry/bin/gcc-c++11/release/stoichiometry.so")
thermochem_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/thermochemistry/bin/gcc-c++11/release/thermochemistry.so")
fincalc_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/financial/calculation_engines/bin/gcc-c++11/release/calculation_engines.so")
des_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/financial/double_entry_system/bin/gcc-c++11/release/des.so")
tax_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/financial/tax/bin/gcc-c++11/release/tax.so")
stock_calc_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/stock/calculation_engines/bin/gcc-c++11/release/calculation_engines.so")
stock_des_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/stock/double_entry_system/bin/gcc-c++11/release/des.so")
business_mod_path = os.path.join(project_path, r"../../src/auxi4py/modelling/business/bin/gcc-c++11/release/business.so")

core_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/core/bin/gcc-c++11/release/libcore.so"),
boost_py_lib_path,
boost_dt_lib_path,
boost_fs_lib_path,
boost_sy_lib_path,
os.path.join(project_path, r"lib/core.pyd"),
os.path.join(project_path, r"lib/core_win.dll"),
win_boost_py_lib_path,
win_boost_dt_lib_path,
win_boost_fs_lib_path,
win_boost_sy_lib_path,
core_mod_path
]

stoi_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/stoichiometry/bin/gcc-c++11/release/libstoichiometry.so"),
boost_fs_lib_path,
os.path.join(project_path, r"lib/core.pyd"),
os.path.join(project_path, r"lib/core_win.dll"),
os.path.join(project_path, r"lib/stoichiometry.pyd"),
os.path.join(project_path, r"lib/stoichiometry_win.dll"),
os.path.join(project_path, r"lib/thermochemistry.pyd"),
os.path.join(project_path, r"lib/thermochemistry_win.dll"),
stoi_mod_path
]

thermochem_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/thermochemistry/bin/gcc-c++11/release/libthermochemistry.so"),
thermochem_mod_path
]

financial_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/modelling/financial/calculation_engines/bin/gcc-c++11/release/libcalculation_engines.so"),
os.path.join(project_path, r"../../src/auxi/modelling/financial/double_entry_system/bin/gcc-c++11/release/libdouble_entry_system.so"),
os.path.join(project_path, r"../../src/auxi/modelling/financial/tax/bin/gcc-c++11/release/libtax.so"),
fincalc_mod_path,
des_mod_path,
tax_mod_path
]

stock_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/modelling/stock/calculation_engines/bin/gcc-c++11/release/libcalculation_engines.so"),
os.path.join(project_path, r"../../src/auxi/modelling/stock/double_entry_system/bin/gcc-c++11/release/libdouble_entry_system.so"),
stock_calc_mod_path,
stock_des_mod_path
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
    create_win_libs_symbolic_links("../../core", dep_path__tools_chemistry)
for dep in thermochem_dependencies_paths:
    shutil.copy(dep, dep_path__tools_chemistry)
for dep in financial_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_fin)
for dep in stock_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_stock)
for dep in business_dependencies_paths:
    shutil.copy(dep, dep_path__modelling_business)

new_core_mod_path = os.path.join(dep_path__core, "core.so")
new_stoichiometry_mod_path = os.path.join(dep_path__tools_chemistry, "stoichiometry.so")
new_thermochem_mod_path = os.path.join(dep_path__tools_chemistry, "thermochemistry.so")
new_thermochem_lib_path = os.path.join(dep_path__tools_chemistry, "libthermochemistry.so")
new_fincalc_mod_path = os.path.join(dep_path__modelling_fin, "calculation_engines.so")
new_des_mod_path = os.path.join(dep_path__modelling_fin, "des.so")
new_tax_mod_path = os.path.join(dep_path__modelling_fin, "tax.so")
new_stock_calc_mod_path = os.path.join(dep_path__modelling_stock, "calculation_engines.so")
new_stock_des_mod_path = os.path.join(dep_path__modelling_stock, "des.so")
new_business_mod_path = os.path.join(dep_path__modelling_business, "business.so")

call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN' " + new_core_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_stoichiometry_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_lib_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_fincalc_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_des_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_tax_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_stock_calc_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_stock_des_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../core:$ORIGIN/financial:$ORIGIN/stock' "+ new_business_mod_path], shell=True)

print('COPY REPORTS')
shutil.copy(r"../../src/auxi4py/modelling/financial/reporting/balance_sheet_report.py", dep_path__modelling_fin)
shutil.copy(r"../../src/auxi4py/modelling/financial/reporting/income_statement_report.py", dep_path__modelling_fin)
shutil.copy(r"../../src/auxi4py/modelling/financial/reporting/financial_transactions_report.py", dep_path__modelling_fin)
shutil.copy(r"../../src/auxi4py/modelling/financial/reporting/classes_report.py", dep_path__modelling_fin)

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
                "auxi.modelling", "auxi.modelling", "auxi.modelling.financial", "auxi.modelling.stock", "auxi.simulation",
                "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*', '*.a', '*.dll', '*.pyd'],
                    'auxi.modelling.financial': ['*.a', '*.so*', '*.dll', '*.pyd', '*_report.py'],
                    'auxi.modelling.stock': ['*.a', '*.so*', '*.dll', '*.pyd', '*_report.py'],
                    'auxi.modelling': ['*.a', '*.so*', '*.dll', '*.pyd', '*_report.py'],
                    'auxi.simulation': ['*.py', r'io/*'],
                    'auxi.tools.chemistry': ['*.so*', '*.a', '*.dll', '*.pyd', r'data/*']}#,
     #               'auxi' : [r'datafiles/*']}
)

print("Done")
