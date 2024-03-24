This project consists of apis which are used for carrier integrations


before statring the project create a db with the sql file 'Asendia db.sql' in pgadmin and change db config details in dbfun.py
schema picture is added to repo for reference

to install requirements - 'pip install -r requirements.txt'

to start the project - 'uvicorn main:app --reload'

once uvicorn server is up, navigate to http://127.0.0.1:8000/docs (fastapi swager ui) to test the apis

api bodies and responses are added to repo for reference in json format.


Note:- Both sender and reciver must signup before creating a shipment.

