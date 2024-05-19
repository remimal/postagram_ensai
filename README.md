cd terraform

pipenv lock 
pour créer Pipfile.lock

To activate this project's virtualenv, run pipenv shell.


Déploiement en deux temps :
cd terraform/

cdktf deploy -a "pipenv run python3 main_serverless.py"

cdktf deploy -a "pipenv run python3 main_server.py"

dans webservice

pip install -r requirements.txt

swagger
http://0.0.0.0:8080/docs