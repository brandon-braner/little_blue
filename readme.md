## Little Blue - Helping you get and keep your projects up
![BluePill](https://github.com/brandon-braner/images/blob/master/github_images/bluepill_200x210.png?raw=true)

## What is Little Blue?

With many companies moving to microservices it is sometimes difficult to keep track of all the different services you have
to maintain. Also each team has to remember what services to have new engineers setup and the steps to get them up and running.

Little Blue aims to make it easy to codify the steps to get your projects up and running. Tell it which repositories you want
setup and the scripts or commands you need to get them setup and let it do the rest. Setting up new engineers has never been so easy.

For current engineers you can have Little Blue keep your repos up to date by checking out and pulling your latest master and develop branches.
It will then pull the latest changes for each branch, run any scripts you define and then re-checkout the current branch you are working on. 

## Configuration

Configuration is done through toml files. If you have never worked with toml files you can read about them [here](https://github.com/toml-lang/toml)

Each project is setup in the `configs` directory. The name of the project is the name of the directory.  

To setup a project simply create a directory and inside that directory create a toml file with the name `main.toml`.  

You will then create a new toml file for each repo you want to setup `repo.toml`. In the example below you wil see headers like
`[repo.{reponame}]` in each header replace `{}` with the name of the repo. These are just here for unique identification. They can be anything
but must be unique.

Finally create a `build.toml`. This will contain the name of the main.toml file incase you decide to change it as well as an
array of the project files. The order they appear here is the order they will be built. When listing the files you do not need to append the .toml extension.

### main.toml
main.toml is where you setup the basic information on your project. You can copy the code block below as a template to start.  
```
title = "The title of your project"
directory = "directory where you want the repo to download to. If it does not exist it will be created"
```

### repo.toml
* These files can be named whatever you want as long as they end with the .toml extension.
* Replace each `{reponame}` with your repos name. This must be unqiue across all repos.
* 
```
[repos.{reponame}]
repo_url = "git@github.com:brandon-braner/little_blue.git"
folder_name = "little_blue"
active = true
main_branch = "master"
develop_branch = "develop"

# These would be run with a setup task
[[repos.{reponame}.scripts]]
executable = "pwd"
args = ""
action = "setup"
```

### build.toml
```
main_file = "main"
repo_build_order = ["repo_1", "repo_2"]
```

### Setup & Add a new repo

Follow the following steps to setup this project.
* Install Python if you do not have it. 
* Setup a virtualenv. The simplest way to do this is to change to this directory and run `python -m venv venv`.
* Install the requirements by activating your virtualenv by running `source venv/bin/activate` and then run `pip install -r requirements.txt`.
* Follow the steps above for creating a new project and repo.


Python setup instructions: https://realpython.com/installing-python/
```
# run this to create virtual env.
python3 -m  venv venv

# activate virtual env
source venv/bin/activate

# install requirements
pip install -r requirements.txt
```

The following is an example of a repo config. You will need at least one repo setup.

* **repo_url** the ssh url we can clone the repo from. Currently, we are only supporting ssh. 
* **folder name** is your local folder name where the repo is stored locally and will be clones to
* **active** set to true if you want this repo to maintain your repo else false
* **main_branch** the name of the main/master branch of your repository
* **develop_branch** the name of the develop branch of your repository
* **scripts** the scripts that need to run for your project. 
```
[repos.my_repo]
repo_url = "git@github.com:brandon-braner/little_blue.git"
folder_name = "little_blue"
active = "true"
main_branch = "master"
develop_branch = "develop"

[[repos.mono.scripts]]
executable = "migration executable"
args = "migration args"
action = "setup/upgrade/all"
```

## How to Run

* Ensure you have your virtualenv activated.
* Test that the inv command works by running `inv --version`. You should get a response that looks like `Invoke 1.6.0`
the version number will depend on what version of Invoke you are using.
* Run `inv {action} {project}` where {action} is one of the actions is either `setup` or `upgrade` and `{project}` is the name 
of the folder from the `configs` directory you want to run.

## Actions

There are currently 3 actions setup, upgrade and all.  
Setup will run first, then upgrade and finally all

**setup**  
setup will run when you run `inv setup`

**upgrade**  
upgrade will run when you run `inv change`  

All upgrades will checkout your develop branch -> pull the changes -> run your scripts -> re-checkout the branch you were on.  
**Make sure you commit or stash your changes first**
  
**all**  
all will run after setup and upgrade on every other action

## Scripts
Scripts are anything that you need to run after you either clone or pull your repo.  
Example if you have a Django app you might want to run `python manage.py db upgrade` after you clone or pull your repo
you would put `python manage.py` as your executable and `db upgrade` as your args.

Scripts are run in the order they are listed in the config.

## Open Source Projects Used
> [Invoke](https://www.pyinvoke.org/)  An awesome library to write makefile like scripts but in Python.

> [Pydantic](https://pydantic-docs.helpmanual.io/)  Data validation and settings management using python type annotations.

# Changelog
[0.1.0](https://github.com/brandon-braner/little_blue/releases/tag/0.0.2) 2021-11-06
* Updated to allow multiple projects to be setup. Also broke out the repo configs into a separate files
to make them easier to manage.

[0.0.2](https://github.com/brandon-braner/little_blue/releases/tag/0.0.2) 2021-11-06
* Fixed clone function to clone to the repo folder
* Added a change dir command to change to the repo folder when running scripts

[0.0.1](https://github.com/brandon-braner/little_blue/releases/tag/0.0.1) 2021-11-05
* Inital Release
