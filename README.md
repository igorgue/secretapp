# Secret-app
Secret-app is the source code for the website http://secretcities.com

We happily encourage contributions to the source. Is there a cool feature you'd like to add? Do you want to positively improve the experience of tens of thousands of users? Then get involved. Thats one of the strongest and most important facts about this group, is that you'll be working on a living breathing project used by a living breathing very active community.

So get involved and join in!


## Contents
1. General
2. Contributing
3. Getting setup


## General

### Helpful links
* **Website** http://secretcities.com
* **Dev - Community** http://groups.google.com/group/secretcities/
* **Dev - Notifications** http://timjdavey.com/tagged/secretcities
* **Dev - Tutorials** http://timjdavey.com/tagged/tutorial
* **Twitter** http://twitter.com/secret_london
* **Secretlondon Facebook** http://www.facebook.com/group.php?gid=259068995911

### License
See LICENSE doc for details.
http://github.com/timjdavey/secretapp/blob/master/LICENSE



## Contributing
To get involved in the project, we do a thing called "forking". See http://help.github.com/forking/ for more details.
Once you've got that down and understand how that works. Following the "Getting setup" to get the project setup on your local machine.
Then you can submit patches, features, designs to you're hearts content.

Obviously if you are an active contributor we'll pull you into the core team.
Also get chatting on our google dev group. http://groups.google.com/group/secretcities/


## Getting setup
1. Install the dependancies (check out the notes for how to install each of these).
2. Setup your environment settings
3. Setup the database
4. Run the search-server
5. Load data
6. Run the server

Steps 4,5,6 should in theory be run every time you do a git-pull

### Dependancies
#### Git
* **signup** http://github.com/
* **tutorial** http://learn.github.com/p/intro.html
* **mac-install** http://help.github.com/mac-git-installation/
* **ubuntu-install** `apt-get install git-core`
* **setup ssh-keys** http://github.com/guides/providing-your-ssh-key
* **general help** http://help.github.com/

#### Django
* **link** http://www.djangoproject.com/ v.1.1
* **download** http://www.djangoproject.com/download/
* **general-install** http://docs.djangoproject.com/en/1.1/intro/install/#intro-install
* **ubuntu-install** `apt-get install python-django`

#### PIL
* **link** http://www.pythonware.com/products/pil/#pil117 v.1.1.7
* **download-install** http://effbot.org/downloads/Imaging-1.1.7.tar.gz `cd Imaging-1.1.7; python setup.py install`
* **ubuntu-install** `apt-get install python-imaging`

#### South
* **link** http://south.aeracode.org v.0.6.2 (or latest)
* **tutorial** http://south.aeracode.org/wiki/QuickStartGuide
* **download** http://south.aeracode.org/wiki/Download
* **github** http://github.com/andrewgodwin/south
* **git-original** `git clone git://github.com/andrewgodwin/south.git; cd south; python setup.py install;`
* **git-mirror** `git clone git://github.com/timjdavey/south.git; cd south; git rebase; python setup.py install;`

#### pyfacebook
* **link** http://github.com/sciyoshi/pyfacebook/ v.0.1
* **git-install** `git clone git://github.com/sciyoshi/pyfacebook.git; cd pyfacebook; python setup.py install;`
* **ubuntu-install** `apt-get install python-facebook`

#### django-socialauth
* **link** http://github.com/uswaretech/Django-Socialauth v.0.6c9 (or latest)
* **git-install** `git clone git://github.com/uswaretech/Django-Socialauth.git; cd Django-Socialauth; python setup.py install;`

#### Openid
* **link** http://pypi.python.org/pypi/python-openid/
* **download-install** http://openidenabled.com/files/python-openid/packages/python-openid-2.2.4.tar.gz `cd python-openid-2.2.4; python setup.py install;`
* **easy-install** `easy_install python-openid`

#### Yadis
* **link** http://pypi.python.org/pypi/python-yadis/1.1.0
* **download-install** http://openidenabled.com/files/python-openid/files/python-yadis-1.1.0.tar.gz `cd python-yadis-1.1.0; python setup.py install;`
* **easy-install** `easy_install python-yadis`

#### OpenAuth
* **link** http://github.com/leah/python-oauth
* **git-install** `git clone git://github.com/leah/python-oauth.git; cd python-oauth; python setup.py install;`

#### Solr
* **link** http://wiki.apache.org/solr/SolrTomcat
* **mac-install** http://timjdavey.com/post/423973736/installing-solr-on-mac-osx
* **ubuntu-install** http://timjdavey.com/post/421915671/installing-solr-with-tomcat6-on-ubuntu-8-04

#### Solango
* **link** http://code.google.com/p/django-solr-search/ v.0.0.2 (or latest)
* **original-install** `svn co http://django-solr-search.googlecode.com/svn/trunk/ django-solr-search`
* **ERROR:** often people getting the error `ConfigParser.NoSectionError: No section: 'formatters'`
* **alternative-install** git-hosted version: http://github.com/timjdavey/solango `git clone git://github.com/timjdavey/solango.git; cd solango; python setup.py install;`


### Environment
Next we need to setup the specific configurations for your local machine.

1. Create a file called `environment.py` in the same directory as `settings.py`
2. Go to `settings.py` look at the comments at the top of the page
3. Copy the example and settings at the top of the page
4. Alter settings to fit with for you


### Database
Create a database. Can be anything you want, just make sure its setup correctly in the settings file.

For mysql (want utf8 character set)

    CREATE DATABASE secretapp CHARACTER SET utf8;

Next you need to create the tables

    # standard django
    ./manage.py syncdb --noinput
    
    # south syncdb
    ./manage.py migrate


### Run Search Server
We need to get the search server up and running with django

Step 1. Setup the schema

    ./manage.py solr --schema

Step 2. Restart the server

    ./manage.py solr --start

Step 3. Index the data so solr can handle it

    # in a new terminal (so start is still running)
    ./manage.py solr --reindex

See the solango docs for more details http://www.screeley.com/djangosolr/tutorial.html#solr-schema-xml


### Load data
There is a large django dumpfile in 
    
    ./manage.py loaddata /fixtures/example_data.json
    
    ./manage.py solr --reindex

This also contains an admin with username:`admin` password:`admin`


This file may go out of date in comparison to the models. So if you would like to import the data raw. 
We'll turn this into a `./manage.py dumpdata` file soon. But for now run the following from `./manage.py shell`.

    from utilz.csv_import import import_data
    import_data()

There will be a few numbers outputted at this point. Ignore those.
Then just check all the data is loaded by going into the db or admin interface!


Enjoy!

