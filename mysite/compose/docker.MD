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

docker images
docker ps
docker ps -a
docker ps -l
docker info
docker start d9b100f2f636
docker stop sharp_volhard
docker rm festive_williams


# Tutorials
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
