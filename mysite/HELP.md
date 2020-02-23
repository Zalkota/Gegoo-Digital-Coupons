# To Start Server

Python3 local.py runserver

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

3. Create a folder on your computer to store the project files, call it 'estore'

4. go into that folder and git pull the project from github

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

# add -w to silence containers
sudo lsof -nP -w | grep LISTEN

echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p`


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
sudo systemctl status gunicorn
systemctl daemon-reload

sudo journalctl -u gunicorn


gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application

sudo nano /etc/systemd/system/gunicorn.service

''
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=dom
Group=www-data
WorkingDirectory=/home/dom/Desktop/projects/gegoo/mysite
ExecStart=/home/dom/Desktop/projects/gegoo/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/dom/Desktop/projects/gegoo/mysite/mysite.sock mysite.$

[Install]
WantedBy=multi-user.target
''


# .bashrc

cd to base directory with:
cd    
nano .bashrc

## Create .env below

DEBUG=off
DJANGO_SECRET_KEY=''
DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=ungithubbed-secret

EMAIL_PASSWORD='$Django28'
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
''

sudo systemctl stop gunicorn

systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

debug:
systemctl status gunicorn.service


# SSH

Log in as root
Edit ssh config:
sudo nano /etc/ssh/sshd_config

Change this line:
PasswordAuthentication no

to
PasswordAuthentication yes

Restart daemon:
sudo systemctl restart sshd



# Letscrypt
https://www.linode.com/docs/security/ssl/install-lets-encrypt-to-create-ssl-certificates/#create-an-ssl-certificate

Create an SSL Certificate
cd /opt/letsencrypt
sudo -H ./letsencrypt-auto certonly --standalone -d printrender.com -d www.printrender.com

Renew
sudo -H ./letsencrypt-auto certonly --standalone --renew-by-default -d example.com -d www.example.com

CronTab
sudo crontab -e
0 0 1 * * /opt/letsencrypt/letsencrypt-auto renew


Check Certificate
sudo ls /etc/letsencrypt/live

# Cert bot
sudo -H ./letsencrypt-auto certonly --preferred-challenges http -d negativegravityband.com -d www.negativegravityband.com

test:
certbot renew --cert-name negativegravityband.com -a nginx --dry-run

live:
certbot renew --cert-name negativegravityband.com -a nginx

Delete
sudo certbot delete --cert-name example.com

Install
apt-get install software-properties-common python-software-properties
add-apt-repository ppa:certbot/certbot
apt-get update
apt-get install python-certbot-apache
sudo apt-get install certbot python-certbot-nginx

Install Link: https://linuxhostsupport.com/blog/install-lets-encrypt-ssl-certificates-using-certbot/

comment out sites-available

sudo certbot --nginx

ps -ef | grep certb

Helpful Links:
https://www.digitalocean.com/community/tutorials/how-to-use-certbot-standalone-mode-to-retrieve-let-s-encrypt-ssl-certificates-on-ubuntu-16-04

https://community.letsencrypt.org/t/already-listening-on-tcp-port-80/61885

https://community.letsencrypt.org/t/cert-renewal-for-standalone-nginx/89149

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

# Elastic search

Dependencies:
Elastic 1.7.6  https://www.elastic.co/downloads/past-releases/elasticsearch-1-7-6
Sudo apt install openjdk-8-jre-headless


elasticsearch==5.5.3
django-haystack==2.8.1

Extract files:

tar -xvf elasticsearch-5.6.16.tar.gz

how to run elastic search Server:

    bin/elasticsearch

Download This:
https://www.elastic.co/downloads/past-releases/elasticsearch-5-6-16

https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
or
https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

Run search_index --rebuild

python manage.py rebuild_index

python manage.py update_index

You should cron up a ./manage.py update_index job at whatever interval works best for your site (using --age=<num_hours> reduces the number of things to update).
Alternatively, if you have low traffic and/or your search engine can handle it, the RealtimeSignalProcessor automatically handles updates/deletes for you.
https://django-haystack.readthedocs.io/en/v2.4.1/tutorial.html
https://knowpapa.com/haystack-elasticsearch/

# DUMP DATABASE #

python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions -e wagtailcore.pagerevision > databasedump2.json

## THIS WORKED ##

LOADING A DATBASE FILE INTO BLANK DATABASE:
python3 local.py loaddata db.json

python3 production.py loaddata db.json


CREATING A DATABASE FILE FROM EXISTING DATABASE:
python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions > db.json



## GeoDjango

https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS24UbuntuPGSQL10Apt

sudo -u postgres psql -d gegoo -c "CREATE EXTENSION IF NOT EXISTS postgis;"

CREATE EXTENSION postgis;

su postgres
psql
alter role user_name superuser;
#then create the extension as the user in a different screen
alter role user_name nosuperuser




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

- mv  -v ./server/gegoo/* ./server/

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
