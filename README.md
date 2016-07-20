Master:  [![Coverage Status](https://coveralls.io/repos/github/Ex-Mente/auxi.0/badge.svg?branch=master)](https://coveralls.io/github/Ex-Mente/auxi.0?branch=master)

Develop: [![Coverage Status](https://coveralls.io/repos/github/Ex-Mente/auxi.0/badge.svg?branch=develop)](https://coveralls.io/github/Ex-Mente/auxi.0?branch=develop)

# Welcome to the `auxi` GitHub repository!

## Introduction

`auxi` is a toolkit to help metallurgical process engineers with their day-to-day tasks. Many of the calculations that we do require things like molar masses, conversion of one compound to another using stoichiometry, enthalpy calculations, heat transfer calculations, mass balances, energy balances, etc. It is usually quite time consuming to get started with these calculations in a tool like Excel. `auxi` aims to save you time by making many of these calculations available from within Python.

We hope that `auxi` will help you spend less time focusing on searching for formulas and data, and setting up calculations, and more time on thinking about the problems that you need to solve with these calculations. Enjoy!

Here are some of the other `auxi` resources:
* documentation: http://auxi.readthedocs.io/en/latest/
* Youtube channel: https://www.youtube.com/channel/UCdklSCJ8S9wFyayLAO7iINQ
* Discussion forum: https://groups.google.com/forum/#!forum/auxi-za

To install auxi, use the following command:
```
pip install auxi
```


## Repository Overview

### Directory Structure
The repository contains the following top-level directories:
* root

   This directory contains the high-level system documentation such as this readme file, and other files that need to be easily accessible to contributors and maintainers. It also contains the `.gitignore` file to specify ignored files and patterns, and `.travis.yml` file to provide configuration details for the Travis.CI continuous integration tool.

* doc

   This directory currently contains the `auxi` user documentation. Detailed system documentation may be added later.

* scripts

   This directory contains scripts used to automate the build and release process.

* src

   This directory contains the source files of the Python package.


### High-level System Documentation
The `auxi` high-level system documentation consists of the following files:
* ROLES.md

   This document identifies the roles involved in the `auxi` project, and explains the responsibilities and access rights of each role.

* STANDARDS.md

   This document lists and explains the standards that are used in the `auxi` project. If you want to play along nicely when you contribute, you need to know and understand these.

* CONTRIBUTING.md

   This document explains exactly how you can contribute code to `auxi`.

* RELEASING.md

   This document explains how releases are done. Not everyone can do this, but it is important for everyone involved in the project to understand how this works.

* RELEASE-NOTES.md

   This document contains the details of what changed in each `auxi` release.
