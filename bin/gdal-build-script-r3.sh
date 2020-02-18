#!/bin/bash

# Installation of GDAL and dependencies.
# Based on https://gist.github.com/hervenivon/fe3a327bc28b142e51beb38ef11844c0

# Update with your versions.
GDAL_VERSION=2.2.0


sudo yum-config-manager --enable epel
sudo yum -y install make automake gcc gcc-c++ libcurl-devel proj-devel geos-devel


# Compilation work for GDAL
mkdir -p "/tmp/gdal-${GDAL_VERSION}-build"
cd "/tmp/gdal-${GDAL_VERSION}-build"
curl -o "gdal-${GDAL_VERSION}.tar.gz" \
    "http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz" \
    && tar xfz "gdal-${GDAL_VERSION}.tar.gz"
cd "/tmp/gdal-${GDAL_VERSION}-build/gdal-${GDAL_VERSION}"
./configure --prefix=/usr/local/gdal \
            --with-static-proj4=/usr/local/proj4 \
            --without-python

# Make in parallel with 2x the number of processors.
make -j $(( 2 * $(cat /proc/cpuinfo | egrep ^processor | wc -l) )) \
 && sudo make install \
 && sudo ldconfig


# Bundle resources.

cd /usr/local/gdal
tar zcvf "/tmp/gdal-${GDAL_VERSION}.tar.gz" *

