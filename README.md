#Prédiction prix maison

Vous avez le choix entre lancer l'API en local ou travailler sur l'image de l'application dockerisé

Cas 1: Application en local

Etape 1: accéder à l'environnement virtuel myvenv pour installer les dépendances tout en évitant les conflits de package

1-1 : source myvenv/bin/activate (pour linux)
source myvenv/Scripts/activate (pour windows)

1-2: installer les dépendances
pip install -r requirements

Etape 2: lancer l'application
python app.py

Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)


Cas 2: Accéder à l'application via l'image dockerisé
 #construire l'image docker
 
 docker compose build (ou docker-compose build) selon votre version de docker compose

#vérifier si l'image est bien construite
 docker images
 (myvenv) (base) hans@hans-ThinkPad-E16-Gen-1:~/Projet_immo$ docker images
REPOSITORY                      TAG           IMAGE ID       CREATED         SIZE
projet_immo_ml-app              latest        2c4d8ff8a6ad   2 minutes ago   855MB

 l'image projet_immo_ml-app devrait être créée

 #démarrer le conteneur: lance ton application 
 docker compose up

 projet_immo-ml-app-1  | INFO:     Started server process [1]
projet_immo-ml-app-1  | INFO:     Waiting for application startup.
projet_immo-ml-app-1  | INFO:     Application startup complete.
projet_immo-ml-app-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

accéder à cet URL en local : Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

MERCI



#Signification du Dockerfile


Voici une explication détaillée de chaque section du Dockerfile :

1. FROM python:3.10-slim
Cette ligne spécifie l'image de base à utiliser pour créer ton image Docker.

python:3.10-slim est une version allégée (minimale) de l'image officielle Python, basée sur Debian. Elle inclut Python 3.10, mais avec moins de paquets inutiles par rapport à une image standard, ce qui permet de réduire la taille de l'image finale.

2. WORKDIR /app
Cette instruction définit le répertoire de travail à l'intérieur du conteneur Docker.

WORKDIR spécifie où seront placés tous les fichiers copiés dans le conteneur, et où les commandes suivantes seront exécutées.
Dans ton cas, le répertoire /app est créé et utilisé pour stocker ton application.

3. COPY requirements.txt .
Cette ligne copie ton fichier requirements.txt du répertoire local vers le répertoire de travail du conteneur (/app).

Cela permet à Docker d'installer les dépendances Python avant de copier le reste des fichiers de l'application, ce qui améliore l'efficacité du cache de Docker. Si les dépendances n'ont pas changé, Docker réutilisera l'étape précédente sans avoir besoin de reconstruire tout le conteneur.

4. RUN pip install --no-cache-dir -r requirements.txt
RUN exécute une commande dans le conteneur lors de la création de l'image.
Ici, il installe toutes les dépendances Python nécessaires spécifiées dans le fichier requirements.txt.
L'option --no-cache-dir permet d'éviter que les caches de pip ne soient stockés, réduisant ainsi la taille de l'image Docker.

5. COPY . .
Cette ligne copie tout le contenu du répertoire local (le répertoire où se trouve ton Dockerfile) dans le répertoire de travail du conteneur (/app).

Cela inclut ton fichier app.py, home.html, ton modèle (regmodel.pkl), ainsi que tout autre fichier nécessaire au fonctionnement de ton application.

6. EXPOSE 8000
EXPOSE est une instruction informelle qui indique que le conteneur écoute sur le port 8000.
C'est plus une indication pour Docker et d'autres outils que pour le fonctionnement réel de l'application.
Cela ne fait pas automatiquement "rediriger" les ports, mais c'est utile pour comprendre quel port l'application va utiliser.

7. CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD spécifie la commande par défaut à exécuter lorsque le conteneur est lancé.
Ici, il lance l'application avec uvicorn, le serveur ASGI utilisé par FastAPI.
"app:app" indique que le fichier Python à exécuter est app.py et que l'objet FastAPI à lancer est appelé app (c'est ce que tu as dans ton code).
--host 0.0.0.0 permet d'accepter les connexions de n'importe quelle adresse IP (utile dans un environnement Docker).
--port 8000 définit le port d'écoute du serveur à 8000, qui est ensuite mappé dans le fichier `docker-compose.yml




#Signification du docker compose

Voici l'explication détaillée de chaque section de ton fichier docker-compose.yml :

docker-compose.yml :


version: '3.8'
version : Indique la version du format de fichier docker-compose. Ici, tu utilises la version 3.8, qui est largement utilisée et compatible avec de nombreuses fonctionnalités modernes.


services:
  ml-app:
services : Cette section définit les différents services ou conteneurs que tu veux exécuter avec Docker Compose. Un service correspond à un conteneur Docker.
ml-app : C'est le nom du service, que tu choisis pour représenter ton application dans le fichier docker-compose.yml. Ce nom sera utilisé pour les opérations comme démarrer, arrêter ou lister le conteneur.


    build:
      context: .
      dockerfile: Dockerfile
build : Cette section permet de spécifier comment Docker doit construire l'image pour ce service.
context : Indique le répertoire où Docker doit chercher le fichier Dockerfile et tous les fichiers nécessaires pour construire l'image. Ici, le . signifie le répertoire actuel.
dockerfile : Spécifie explicitement quel fichier Dockerfile doit être utilisé pour construire l'image (ici Dockerfile), bien que si ton fichier Dockerfile porte le nom par défaut, cette ligne est optionnelle.


    ports:
      - "8000:8000"
ports : Cette section mappe les ports entre ton hôte (ta machine locale) et le conteneur Docker.
"8000:8000" : Cela signifie que le port 8000 de ton conteneur (qui est le port exposé par Uvicorn dans ton Dockerfile) sera mappé sur le port 8000 de ta machine hôte. Cela permet d'accéder à ton application via http://localhost:8000.


    volumes:
      - .:/app
volumes : Cette section permet de monter des répertoires de l'hôte (ta machine locale) dans le conteneur. Cela est utile pour le développement, car cela permet de modifier ton code localement sans avoir à reconstruire l'image Docker.
.:/app : Cela signifie que le répertoire courant (.) de ton hôte sera monté dans le répertoire /app à l'intérieur du conteneur. Le répertoire /app sera donc accessible par ton application dans le conteneur.


    environment:
      - PYTHONUNBUFFERED=1
environment : Cette section permet de définir des variables d'environnement dans le conteneur Docker.
PYTHONUNBUFFERED=1 : Cette variable est définie pour que les sorties de logs de Python (comme celles de print) s'affichent immédiatement dans la console, ce qui est utile pour le débogage.


Résumé :
version : Définit la version du format Docker Compose.
services : Contient la configuration des différents services à lancer avec Docker Compose.
ml-app : Nom du service.
build : Définit le répertoire et le fichier Dockerfile pour construire l'image.
ports : Mappage des ports entre l'hôte et le conteneur (permet d'accéder à l'application).
volumes : Monte le répertoire local dans le conteneur pour le développement.
environment : Définition de variables d'environnement pour le conteneur.
Ce que tu obtiens à partir de ce fichier :
Lorsque tu exécutes docker compose up :

Docker Compose va chercher à construire l'image à partir du Dockerfile que tu as fourni.
Ensuite, il démarre un conteneur avec cette image, et le service ml-app sera accessible sur le port 8000 de ta machine.
Les fichiers de ton projet local sont montés dans le conteneur pour que tu puisses voir les changements immédiatement sans avoir à reconstruire l'image chaque fois.


MERCI


