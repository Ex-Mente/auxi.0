#!/usr/bin/env python3

import glob
import os

new_ver = input("Enter the new version number: ")

print("...")
print("Updating the version number to: " + new_ver)

# Find the previous version number:
with open('setup.py', 'r') as f:
    content = f.read()
    v_ix = content.index("version='") + 9
    v_ix_end = v_ix + content[v_ix:].index("'")
    old_ver = content[v_ix:v_ix_end]
    content = content[:v_ix] + new_ver + content[v_ix_end:]

# Update setup.py
print("Updating setup.py")
with open('setup.py', 'w') as f:
    f.write(content)

print("Old version = " + old_ver)

# Update the build scripts
for file in glob.glob("*.sh"):
    with open(file, 'r') as f:
        content = f.read()
        content = content.replace(old_ver, new_ver)
    with open(file, 'w') as f:
        f.write(content)

# Update all the 'src' dirs .py file's __version__ field.
for root, dirs, files in os.walk("../src"):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            print("Updating " + file_path)
            with open(file_path, 'r') as f:
                content = f.read()
                content = content.replace(
                    "__version__ = '" + old_ver + "'",
                    "__version__ = '" + new_ver + "'")
            with open(file_path, 'w') as f:
                f.write(content)

# Update the docs version
for root, dirs, files in os.walk("../doc"):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            print("Updating " + file_path)
            with open(file_path, 'r') as f:
                content = f.read()
                content = content.replace(
                    "copyright = '2015-2016, " + old_ver + "'",
                    "copyright = '2015-2016, " + new_ver + "'")
                content = content.replace(
                    "version = '" + old_ver + "'",
                    "version = '" + new_ver + "'")
                content = content.replace(
                    "release = '" + old_ver + "'",
                    "release = '" + new_ver + "'")
            with open(file_path, 'w') as f:
                f.write(content)
