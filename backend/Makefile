.ONESHELL :

SHELL= /bin/bash
CONDAROOT = /opt/anaconda3


create:
		conda config --prepend channels conda-forge;
		conda create -n CS520-InfinityEleNa --strict-channel-priority osmnx;

install:
		pip install django;
		pip install django-cors-headers;
		pip install django_nose;
