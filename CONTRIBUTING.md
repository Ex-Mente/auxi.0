# How to contribute

New functionality and third-party patches are necessary to help auxi make a
difference. We can't test for all the different configurations and usages in
auxi. auxi development is for the community, and thus, new features needed by
the community helps for auxi make the difference.

We want to keep it as easy as possible to contribute features and changes
that will help you. In order to help us maintain auxi, our contributors need
to follow a few guidelines.

If you need any help regarding your contribution, you may visit
[#auxi-za mailing list](https://groups.google.com/forum/#!forum/auxi-za)

## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free)
* Submit a ticket for your issue, assuming one does not already exist.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you specify the version of auxi that has this issue.
  * Make sure you specify your OS, its architecture (32 or 64bit).
  * Make sure you specify the version of Python you are using.
* Fork the repository on GitHub

## Making Changes

* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target release branches if you are certain your fix must be on that
    branch.
  * To quickly create a topic branch based on master; `git checkout -b
    fix/master/my_contribution master`. Please avoid working directly on the
    `master` branch.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.

````
    (#32) Add contributor guidelines

    Currently contributors have no idea how to contribute, what our coding
    style standards is, that tests needs to be created, and that all tests
    should pass before creating a pull request.
    This is likely to limit the number and quality of contributions.
    This document guides contributions on how to contribute as well as our
    quality requirements.
````

* Make sure that all your code follows the PEP-8 styling standard.
* Each python file should adhere to the following format:

```
    #!/usr/bin/env python3
    """
    This module description.
    """

    import built-in python modules

    import third-party modules

    import auxi modules


    __version__ = '0.2.3'
    __license__ = 'LGPL v3'
    __copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
    __author__ = 'Christoff Kok, Johan Zietsman'
    __credits__ = ['Christoff Kok', 'Johan Zietsman']
    __maintainer__ = 'Christoff Kok'
    __email__ = 'christoff.kok@ex-mente.co.za'
    __status__ = 'Planning'

    code
```
* Make sure you have added the necessary tests for your changes.
* Run src/tests.py to make sure taht nothing is broken by your changes.


## Submitting Changes

* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the repository in the Ex-Mente organization.
* The core team looks at Pull Requests on a regular basis.

# Additional Resources

* [auxi youtube channel](https://www.youtube.com/channel/UCdklSCJ8S9wFyayLAO7iINQ)
* [General GitHub documentation](https://help.github.com/)
* [GitHub pull request documentation](https://help.github.com/send-pull-requests/)
* [#auxi-za mailing list](https://groups.google.com/forum/#!forum/auxi-za)
