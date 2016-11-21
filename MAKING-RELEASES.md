# How to Make an `auxi` Release

A high quality release is of utmost importance to `auxi`. This includes well tested code, good documentation and good examples. To help make releases smooth, easy and as bug free as possible we have automation scripts and procedures in place. The release procedure is explained below.


## Git Branching Strategy
The two main branches in `auxi` are `develop` and `master`. The `master` branch contains the latest release available on PyPi (pip install auxi). The `develop` branch contains the most up-to-date work that includes all the additions and changes from completed issue branches merged into `develop` since the latest release.

For a new release, a release branch must be created from the develop branch. Once this is done, the release is feature frozen, and it will not be influenced if further issue branches are merged into `develop`. To maintain this feature frozen status, the release branch must not be updated or rebased from `develop`. The release branch must be tested and checked against `auxi`'s standards. (See the STANDARDS.md file) Once all bugs and shortcomings are fixed, the release branch may be merged into the develop and master branches. Each release on the master branch must be tagged with the release number.


## Release Procedures
A release consists of one or more release candidates. Each release candidate represents a deployment on PyPi and addresses bugs and corrections discovered while testing a previous release candidate. A release candidate is denoted by the release version number and a release candidate suffix, e.g. "0.3.0rc1".

#### Step 1: Create an Issue
Create a issue for the new release. As specified in the CONTRIBUTING.md file, the issue should have a `background` and `purpose`. Specifying `scope` is important as well. Make sure that the purpose for this release comes through clearly. Specify the addressed issues highlights in the `scope`.

#### Step 2: Create Release Branch
When making a release the first thing that needs to be done is to create a new release branch from `develop`.

First, create the release branch on the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) from `develop`.
The name of the release branch should be the version number of the release e.g. "0.3.0".

On your local repository, create the release branch and update it from the central repository:

```
git checkout -b <<release number>>
git pull upstream <<release number>>
```


#### Step 3: Increment the version
Under the auxi.0/scripts folder, run the update_version.py script. You will be prompted for the new version number.
Make the version the release number plus 'rc1' (release candidate 1) e.g. "0.3.0rc1". For each new release candidate, increase the release candidate number. e.g. if you are repeating step two the new version number should be "0.3.0rc2".

#### Step 4: Build deployment
Under the auxi.0/scripts folder, run the build_and_deploy.py script

```
sudo sh build_and_deploy.sh
```

This will build your setup as well as deploy it to your python distribution.

Test the release by running `auxi`'s test file. e.g.

```
python /usr/local/lib/python3.4/dist-packages/auxi-0.3.0rc1-py3.4.egg/auxi/test.py
```

Fix any issues you may find and repeat this step until all issues has been fixed.

#### Step 5: Deploy the release candidate to PyPi
Navigate to the deployment you created. Go to auxi.0/dist, extract the .zip or .tar.gz release created e.g. "auxi-0.3.0rc1.tar.gz".
In your command line shell, navigate into the extracted folder and run the following command:

```
python setup.py sdist upload
```

You will be prompted for a PyPi username and password. Use Ex Mente Dev's PyPi username and password (You can find it in the svn repository's passwords file). This will create the `auxi` distribution and upload it to PyPi.

#### Step 6: Test the deployment
Run `auxi`'s tests, make sure everything is working. (First make sure that you uninstall any previous versions of `auxi`)

```
pip install auxi==<<release candidate version e.g. "0.3.0rc1">>
```

Run auxi's test file. e.g.
```
python /usr/local/lib/python3.4/dist-packages/auxi-0.3.0rc1-py3.4.egg/auxi/test.py
```

Test `auxi` both on Windows and on Linux. Make sure all the tests pass on both platforms.

If there are any issues, fix it, and repeat steps 3,4, 5 and 6 until all issues has been fixed.

#### Step 7: Finalize release
The release candidate phase is over and we can move on to create a new release on `master`. Update the version number to the release number (without any suffixes) e.g. "0.3.0".

#### Step 7.1 Update Release Notes
Update the `RELEASE-NOTES.md` file by inserting the new release's notes at the top of the file in the format as specified in the file. Make sure that you list all the issues that this release addressed.

#### Step 8: Push to your online fork repository
Commit all you changes then push them to your online fork repository.

```
git commit -m "Release <<release number>>. This closes issue #<<issue number>>" -a
git push origin <<release number>>
```

#### Step 9: Update [central `auxi` repository](https://github.com/Ex-Mente/auxi.0)'s release branch
Create a pull request from your online fork repository's release branch to the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) release branch.

In the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), approve and merge the release branch ONLY if all of Travis.CI's checks passed. Else, fix the issues and go back to step 2.

#### Step 10: Merge into `develop` and `master`
The release is now ready to be deployed the world.  We will have to merge the release branch back into `develop` and merge it into `master`.

In the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) create a pull request from the release branch to  `develop`. Approve and merge the pull request. Now, do the same for `master`.

#### Step 11: Create a new release
Creating a new release will add a tag to the release which will automatically instruct Travis.CI to create a new PyPi deployment for `auxi`.

To create a on GitHub release, follow these instructions:

* Go to: https://github.com/Ex-Mente/auxi.0
* There is a `releases` link, click on it.
* Click on the `Draft a new release` button.
* Insert the new tag number specified by a `v` plus the `release number` e.g. `v0.3.0`.
* Make sure that the Tag's target is the master branch.
* Give the release a title: `Release ` plus the `release number`. e.g. `Release v0.3.0`
* Add the release notes to the description.
* Click on the `Publish release` button.

GitHub will now create a tag on the last commit on `master`. Travis.CI will detect it and create and publish a new PyPi deployment for `auxi`.

#### Step 12: Test the deployment
Install `auxi` and run the tests.

```
pip install auxi
```

Make sure that the version number specified in the output corresponds to the new release's version.

Run `auxi`'s test file. e.g.
```
python /usr/local/lib/python3.4/dist-packages/auxi-0.3.0rc1-py3.4.egg/auxi/test.py
```

Any further issues discovered on this release will have to be treated as `hotfixes`. See the CONTRIBUTING.md file on how to create a hotfix.

#### Step 13: Update the `readthedocs` documentation
The `readtehdocs` documentation should be build and deployed again.

* Go the https://readthedocs.org and log in.
* Go to your auxi project, and at `Build`, at the dropdown, make sure that `latest` is selected.
* Press on the `Build` button below the dropdown.
* Go to the `Build` tab and monitor the build until it has passed.
* Got to http://auxi.readthedocs.io/en/latest and make sure any documentation changes appears. Also check that the `api` generated. If there where any changes to the api, confirm that the changes are in the api documentation.
