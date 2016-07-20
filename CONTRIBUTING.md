# How to Contribute to `auxi`

`auxi` is a community-driven open-source project. For the software to grow and
become more powerful, the community must be able to contribute. This will help
`auxi` to help the community more.

Members of the community will only contribute if it is clear how to do this,
and if it is easy to contribute. This document explains how you can become an
`auxi` contributor.

If you need any help regarding your contribution, you may visit
[#auxi-za forum](https://groups.google.com/forum/#!forum/auxi-za)


## Adhering to Standards and Procedures
Getting people to work together to achieve a common goal is not always easy, but it is so worth while when it is successful. If `auxi` is to have any chance of succeeding, and help us all out, we need to work according to a common set of standards and procedures. All these things are open for debate on the [#auxi-za forum](https://groups.google.com/forum/#!forum/auxi-za). If things are not working well, we discuss them, and make them better.

So, if you do want to contribute, please familiarise yourself with the details in the system documentation (README.md, ROLES.md, STANDARDS.md, CONTRIBUTING.md, RELEASING.md) in the root of the GitHub repository, and stick to the standards, procedures and other guidelines provided.


## GitHub Account
`auxi` is hosted on GitHub, and to contribute, you need to create a
[GitHub account](https://github.com/signup/free) if you do not already have one.


## Issue Contributions
The simplest way to contribute to `auxi` is to raise an issue, especially if you are not confident enough to contribute code. Issues are used for the following scenarios:

* Bugs/problems

   If you are using `auxi`, and something is not working, or it is failing, or it is creating a problem, you can submit an issue.

* Enhancement requests

   If you have an idea of somethign new that could improve `auxi`, or of some changes that would make it better, you can also submit an issue.

### Content
An issue must be properly documented to enable other contributors and maintainers to understand it clearly, and to implement code that will effectively address the issue. A submitted issue must provide the following information:

* System Details

   If your issue is a bug or problem, you need to clearly specify the `auxi` version that you are working with, the Python version that you are working with, and the details of the operating system that you are working on. (Only required for bugs.)

* Background

   Write some background about the issue to provide some perspective and to put other `auxi` project members in the picture. (This is required for all issues.)

* Purpose

   Write a clear, compact statement to indicate what the purpose of this issue is. Remember, an issue ultimately results in changes to the `auxi` code and documentation. Think about this when writing the purpose. (This is required for all issues.)

* Approach

   If you are able, propose an approach to address the issue. (This is optional for the initial submission of an issue, but it must be provided before a branch will be created to address the issue.)

* Scope

   If you are able, you can provide details of all the items that must be addressed to completely address the issue. (This is optional for the initial submission of an issue, but it must be provided before a branch will be created to address the issue.)

Here is an example of the markdown text of an empty issue:

```
### System Details
auxi version:   <<add your auxi verion here>>
Python version: <<add your Python version here>>
OS details:     <<add your operating system details here>>

### Background
<<add your issue background here>>

### Purpose
<<add your issue purpose here>>

### Approach
<<add your proposed approach to address the issue here>>

### Scope
<<specify the scope of items that must be completed here>>
```

When opening new issues or commenting on existing issues on this repository, please make sure discussions are related to concrete technical issues with the `auxi` software and documentation.


### Procedure
To submit an issue, follow these steps:

1. Open a ticket for your issue on the central `auxi` repository on GitHub. (required)
2. Write system details if your issue is a bug. (required for bug)
3. Write background about your issue. (required)
4. Write a purpose statement for the issue. (required)
5. Propose an approach to address the issue. (optional for initial submition)
6. Specify the scope of the issue. (optional for initial submition)
7. Submit the issue on Github. (required)


## Code Contributions
If you are able to, you can write your own code to address an issue that you have submitted, or one that someone else has submitted. This is where the real fun starts, and where you can really help out. In this case 'code' refers to Python code, test code, examples Jupyter notebooks and user documentation. Whatever you are comfortable with, please dig in and make `auxi` better.


### Step 0: Fork and Clone the `auxi` Repository
You will only need to do this once, hence the number zero.

Contributors cannot work on the central `auxi` repository directly, and need to make their own fork to work on. You can do this on GitHub, from the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) by simply clicking on the "Fork" button and following the instructions. Remember, you need a GitHub account to do this.

Next, you need to clone the `auxi` repository to your local computer:

```
git clone https://github.com/your-username-here/auxi.0
cd auxi.0
git remote -v
```

The last instruction lists the remote repositories that are linked to the local repository on your computer. There is currently only one, which is the fork that you made. We need to add the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) to the list of remotes.

```
git remote add upstream https://github.com/Ex-Mente/auxi.0
git remote -v
```

Now you should have two remote repositories connected. The first is called `origin`, which is your fork, and the second is called `upstream` and refers to the central `auxi` repository.


### Step 1: Finalise the Issue
Before starting implementation of an issue, it is very important that the issues is finalised. Read through the issue carefully, and make sure that all the headings are populated, even the optional ones like approach and scope.

Communication is very important at this point. Use issue comments to correspond with other `auxi` team members to make sure that you have the best possible starting point, and buy-in from as many members as possible. Use the forum as well to keep other members aware of what you are doing.


### Step 2: Create Local Branch
Now we need to create a branch in our local git repository. We will assume that we are working on issue 999 for this discussion. Do the following:

```
git checkout -b issue-999
```

### Step 3: Pull from Upstream
You should now be on the branch called issue-999 in your local repository. We now need to pull the latest information from the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) in this branch. You can be facing one of two scenarios at this stage:

* Issue branch available

   If an issue-99 branch has already been created in the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), you do the following:

```
git pull upstream issue-999
```

   This makes sure that you have the latest information to do your implementation on.

* Issue branch NOT available

   If an issue-99 branch


### Step 4: Implementation
### Step 5: Rebase
### Step 6: Push to Origin
### Step 7: Create Pull Request
### Step 8: Respond to Pull Request Feedback


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
