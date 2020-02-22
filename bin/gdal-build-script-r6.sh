#Install GEOS
wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
tar xjvf geos-3.4.2.tar.bz2
cd geos-3.4.2
./configure
make
sudo make install

#Install PROJ
cd /home/ec2-user/postgis/
wget http://download.osgeo.org/proj/proj-4.9.1.tar.gz
wget http://download.osgeo.org/proj/proj-datumgrid-1.5.zip
tar zxvf proj-4.9.1.tar.gz
cd proj-4.9.1/nad
unzip ../../proj-datumgrid-1.5.zip
cd ..
./configure  
make
sudo make install

wget http://download.osgeo.org/gdal/2.4.4/gdal-2.4.4.tar.gz
tar zxvf gdal-2.4.4.tar.gz
cd gdal-2.4.4
./configure
make
sudo make install
sudo ldconfig



#update lib
sudo su
echo /usr/local/lib >> /etc/ld.so.conf
exit
sudo ldconfig
