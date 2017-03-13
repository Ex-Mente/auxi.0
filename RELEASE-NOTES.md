# `auxi` Release Notes
This file reports the details of each `auxi` release from newest to oldest.

## 0.3.5
There were also issues with `auxi`'s thermochemistry data file format that were fixed. The data files written by Compound.write() could not be read by load_data_auxi. The Rao and NIST data were also incorrectly formatted. These were all fixed.

## 0.3.4
In this release a large number of changes made by Carl Sandrock and other authors were added.

## 0.3.3
In this release new Jupyter notebooks were added, the thermo data file issue on Windows fixed, readtehdocs documentation fixed and the release procedure was updated.

### Release Details
Date:       05 August 2016

Maintainer: Christoff Kok (christoff.kok@ex-mente.co.za)

### Issues Addressed
* Added Jupyter notebooks for auxi.tools.chemistry.stoichiometry (#118)
* Added Jupyter notebooks for auxi.tools.chemistry.thermochemistry (#119)
* Fix RHO thermo data Compound\_CO, Co Windows naming issue. The Compound\_Co file is now named Compound_Cobalt. (#156)
* Fixed an issue where the API api documentation was empty on readtehdocs. (#157)
* Updated MAKE-RELEASES.md to add the documentation release procedure. (#158)

## 0.3.2
In this release a couple of documentation changes where made and a modules test improved.

### Release Details
Date:       29 July 2016

Maintainer: Christoff Kok (christoff.kok@ex-mente.co.za)

### Issues Addressed
* Adding of test coverage checking on Travis.CI (#77)
* (bug) Fixed the PyPi description format issue. (#99)
* Added the procedure for testing different platforms to MAKE-RELEASES.md (#96)
* (bug) Updated the Travis.CI deploy trigger procedure to MAKE-RELEASES.md (#100)
* (bug) Fixed auxi's docs on readthedocs which failed to build. (#109)
* Improved test coverage in auxi.tools.chemistry.stoichiometry. (#113)

## 0.3.1
In this release a hotfix was made to make Windows deployment work (#103).

### Release Details
Date:       22 July 2016

Maintainer: Christoff Kok (christoff.kok@ex-mente.co.za)

### Issues Addressed
* 0.3.0 Windows deployment fails. (#103)


## 0.3.0
In this release a significant number of additions were made. These included:
* added a material physical property package under tools;
* added a transport phenomena package under tools (#57);
* added a front page to the GitHub repository (#69);
* cleaned up the root directory of the repository (#70);
* added system documentation to make contributions easy (#33);

### Release Details
Date:       21 July 2016

Maintainer: Christoff Kok (christoff.kok@ex-mente.co.za)

### Issues Addressed
* added a material physical property package under tools;
* added a transport phenomena package under tools (#57);
* added a front page to the GitHub repository (#69);
* cleaned up the root directory of the repository (#70);
* added system documentation to make contributions easy (#33);
