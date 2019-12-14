# Startup Django Guide

# prerequisites
1. Python 3
2. pip3
3. VirtualEnv
4. Postgres Database

How to install 1-3: https://www.digitalocean.com/community/tutorials/how-to-install-django-and-set-up-a-development-environment-on-ubuntu-16-04

How to install postgres: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

# How to start development server
1. Create virtualenv in the folder previous to mysite.

2. go to /mysite/requirements

3. Create a folder on your computer to store the project files.

4. go into that folder and git pull the project from github.

To do that, open up that folder in your terminal and execute the following line:

'git clone https://github.com/Zalkota/project.git'

5. Go into the folder that was just pulled and create a virtualenv in that folder. It should be before mysite.
run 'virtualenv -p python3 env'

6. Turn on the virtual environment:
 'source env/bin/activate'

 You will see (env) in your terminal.

7. go to /mysite/requirements

8. run: pip3 install -r requirements.txt
This will install all of the requirements for the website_url

9. Now we need to create a database in postgresql, run the next 10 commands below.
sudo su postgres
psql
CREATE DATABASE estore;
psql -c "'CREATE USER estoreadmin WITH PASSWORD '$Django10';
ALTER ROLE estoreadmin SET client_encoding TO 'utf8';
ALTER ROLE estoreadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE estoreadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE estore TO estoreadmin;
\q
exit

10. navigate to folder /mysite/, you should see the file local.py.

11. run 'Python3 local.py makemigrations'
    run 'Python3 local.py migrate'
    run 'Python3 local.py runserver'

12. Open a new terminal and go to /projects/project/mysite/
run 'npm install'
run 'grunt watch'

Now your sass files are compiling


13. run elasticsearch 1.7.6
go to extracted file of elasticsearch
run 'bin/elasticsearch'

If that works then congratulations, open your internet browser and go to 127.0.0.1:8000 in the address bar.



14. Importing data for Django Cities
run 'python3 local.py cities_light'


#############################################################3
# Common Commands

python3 local.py runserver

python3 local.py createsuperuser

### Migrations ###

python3 local.py makemigrations

python3 local.py migrate

### End migrations ###


### Docker - Ignore this.. ###
docker-compose -f local.yml build
docker-compose -f local.yml up


# VIRTUALENV
virtualenv -p python3 env


# PIP
pip3 install -r requirements.txt
