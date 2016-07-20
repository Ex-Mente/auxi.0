# `auxi` Project Standards

This document describes the standards that are used in the `auxi` project. The purpose of enforcing these standards is to improve clarity, quality and productivity.


## Functional Units
Each feature in `auxi` that can stand alone in terms of functionality, is called a functional unit. For example, a new slag viscosity model would constitute a functional unit (FU).

Functional units are not just about code. For the complete implementation of an FU, the following components must be created:
* Code

   This is the most obvious component, and since `auxi` is a Python package, some Python code should be written. The purpose of this code is to implement the details of the functional unit so that it can be made available to `auxi` users.

   This code can be added to existing files, or it may require the creation of new packages and modules. This depends on the nature of the new feature.

* Tests

   All code added to `auxi` must be thoroughly tested and covered by a set of unit tests. These unit tests are implemented in separate `_test.py` files. New test files should also be called from the global `tests.py` file located in the root of the `auxi` package.

* Examples

   All functional units must be thoroughly demonstrated to users by using Jupyter Notebook examples.

* User Documentation

   All functional units must be introduced and described in the `auxi` user documentation.


## Code Files

### Code Format

All code files will be checked against Python's PEP8 style guide during the continous integration process. If a code file does not comply with this standard, it will not be accepted into the `auxi` develop or main branches.

### File Header
Each code file must have a header formatted as follows:

```
#!/usr/bin/env python3
"""
<<Add a clear description of the module here.>>
This module ...
"""

import <<import built-in Python modules here>>

import <<import third-party modules here>>

import <<import auxi modules here>>


__version__ = '0.2.3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2015-2016, Ex Mente Technologies (Pty) Ltd'
__author__ = '<<add the list of authors here>>'
__credits__ = [<<add the list of credits here>>]
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'

<<Add your code from this point.>>
```

### File Footer
Each code file must have a fotter as follows. This makes it possible to run code tests easily while developing.

```
if __name__ == "__main__":
    import unittest
    from <<Add the relevant test module(s) here.>> import *
    unittest.main()
```

### Documentation
All code files must be completely documented so that this information can be extracted by Sphinx to generate a complete set of API documentation in the user documentation. This following items must be documented in each code file:

* Module

   A module must be clearly described with a docstring at the top of the module.

```
"""
This module provides tools for solving flow sheet models.
"""
```

* Public variables and constants

   A single-line docstring must follow immediately after a public variable. If the variable has units, the units must be stated in square brackets at the start of the docstring.

```
epsilon = 1.0e-3
"""[kg/h] Convergence criterion when solving feed rates in a flow sheet."""
```

* Public functions

   A function, its parameter(s) and return value(s) must be documented with a docstring. The function description must be written as if giving an instruction to the module (e.g. Identify the next node in the flow sheet to execute.", and not as a description (e.g. This function identifies the next node in the flow sheet to execute.".

```
def identify_next_node(nodes, direction):
    """
    Identify the next node in the flow sheet to execute.

    :param nodes: The list of nodes in the flow sheet.
    :param direction: The direction in which the flow sheet is being solved, e.g. forward or reverse.

    :returns: The next node to execute.

    <<Add further documentation details here.>>
    """

    <<Function code goes here.>>
```

* Public classes

   Classes must be documented with a docstring following the class declaration line. Constructor details must also be incorporated into this docstring.

```
class Model(Object):
    """
    Base class of models that describe the variation of a specific material
    physical property.

    :param material: the name of the material being described, e.g. "Air"
    :param proprty: the name of the property being described, e.g. "density"
    :param symbol: the symbol of the property being described, e.g. "rho"
    """

    def __init__(self, material, proprty, symbol):
        self.material = material
        """The name of the material to which this model applies."""
        self.property = proprty
        """The name of the property being described by this model."""
        self.symbol = symbol
        """The symbol used to represent the property being described."""
```

* Public class attributes

   Public class attributes should be documented with a docstring directly below where the attribute is created. This is demonstrated in the previous code snippet. If the attribute has units, the units must be stated in square brackets at the start of the docstring, similar to public variables.

* Public class methods

   A method, its parameter(s) and return value(s) must be documented with a docstring. The method description must be written as if giving an instruction to the module (e.g. Calculate the property value.", and not as a description (e.g. This function calculates the property vlaue.".

```
        def calculate(self, **state):
        """
        Calculate the property value.

        :param **state: The material state

        :returns: Property value.
        """

        <<Add your method code here.>>
```


## Test Files
Tests are executed during continuous integration. If any test fails, the pull request will not be accepted into the `auxi` develop or main branches.

### Code Format
Test files have exactly the same formatting requirements as code files.

### File Header
Test files have exatctly the same header requirements as code files.

### File Footer
Test files must have the following footer:

```
if __name__ == '__main__':
    unittest.main()
```

### Documentation
Test modules, classes and methods must be documented in the same way used for code. All descriptions must clearly state the testing purpose of the class or method.


## Examples
All examples must be implemented in Jupyter notebooks. All aspects of a functional unit must be covered by an example so that users can clearly see how the FU can be used.


## User Documentation
User documentation must be kept up to date with the addition of each functional unit. The purpose of the user documentation is to provide background and perspective to users, which cannot be sensibly incorporated into code documentation.
