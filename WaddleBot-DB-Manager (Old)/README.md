# WaddleBot DB Manager

This is a python Flask REST API that handles all DB CRUD requests with the Waddlebot Database (WIP).

# Basic Setup

## 1. Python local testing

To test the API without it being in a container, do the following (all the commands are to be executed in the WaddleBot-DB-Manager folder for now):

1. Ensure that you have python installed on your local machine, preferably v3.12. 
Download link: (https://www.python.org/downloads/)
To check if its installed correctly, run the following command in the terminal:

`py --version`

If its installed correctly, you will see this output:

`Python 3.12.3`

2. Install the python virtual environment in the root folder of the project ("versafitclub-orders-trainerize-integration") by typing:

`py -m venv ./venv`

3. Activate the virtual environment by running:

`venv\scripts\activate.bat`

4. Install the requirements of the script by running:

`pip install -r requirements.txt`

5. Ensure that the .env file with the correct environmental variables are present in the "app" folder.

6. Run the app by running the following command while having the virtual env active:

`py dbmanager.py`

7. The endpoints UI should now be available at http://127.0.0.1:5000/. 