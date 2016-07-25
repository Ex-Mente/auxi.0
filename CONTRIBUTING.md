# How to Contribute to `auxi`

* [Adhering to Standards and Procedures](#adhering-to-standards-and-procedures)
* [GitHub Account](#github-account)
* [Issue Contributions](#issue-contributions)
  * [Content](#content)
  * [Procedure](#procedure)
* [Code Contributions](#code-contributions)
  * [Step 0: Fork and Clone the `auxi` Repository](#step-0-fork-and-clone-the-auxi-repository)
  * [Step 1: Finalise the Issue](#step-1-finalise-the-issue)
  * [Step 2: Create Local Branch](#step-2-create-local-branch)
  * [Step 3: Pull from Upstream](#step-3-pull-from-upstream)
  * [Step 4: Implementation](#step-4-implementation)
  * [Step 5: Rebase](#step-5-rebase)
  * [Step 6: Push to Origin](#step-6-push-to-origin)
  * [Step 7: Create Pull Request](#step-7-create-pull-request)
  * [Step 8: Respond to Pull Request Feedback](#step-8-respond-to-pull-request-feedback)
* [Hotfix Contributions](#hotfix-contributions)
* [Developer's Certificate of Origin 1.1](#developers-certificate-of-origin-11)


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
If you are able to, you can write your own code to address an issue that you have submitted, or one that someone else has submitted. This is where the real fun starts, and where you can really help out. In this case 'code' refers to Python code, test code, examples in the form of Jupyter notebooks and user documentation. Whatever you are comfortable with, please dig in and make `auxi` better.


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

   If an issue-99 branch does not exist in the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), you do the following:

```
git pull upstream develop
```

### Step 4: Implementation
Now you are ready to get rolling. You can write code, tests, documentation, examples, and user docs to your hearts content. Make sure you adress all the aspects of the issue as thoroughly as possible. Also, make sure that everything you do are in line with the `auxi` standards and procedures.

You can add and submit your changes using the `git add` and `git commit` commands. Once you have done that, make sure that you comply with the standards, and make sure that your tests all run successfully.


### Step 5: Rebase
While you have been having fun with the implementation, someone else may have made some changes to your source branch (the one you pulled from. Before we start transferring your contribution to the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), we need to rebase so that we are working off an up-to-date version of the source branch. We need to cater for two scenarios again.

* Issue branch available

   If an issue-99 branch was already available in the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), you do the following:

```
git pull --rebase upstream issue-999
```

   This makes sure that you have the latest information to do your implementation on.

* Issue branch NOT available

   If an issue-99 branch did not exist in the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), you do the following:

```
git pull --rebase upstream develop
```

After rebasing, run your tests again to make sure everything is still OK. If some problems occur, fix them and commit to your local repository before continuing.


### Step 6: Push to Origin
Now we are ready to push your work to your online fork repository. This is how we do it:

```
git push origin issue-999
```

If the issue-999 branch did not already exist in your fork repository, it will be created.


### Step 7: Create Pull Request
Now you want to request the `auxi` maintainers to pull your code contribution from your for repository to the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0). We do this with a 'pull request'. Here is the procedure:

1. Open your fork GitHub repository in your browser.
2. Select the issue-999 branch.
3. Click the 'New pull request' button.
4. In the comment box, write "closes issue #999".
5. Click the "Create pull request button".

Great. Things are out of your hands for now. The continuous integration system should give you feedback if your contribution does not comply with certain standards. In such a case your pull request will not be accepted. Fix all issues and try again.


### Step 8: Respond to Pull Request Feedback
The `auxi` maintainers may respond to your pull request by giving you feedback about things you need to fix. Do this promptly and inform them of the progress so that they can accept your pull request as quickly as possible, and merge it into the source branch in the central repository. They may also request you to create a pull request to a different issue branch, if the issue branch did not exist before.


## Hotfix Contributions
The purpose of a hotfix is to make a quick revision on an auxi release, without waiting for the next full-scale release to be completed.

Hotfix contributions work the same as code contributions, with one important difference. We do code contributions based on the develop branch, but hotfix contributions based on the master branch. You can therefore follow the instructions under [Code Contributions](#code-contributions), but simply replace references to the develop branch, with references to the master branch.


## Developer's Certificate of Origin 1.1
By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or

(b) The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or

(c) The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.

(d) I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.
