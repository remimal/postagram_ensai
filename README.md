Rémi Malleville

## AWS

Récupérer les credentials :  
se connecter à aws -> Start Lab -> AWS Details -> AWS CLI  

Les mettre dans home/.aws.credentials  
Dans .aws/congig la région doit être "us-east-1".

## Déploiement

Se placer dans le répertoire terraform  
> cd terraform

<!-- pipenv lock 
pour créer Pipfile.lock

To activate this project's virtualenv, run pipenv shell. -->

Puis lancer l'environement virtuel :  
> pipenv sync  
> pipenv shell

Déployer la partie serverless :

> cdktf deploy -a "pipenv run python3 main_serverless.py"  

<span style="color:red">La console affiche en output les id des s3 et dynamodb. Il faut les récupérer et les mettre dans le script de déploiement main_server.py et aussi dans le .env du webservice !</span>  

Déployer la partie server :

> cdktf deploy -a "pipenv run python3 main_server.py"

<span style="color:red">La console affiche en output l'url du load balancer. Il faut la récupérer et la mettre dans le fichier webapp/src/index.js comme valeur à la variable `axios.defaults.baseURL` !</span> 

## Webapp

Pour lancer l'application, se placer dans le répertoire webapp, puis :
>npm install  
>npm start  


## En cas de problème

Si le react ne fonctionne pas, on peut passer par le swagger de l'api. Lancer le script webservice/app.py, puis dans un navigateur aller à http://0.0.0.0:8080/docs.

Installer les packages si nécessaire :  
> pip install -r requirements.txt
