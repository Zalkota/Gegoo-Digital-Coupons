FROM python:3.6

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# OS dependencies for GeoDjango
RUN apt-get update && apt-get install -y \
  binutils \
  libproj-dev \
  gdal-bin \
  python-gdal

#OPTIONAL python-gdal  # (Geospatial Data Abstraction Library), specifically the OGR Simple Feature Library, that gives read and, in many cases, write access to a variety of vector file formats, implementing the OCG Simple Feature specification
#OPTIONAL libgeoip1  # an IP-based geolocation library

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install -r /requirements/requirements.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

#COPY ./compose/django/gunicorn.sh /gunicorn.sh
#RUN sed -i 's/\r//' /gunicorn.sh
#RUN chmod +x /gunicorn.sh

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/


# ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT ["/start-dev.sh"]

#CMD cd ./mysite
#CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
#CMD sudo systemctl status gunicorn
