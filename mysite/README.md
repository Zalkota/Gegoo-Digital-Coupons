# The Official README #

# Table of Contents #

1 Startup Guide for M2 Repository
2 Common Commands
3 VIRTUALENV
4 PIP
5 NETWORKS
6 NGINX
7 Ubuntu Permissions
8 Gunicorn
9 Internet problem
10 DOCKER Commands
11 POSTGRESQL
12 DUMP DATABASE
13 Going Production Check List

# Startup Guide for M2 Repository

1. You will need version 3.6 of Python, so download it

2. Download Virtual environment

3. Create a folder on your computer to store the project files "m2"

4. Pull the project into that folder

To do that, open up that folder in your terminal and execute the following line:

git clone https://github.com/Zalkota/m2-capital.git

5. Create VirtualEnv (look up guide for mac)

6. Enable the virtual environment

7. navigate to folder /mysite/requirements/

8. run: sudo pip3 install -r requirements.txt
This will install all of the requirements for the website_url

9. Install postgres database 9.6.12
Go to Postgres part of this document and create a database and user

10. navigate to folder /mysite/

11. run: python3 local.py runserver

If that works then congratulations, open your internet browser and go to 127.0.0.1:8000 in the address bar.


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


# NETWORKS

docker network rm $(docker network ls -q)
sudo lsof -nP | grep LISTEN
sudo kill -9 1511


# NGINX

/etc/init.d/nginx restart
tail -f /var/log/nginx/error.log
nginx -s reload
sudo systemctl restart nginx


# Ubuntu Permissions

sudo reboot
find ./static -type d -exec chmod 755 {} \;


# Gunicorn

### When in production you must restart gunicorn when you pull new settings ###
sudo systemctl restart gunicorn


gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application

sudo nano /etc/systemd/system/gunicorn.service
''
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myproject
ExecStart=/home/sammy/myproject/venv/bin/gunicorn --workers 3 --bind unix:/home/sammy/myproject/myproject.sock myproject.wsgi:application
EnvironmentFile=/home/sammy/myproject/.env

[Install]
WantedBy=multi-user.target
''
# .bashrc

cd to base directory with:
cd    
nano .bashrc

## Create .env below

'' //ENV file #What is this for?? Environment file?
DEBUG=off
DJANGO_SECRET_KEY_MCMANUS=''
DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=ungithubbed-secret
''

sudo systemctl stop gunicorn

systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

debug:
systemctl status gunicorn.service


# Internet problems

dominic@dom-Inspiron-7559:~$ sudo rm -f /var/lib/NetworkManager/NetowkrManager.state
[sudo] password for dominic:
dominic@dom-Inspiron-7559:~$ sudo service network-manager restart
network-manager stop/waiting
network-manager start/running, process 5279
dominic@dom-Inspiron-7559:~$


# DOCKER Commands


docker-compose ps
docker-compose down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume rm $(docker volume ls -qf dangling=true)


# POSTGRESQL

sudo su postgres
psql
drop database your_database_name;
create database your_database_name with owner user_you_use_in_django;
\q
exit


# Create a Database for your server

CREATE DATABASE myproject;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
\q



### MODIFY Postgres Database Tables ##
First you must connect to the database within container:
sudo su postgres
psql -h localhost -p 5432

sudo su postgres
\l "Lists all databases"
\c vickibot "connects to database vickibot"
\dt "lists all tables"
SELECT * FROM pg_catalog.pg_tables;
\c vickibot "connects to database vickibot"

\ Delete table
mod=# DROP TABLE event_eventpage;

example: select * from memberships_usermembership;
memberships_usermembership = table

Make sure that both databases have the same amount of tables, try deleting users in dev environment. delete the pages, but not root.



DOCKER COMMANDS:
docker ps #shows all runnign docker containers
##TODO: remove postgres 5433 port for production
python manage.py generate_secret_key [--replace] [secretkey.txt]



# DUMP DATABASE #

python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions -e wagtailcore.pagerevision > databasedump2.json

## THIS WORKED ##

LOADING A DATBASE FILE INTO BLANK DATABASE:
python3 local.py loaddata db.json

python3 production.py loaddata db.json


CREATING A DATABASE FILE FROM EXISTING DATABASE:
python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions > db.json



Exclude apps:
wagtailusers
wagtailsearch
wagtailredirects
wagtailimages
wagtailforms
wagtailembeds
wagtaildocs
wagtailcore
wagtailadmin



docker-compose -f dev.yml run --rm django python manage.py flush

docker-compose -f dev.yml run --rm django python manage.py loaddata db-8-30.json

docker-compose -f dev.yml run --rm django python manage.py migrate

# Node-sass/Gruntfile.js Instructions

1. Install npm (Node Package Manager)

2. navigate to m2/mysite

3. run the following command in terminal: npm install
This will install the packages outlined in package.json file

4. run this command: grunt

If this returns an error just send it to me in slack and I will help you or google it.

5. This will render the following .scss files to .css as outlined in the Gruntfile.js like below

Gruntfile.js
'<%= paths.css %>/base.css': '<%= paths.sass %>/_base.scss'
'<%= paths.css %>/base-alt.css': '<%= paths.sass %>/_base-alt.scss'
__



# Going Production Check List #

Clone repo
Check DB
Edit Nginx FILEenv
import DB


Checklist:
- Dump data from dev server

- Set up Database on server

- git pull

- migrate database

- load data

- Update sites-available Nginx File (sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled)

- Create stemletics/stemletics/mysite/.env file from above for Gunicorn

- Update Gunicorn File
  sudo nano /etc/systemd/system/gunicorn.service

  systemctl daemon-reload
  sudo systemctl start gunicorn
  sudo systemctl enable gunicorn
  sudo systemctl status gunicorn

- edit WSGI.py file from dev to production

- Set Django ALLOWED_HOSTS in production settings

- Setup Recaptcha Settings https://github.com/praekelt/django-recaptcha  https://www.google.com/recaptcha/admin#list


SEO:
site.xml
robot.txt
page titles
