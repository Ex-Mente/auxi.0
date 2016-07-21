# How to Make an `auxi` Release

A high quality release is of utmost importance to `auxi`. This includes well tested code, good documentation and good examples. To help make releases smooth, easy and as bug free as possible we have automation scripts and procedures in place. The release procedure is explained below.


## Git Branching Strategy
The two main branches in `auxi` are `develop` and `master`. The `master` branch contains the latest release available on PyPi (pip install auxi). The `develop` branch contains the most up-to-date work that includes all the additions and changes from completed issue branches merged into `develop` since the latest release.

For a new release, a release branch must be created from the develop branch. Once this is done, the release is feature frozen, and it will not be influenced if further issue branches are merged into `develop`. To maintain this feature fronzen status, the release branch must not be updated or rebased from `develop`. The release branch must be tested and checked against `auxi`'s standards. (See the STANDARDS.md file) Once all bugs and shortcomings are fixed, the release branch may be merged into the develop and master branches. Each release on the master branch must be tagged with the release number.


## Release Procedures
A release consists of one or more release candidates. Each release candidate represents a deployment on PyPi and addresses bugs and corrections discovered while testing a previous release candidate. A release candidate is denoted by the release version number and a release candidate suffix, e.g. "0.3.0rc1".

#### Step 1: Create an Issue
Create a issue for the new release. As specified in the CONTRIBUTING.md file, the issue should have a `background` and `purpose`. Specifying `scope` is important as well. Make sure that the purpose for this release comes through clearly. Specify the addressed issues highlights in the `scope`.

#### Step 1: Create Release Branch
When making a release the first thing that needs to be done is to create a new release branch from `develop`.

First, create the release branch on the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) from `develop`.
The name of the release branch should be the version number of the release e.g. "0.3.0".

On your local repository, create the release branch and update it from the central repository:

```
git checkout -b <<release number>>
git pull upstream <<release number>>
```


#### Step 2: Increment the version
Under the auxi.0/scripts folder, run the update_version.py script. You will be prompted for the new version number.
Make the version the release number plus 'rc1' (release candidate 1) e.g. "0.3.0rc1". For each new release candidate, increase the release candidate number. e.g. if you are repeating step two the new version number should be "0.3.0rc2".


#### Step 3: Deploy the release candidate to PyPi
Navigate to the setup you created. Go to auxi.0/dist, extract the .zip or .tar.gz release created e.g. "auxi-0.3.0rc1.tar.gz".
In your command line shell, navigate into the extracted folder and run the following command:

```
pip setup.py sdist upload
```

You will be prompted for a PyPi username and password. Use Ex Mente Dev's PyPi username and password (You can find it in the svn repository's passwords file). This will create the `auxi` distribution and upload it to PyPi. 

#### Step 4: Test the deployment
Run `auxi`'s tests, make sure everything is working. (First make sure that you uninstall any previous versions of auxi)

```
pip install auxi==<<release candidate version e.g. "0.3.0rc1">>
```

Run auxi's test file. e.g.
```
python /usr/local/lib/python3.4/dist-packages/auxi-0.2.3-py3.4.egg/auxi/test.py
```

If there are any issues, fix it, and repeat steps 2,3 and 4 until all issues has been fixed.

#### Step 5: Finalize release
The release candidate phase is over and we can move on to create a new release on `master`. Update the version number to the release number (without any suffixes) e.g. "0.3.0". Commit and push your changes.

#### Step 5.1 Update Release Notes
Update the `RELEASE-NOTES.md` file by inserting the new release's notes at the top of the file in the format as specified in the file. Make sure that you list all the issues that this release addressed.

#### Step 6: Push to your online fork repository
Commit all you changes then push them to your online fork repository. 

```
git commit -m "Release <<release number>>. This closes issue #<<issue number>>" -a
git push origin <<release number>>
```

The last commit is an important point in our git History. We will mark this by creating a tag of the commit.
```
git tag -a Tag-<<release number>>
git push origin Tag-<<release number>>
```

#### Step 7: Update [central `auxi` repository](https://github.com/Ex-Mente/auxi.0)'s release branch
Create a pull request from your online fork repository's release branch to the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) release branch.

In the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0), approve and merge the release branch ONLY if all of Travis.CI's checks passed. Else, fix the issues and go back to step 2.

#### Step 8: Merge into `develop` and `master`
The release is now ready to be deployed the world. Merging the release into master will automatically instruct Travis.CI to create a PyPi deployment for `auxi`. We will also have to merge it back into `develop`.

In the [central `auxi` repository](https://github.com/Ex-Mente/auxi.0) create a pull request from the release branch to  `develop`. Approve and merge the pull request. Now, do the same for `master`.

#### Step 9: Test the deployment
Install `auxi` and run the tests.

```
pip install auxi
```

Make sure that the version number specified in the output corresponds to the new release's version. 

Run `auxi`'s test file. e.g.
```
python /usr/local/lib/python3.4/dist-packages/auxi-0.2.3-py3.4.egg/auxi/test.py
```

Any further issues discovered on this release will have to be treated as `hotfixes`. See the CONTRIBUTING.md file on how to create a hotfix. 
