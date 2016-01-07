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
doc_path = os.path.join(dep_path_auxi, 'doc')

dep_path_thermo_data_files = os.path.join(dep_path__tools_chemistry, 'data')

boost_py_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_python-py34.so.1.54.0"
boost_dt_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.54.0"
boost_fs_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.54.0"
boost_sy_lib_path = "/usr/lib/x86_64-linux-gnu/libboost_system.so.1.54.0"

# delete old files from package structure and add new ones
print("REMOVE OLD FILES")
remove_old_files(dep_path_auxi)
deleteFileOrFolder(dep_path_thermo_data_files)
deleteFileOrFolder(doc_path)
print()

core_mod_path = os.path.join(project_path, r"../../src/auxi4py/core/bin/gcc-c++11/debug/core.so")
stoi_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/stoichiometry/bin/gcc-c++11/debug/stoichiometry.so")
thermochem_mod_path = os.path.join(project_path, r"../../src/auxi4py/tools/chemistry/thermochemistry/bin/gcc-c++11/debug/thermochemistry.so")

core_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/core/bin/gcc-c++11/debug/libcore.so"),
boost_py_lib_path,
boost_dt_lib_path,
boost_fs_lib_path,
boost_sy_lib_path,
core_mod_path
]

stoi_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/stoichiometry/bin/gcc-c++11/debug/libstoichiometry.so"),
boost_fs_lib_path,
stoi_mod_path
]

thermochem_dependencies_paths = [
os.path.join(project_path, r"../../src/auxi/tools/chemistry/thermochemistry/bin/gcc-c++11/debug/libthermochemistry.so"),
thermochem_mod_path
]


print('COPY DEPENDENCIES')
for dep in core_dependencies_paths:
    shutil.copy(dep, dep_path__core)
for dep in stoi_dependencies_paths:
    shutil.copy(dep, dep_path__tools_chemistry)
for dep in thermochem_dependencies_paths:
    shutil.copy(dep, dep_path__tools_chemistry)

new_core_mod_path = os.path.join(dep_path__core, "core.so")
new_stoichiometry_mod_path = os.path.join(dep_path__tools_chemistry, "stoichiometry.so")
new_thermochem_mod_path = os.path.join(dep_path__tools_chemistry, "thermochemistry.so")
new_thermochem_lib_path = os.path.join(dep_path__tools_chemistry, "libthermochemistry.so")

print("  patchelf")
'''call([patchelf_path, "--set-rpath", "'$ORIGIN'", new_core_mod_path])
call([patchelf_path, "--set-rpath", "'$ORIGIN:$ORIGIN/../../core'", new_stoichiometry_mod_path])
call([patchelf_path, "--set-rpath", "'$ORIGIN:$ORIGIN/../../core'", new_thermochem_mod_path])
call([patchelf_path, "--set-rpath", "'$ORIGIN:$ORIGIN/../../core'", new_thermochem_lib_path])'''
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN' " + new_core_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_stoichiometry_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_mod_path], shell=True)
call(["sudo " + patchelf_path + " --set-rpath '$ORIGIN:$ORIGIN/../../core' "+ new_thermochem_lib_path], shell=True)


print('COPY DATA FILES')
thermo_data_files_path = r"../../src/auxi/tools/chemistry/thermochemistry/data/"
shutil.copytree(thermo_data_files_path, dep_path_thermo_data_files)

print('COPY DOCUMENTATION')
to_copy_doc_path = os.path.join(project_path, '../../doc/auxi4py/user/build/html')
shutil.copytree(to_copy_doc_path, doc_path)
#shutil.move(os.path.join(doc_html_path, 'auxipyUserDocumentation.pdf'), doc_path)

print()

# build the distribution
setup(name="auxi",
      version="0.0.0",
      description="auxi for Python",
      package_dir={'auxi': 'auxi'},
      packages=["auxi", "auxi.core", "auxi.tools", "auxi.tools.chemistry"],
      package_data={'auxi.core': ['*.so*'],
                    'auxi.tools.chemistry': ['*.so*', r'data/*']}#,
     #               'auxi' : [r'datafiles/*',
     #                         'doc/*.pdf', 'doc/html/*', 'doc/html/_static/*', 'doc/html/_sources/*']}
)

print("Done")
