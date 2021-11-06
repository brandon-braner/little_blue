![BluePill](https://github.com/brandon-braner/images/blob/master/github_images/bluepill_200x210.png?raw=true)

## Why?

I often forget to update my repos. I forget to pull the latest master or develop.  
I forget to run the migrations. This is aimed to help me automate the little things.

## Configuration

Configuration is in a toml file. You can read more about it [here](https://github.com/toml-lang/toml).  

Each repo will have its own config in the projects.toml file.  
Why use toml? It sounded fun to be honest, a good opportunity to learn.


### Setup & Add a new repo

Follow the following steps to setup this project.
* Install Python if you do not have it. 
* Setup a virtualenv. The simplest way to do this is to change to this directory and run `python -m venv venv`.
* Install the requirements by activating your virtualenv by running `source venv/bin/activate` and then run `pip install -r requirements.txt`.
* Change the `directory` variable in the `projects.toml to the directory your repos are clones to or want to be cloned to


The following is an example of a repo config. You will need at least one repo setup.

* **repo_url** the ssh url we can clone the repo from. Currently, we are only supporting ssh. 
* **folder name** is your local folder name where the repo is stored locally and will be clones to
* **active** set to true if you want this repo to maintain your repo else false
* **main_branch** the name of the main/master branch of your repository
* **develop_branch** the name of the develop branch of your repository
* **scripts** the scripts that need to run for your project. 

[repos.my_repo]
repo_url = "git@github.com:brandon-braner/little_blue.git"
folder_name = "little_blue"
active = "true"
main_branch = "master"
develop_branch = "develop"

[[repos.mono.scripts]]
executable = "make"
args = "fake"
action = "setup/upgrade/all"

## How to Run

* Ensure you have your virtualenv activated.
* Test that the inv command works by running `inv --version`. You should get a response that looks like `Invoke 1.6.0`
the version number will depend on what version of Invoke you are using.
* Run `inv {action}` where {action} is one of the actions listed in the repo config.

## Actions

There are currently 3 actions setup, upgrade and all.  
Setup will run first, then upgrade and finally all

* **setup**  
setup will run when you run `inv setup`

* **upgrade**  
upgrade will run when you run `inv change`
  
* **all**  
all will run after setup and upgrade on every other action