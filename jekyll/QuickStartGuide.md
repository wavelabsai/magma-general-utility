# Jekyll Static Website Generator

> ### WARNING
> DO NOT RUN ANY OF THE FOLLOWING COMMANDS WITH **SUDO** UNLESS SPECIFIED OTHERWISE

* Open a up terminal window/tab, and follow  the steps below:
```bash
# remove ruby
sudo apt remove --purge ruby
# install prerequisites
cd $HOME
sudo apt-get update 
sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libxml2-dev libxslt1-dev libcurl4-openssl-dev libffi-dev
# clone this ....
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
exec $SHELL
# .... and this
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
exec $SHELL
# install rbenv
rbenv install 3.0.2
rbenv global 3.0.2
gem install bundler
rbenv rehash
# check version
ruby -v
gem -v
```

## Setting up a minimal website
* Open up a terminal window and run the following commands:
```bash
# Install jekyll and bundler
gem install jekyll bundler
# Create your website with minimal jekyll starter code
jekyll new repo # replace "repo" with the name you want for your website
# You can now spin up your website on localhost:
bundle exec jekyll serve
```

## Publishing the website to GitHub pages
* Create a repository on `GitHub`, do not add a `README`, in this example the name of my repository is `blog` 
* In a terminal navigate to your website's directory created in the previous step:
```bash
# modify _config.yml
vim config.yml
.
.
.
title: Awesome Docs # Modify the title (not necessary)
email: user@website.com # Modify the email (not necessary)
description: >- # this means to ignore newlines until "baseurl:"
  Write an awesome description for your new site here. You can edit this
  line in _config.yml. It will appear in your document head meta (for
  Google search results) and in your feed.xml site description.
baseurl: "/repo" # substitute the name of your repo
url: "username.github.io" # replace with username.github.io (username = your username on github)
github_username:  username # replace with github username
.
.
.
# add, commit to git and push the commit
git init
git checkout -b gh-pages
git add .
git commit -m "initial commit"
git remote add origin git@github.com:username/repo.git # replace username/repo.git with your values 
git push origin gh-pages
```
* Go to your repository's GitHub page and click on actions.
* If the actions succeed to build and deploy your website, you'll be able to access it on `username.github.io/repo`
* For more info checkout these links: [github pages documentation](https://pages.github.com/) and [Jekyll setp-by-step](https://jekyllrb.com/docs/step-by-step/01-setup/)

