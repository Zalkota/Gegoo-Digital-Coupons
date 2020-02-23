#  Prerequisites
https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04
Install Docker

# Start the server with Docker
First, cd to the mysite folder

    docker-compose -f local.yml build

    docker-compose -f local.yml up

Open another terminal and run the next to commands (cities_light will take 3-5 minutes):

    docker exec -it mysite_django_1 python3 local.py cities_light

    docker exec -it mysite_django_1 python3 local.py createsuperuser


Migrations:

 docker exec -it mysite_django_1 python3 local.py makemigrations


  docker exec -it mysite_django_1 python3 local.py migrate
