Title: Installing python packages from a git private repo using Pipenv
Date: 2024-09-09 00:00
Modified: 2024-09-09 00:00
Category: Blog
Tags: pipenv, github, python, package
Slug: pipenv-github-private
Authors: Odolix
Summary: Feedback on using dependencies from a private Github repo in a python project

## Installing python packages from a git private repo using Pipenv

Pipenv is a great tool when it comes to package management in Python. But things get les fun when it comes to managing dependencies with private repositories

I built a set of libraries to use in a professional environment. 
You can set up a private Pypi repository with authentication to put your private packages, but that requires to install and maintain a server, with secured authentication, and a proper certificate. 

That can be a hassle when you dev environment becomes large, with several languages and frameworks. 

An alternative is to use a Github private repository. 

### Use a Github repo as a package source


To add a Github package to a pipenv project, you can add the following line in your Pipfile:

> _package_name_ = {git = "https://{github_repo_url}", editable = true, ref = "master"}

Where _package_name_ is the name of your package, _editable_ is to install the package in the _src_ folder of your pipenv virtualenv and avoid caching, and _ref_ is the branch you want to use

You can also add it manually by typing 

``` pipenv install -e git+https://github_repo_url@branch#egg=package_name ```

### Connect to a private repository

Now, that works for non private repositories. 

If you want to access private a private repository, you need to generate a token in  [Github > settings > Developer settings](https://github.com/settings/tokens)

then change the repo URL to 
> https://**token**@github.com/account/repo.git

You can add this token to your environment variables and set pipenv or git to use it.

``` export GITHUB_TOKEN = **token** ```

``` git clone https://${GITHUB_TOKEN}@github.com/account/repo.git ```

### Deploy dependencies

Now let's make it harder and install private packages that depend on private packages.

To setup public dependencies of a dependency, I use the setup.py script. Pipenv will compile a package based on that script and install it in the virtualenv. 

To setup private dependencies of a private dependency, so far, the easiest way I've found is to install the private dependencies in the virtualenv manually or with a deployment script, and not to put them in the Pipfile. :( 



