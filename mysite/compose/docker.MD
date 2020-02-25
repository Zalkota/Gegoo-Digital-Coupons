# Commands

# Compose
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up

docker-compose -f docker-compose.yml run django python ./mysite/local.py makemigrations
docker-compose -f docker-compose.yml run django python ./mysite/local.py migrate
docker-compose -f docker-compose.yml run django python ./mysite/local.py createsuperuser


docker exec -it mysite_django_1 sudo systemctl status gunicorn

docker exec -it mysite_django_1 python3 local.py cities_light
docker exec -it mysite_django_1 python3 local.py createsuperuser
docker exec -it mysite_django_1 python3 local.py collectstatic

# Stop or Remove Containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# Images
docker images
docker images prune


docker ps
docker ps -a
docker ps -l
docker info
docker start d9b100f2f636
docker stop sharp_volhard
docker rm festive_williams


# Database Startup
docker exec -it mysite_django_1 sudo systemctl status gunicorn

docker exec -it mysite_django_1 python3 local.py cities_light


# Shell access
For shell accessing.

#Nginx
docker exec -ti nginx bash

#Web
docker exec -ti web bash

#Database
docker exec -ti db bash
Copy
For logs:

#Nginx
docker-compose logs nginx
#Web
docker-compose logs web
#DB
docker-compose logs db



# Tutorials
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
