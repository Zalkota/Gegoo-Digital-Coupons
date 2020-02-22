# Commands

# Compose
docker-compose -f docker-compose.yml build

docker-compose -f docker-compose.yml run django python ./mysite/local.py makemigrations
docker-compose -f docker-compose.yml run django python ./mysite/local.py migrate
docker-compose -f docker-compose.yml run django python ./mysite/local.py createsuperuser

docker-compose -f docker-compose.yml up

docker build -t gegoo:v0 ./compose/django

docker run --env-file env gegoo:v0 sh -c "python manage.py makemigrations && python manage.py migrate"

docker run --env-file env -p 80:8000 gegoo:v0

docker exec -it gegoo_django sudo systemctl status gunicorn

python3 local.py cities_light

docker exec -it gegoo_django

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


# Tutorials
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04


# Database
python3 local.py cities_light
