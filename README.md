# Infinity Elena


All the steps are assuming that you have a fresh Ubuntu 20.04.1 installation. For mac the steps slightly change for the setup of the environment.

1. Install git 
```
sudo apt install git;
```

2. Clone the repository. Enter your git username and password
```
git clone https://github.com/koushikrbukkasamudram/InfinityEleNa.git;
```

Please run backend first and then the frontend eventhough they are independent of one another it is better since backend supports frontend.

Steps to run backend are inside the backend folder.

Steps to run frontend are inside the frontend folder.

Steps to test:

1. ```cd backend/EleNa/routeFinder```
2. ```conda activate CS520-InfinityEleNa```
3. ```pip install coverage```
4. ```coverage run ../../manage.py test```
