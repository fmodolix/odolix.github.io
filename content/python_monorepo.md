Title: Python monorepo with PDM
Date: 2024-09-10 00:00 
Modified: 2024-09-10 00:00 
Category: Blog
Tags: monorepo, python, pdm
Slug: python-monorepo-pdm 
Authors: Odolix 
Summary: Setup a monorepo with pdm

# Python monorepo with PDM

I've built monolithic apps, macroservice, microservice and libs. In most cases, I was quickly driven to splitting the code into different modules and libraries that I want to share with or reuse on other projects. 

## Monorepo or multi-repo

### Multi-repo

Multi-repo will adapt easily to multi-team approach, limiting the potential conflicts when merging branches by having less code per repository. 

### Monorepo

Monorepo will give you a consistent versioning of the code, and a global overview of dependencies between the different components.

## PDM and Pipenv

[PDM](https://pdm-project.org/latest/) is a Python Package and Dependency manager. It competes with Poetry, Pipenv or Conda (or many others). 

I've started Python development with PIP + Virtualenv, then moved last year to Pipenv, but I was disappointed by Pipenv, mostly because of the speed of dependency resolution, and instability of the dependency resolution. 
I was using it with private repositories with private dependencies. [1](https://blog.peabytes.me/pipenv-github-private.html)

I was also using it to deploy services using Ansible, and the deployment time was sometimes exceptionally long. 

I don't the same problem with PDM anymore, it feels faster and more consistent. That was basically why I chose it at the beginning. 

## Setting up a monorepo

### 1. Move everything

Yes, you have to merge your different repositories into one. You probably can keep the history, but I chose not to. 

I just copied the source into a new folder in the monorepo.

### 2. Folder structure

Before switching, I had 7 repos: 
- 4 Django apps
- 3 Python libraries

Each app had its docker folder, its config folder, its template folder, its source folder, its .env file. 

After switching, the folder structure looks like that: 

```
- repo
  - apps
	  + app1
		  * config
		  * src
		  * pyproject.toml
		  - manage.py <- django app
	  * app2
		  - config
		  - src
 		  * pyproject.toml
  - libs
	  + lib1
		  * src
  - docker
	  + app1
		  * DockerFile
	  + app2
		  * ...
	  + docker-compose.yml
  - pyproject.toml <- That's where the monorepo config goes
  - manage.py <- That's a Django project
```

### 3. Project configuration

Although I use a monorepo, I want to be able to deploy each service independently with installing all the code every time. 

To manage that we use project optional dependencies, 

```
# Code quality and linting
[tool.pdm]
plugins = [
    "pdm-dotenv", # manage env files
    "sync-pre-commit-lock", # check code structure before commit
    "pdm-django",  # manage Django commands 
    "pdm-version" # Manage PDM version
]

# Define files included in the packages
[tool.pdm.build]
includes = [
	"libs/lib1", 
	"libs/lib2",
	"apps/app1"
	"apps/app2",
	"apps/**/*.py",
	"apps/**/*.html",
	"apps/**/*.js",
	"apps/**/*.css",	
]

excludes = [
	"venv", 
	"docker"
]

[pdm.tools.dependencies]
dev = [
	# dev external dependencies
	...
	# dev local dependencies 
	# Let's include everything for dev
	"-e app1 @ file:///${PROJECT_ROOT}/apps/app1",
	"-e app2 @ file:///${PROJECT_ROOT}/apps/app2",
	"-e lib1 @ file:///${PROJECT_ROOT}/libs/lib1",
	"-e lib2 @ file:///${PROJECT_ROOT}/libs/lib2",
]


[project]
name = "My monorepo"
version = "My version"
description = "My monorepo project"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[project.optional-dependencies]
app1_pkg = [
    "lib1 @ file:///${PROJECT_ROOT}/libs/lib1",
    "app1 @ file:///${PROJECT_ROOT}/apps/app1",
]
app2_pkg = [
    "lib1 @ file:///${PROJECT_ROOT}/libs/lib1",
    "lib2 @ file:///${PROJECT_ROOT}/libs/lib2",    
    "app2 @ file:///${PROJECT_ROOT}/apps/app2",
]

# Scripts to run or build partial projects
[tool.pdm.scripts] 
_.env_file = ".env" # Load environment variables from file
docker_build = "docker-compose build docker/docker-compose.yml"
# App1
serve_app1 = "python apps/app1/manage.py runserver --settings=config.settings 127.0.0.1:8000"
```

In the above file, we differentiate install and run on dev environment: we install everything and run only the necessary apps. 

### 4. Deployment

As mentioned in a previous article, I deploy packages from private Github repos, it saves the hassle of building a package server. 

To deploy, I use the following syntax: 

> pip install "project[app1] @ git+https://$GITHUB_TOKEN@github.com/account/project.git@$BRANCH"

This commands targets a private repository and deploys the app on a specific branch. 

This is pretty efficient, and eases the pain of managing private dependencies. 

## Final word

Moving to a monorepo gave me a better visibility on the code, simplified my deployment process, and did not result in a more complex merge of code. 

This was done on a few projects, with a small team, so it doesn't reflect larger ensembles, but I'm pretty confident it that it scales better than a multi-repo approach. 

Special thanks to Lucas for mentioning the monorepo approach in the first place. 