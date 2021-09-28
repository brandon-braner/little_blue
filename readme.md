# Auto Repo Update

## Why?

I often forget to update my repos. I forget to pull the latest master or develop.  
I forget to run the migrations. This is aimed to help me automate the little things.

## Configuration

Configuration is in a toml file. You can read more about it [here](https://github.com/toml-lang/toml).  

Each repo will have its own config in the projects.toml file.  
Why use toml? It sounded fun to be honest, a good opportunity to learn.


### Setup & Add a new repo

To setup this repo you will need Python. Setup a virtualenv and install the requirements.  

Change the directory setting to the directory your repos are clones to or want to be cloned to

The following is an example of a repo config

* **repo_url** the ssh url we can clone the repo from. Currently, we are only supporting ssh. 
* **folder name** is your local folder name where the repo is stored locally
* **active** set to true if you want this repo to maintain your repo else false
* **main_branch** the main/master branch of your repository
* **develop_branch** the develop branch of your repository
* **scripts** the scripts that need to run to setup your project. 

[repos.my_repo]
repo_url = "git@github.com:brandon-braner/fancyrepo.git"
folder_name = "My Repo"
active = "true"
main_branch = "master"
develop_branch = "develop"

[[repos.mono.scripts]]
executable = "make"
path = "fake"
action = "setup/upgrade/all"


## Actions

There are currently 3 actions setup, upgrade and all.  
Setup will run first, then upgrade and finally all

* setup
setup will run when you run `inv setup`

* upgrade
upgrade will run when you run `inv change`
  
* all
all will run after setup and upgrade on every other action