# InfinityEleNa Backend

Steps to run the backend server(Assuming this is a fresh ubuntu 20.04.1)

Open a new terminal window and navigate to the backend folder


1. Install anaconda from the website(https://docs.anaconda.com/anaconda/install/linux/). You can skip step two and the last step. Please install this carefull and check by running ```conda``` to verify if the conda is installed well.

2. Install make
```
sudo apt install make;
```

3. Navigate into InfinityElena backend directory. Install osmnx environment. The commands are packaged into make file under the create. This can be run by the command.
```
cd backend
make create;
```

4. Change the environment to osmnx environment using the command
```
conda activate CS520-InfinityEleNa;
```

5. Install the python dependencies by running
```
make install;
```

6. Navigate into the backend folder and start the backend server
```
python manage.py runserver;
```
