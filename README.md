#########################
####### Startup ##########

docker-compose -f local.yml build
docker-compose -f local.yml up

###########################
####### VIRTUALENV ########

virtualenv -p python3 env

###################
###### PIP ########

 pip install -r requirements.txt

#########################
####### NETWORKS ########

docker network rm $(docker network ls -q)
sudo lsof -nP | grep LISTEN
sudo kill -9 1511

######################
####### NGINX ########

/etc/init.d/nginx restart

tail -f /var/log/nginx/error.log

nginx -s reload


sudo systemctl restart nginx

###################################
####### Ubuntu Permissions ########

sudo reboot

find ./static -type d -exec chmod 755 {} \;

###############################
#######  DUMP DATABASE ########

sudo su postgres
psql
drop database your_database_name;
create database your_database_name with owner user_you_use_in_django;
\q
exit

python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions -e wagtailcore.pagerevision > databasedump2.json


##THIS WORKED

LOADING A DATBASE FILE INTO BLANK DATABASE: python3 local.py loaddata db.json

CREATING A DATABASE FILE FROM EXISTING DATABASE: python3 local.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions > db.json



docker-compose -f dev.yml run --rm django python manage.py flush

docker-compose -f dev.yml run --rm django python manage.py loaddata db-8-30.json

docker-compose -f dev.yml run --rm django python manage.py migrate

#########################
####### Gunicorn ########

# When in production you must restart gunicorn when you pull new settings
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

## Create .env below

'' //ENV file #What is this for?? Environment file?
DEBUG=off
DJANGO_SECRET_KEY_MCMANUS='#^57b45ap)gvbl@#@f5v1uqbv)1x3na2ct@xe$ql^r_ds#g0ap'
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

##################################
####### Internet problems ########

dominic@dom-Inspiron-7559:~$ sudo rm -f /var/lib/NetworkManager/NetowkrManager.state
[sudo] password for dominic:
dominic@dom-Inspiron-7559:~$ sudo service network-manager restart
network-manager stop/waiting
network-manager start/running, process 5279
dominic@dom-Inspiron-7559:~$

#################################
######## DOCKER Commands:########


docker-compose ps
docker-compose down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume rm $(docker volume ls -qf dangling=true)

#########################
###### POSTGRESQL #######

First you must connect to the database within container:
sudo su postgres
psql -h localhost -p 5432

sudo su postgres
\l "Lists all databases"
\c vickibot "connects to database vickibot"
\dt "lists all tables"
SELECT * FROM pg_catalog.pg_tables;
\c vickibot "connects to database vickibot"

example: select * from memberships_usermembership;
memberships_usermembership = table

Make sure that both databases have the same amount of tables, try deleting users in dev environment. delete the pages, but not root.


DOCKER COMMANDS:
docker ps #shows all runnign docker containers

#TODO: remove postgres 5433 port for production


python manage.py generate_secret_key [--replace] [secretkey.txt]


########################
###### Going Live ######

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

- Setup Recaptcha Settings https://github.com/praekelt/django-recaptcha  https://www.google.com/recaptcha/admin#list

- Update Nginx File

- Create stemletics/stemletics/mysite/.env file from above for Gunicorn

- Update Gunicorn File
  sudo nano /etc/systemd/system/gunicorn.service

  systemctl daemon-reload
  sudo systemctl start gunicorn
  sudo systemctl enable gunicorn
  sudo systemctl status gunicorn

- edit WSGI.py file from dev to production
