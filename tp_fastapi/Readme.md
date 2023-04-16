Introduction : 
    
    Ce code implémente un service RESTful basé sur FastAPI, qui fournit des fonctions d'authentification, de stockage de fichiers et de suppression de fichiers. Les utilisateurs peuvent s'inscrire et créer un compte en fournissant un nom d'utilisateur et un mot de passe. Ils peuvent ensuite se connecter avec leurs identifiants pour accéder aux fonctionnalités de stockage de fichiers.


Fonctionnalités :
    1. GET /: Une route d'accueil pour vérifier que le serveur web est en cours d'exécution.
    2. POST/user/signup: Une route pour créer un nouveau compte utilisateur.
    3. GEST/user/whoami: Une route pour récupérer les informations utilisateurs
    4. PUT/files/{filename:path}: Une route qui permet d'envoyer un fichier et qui portera comme nom celui de la variable "filename".
    5. GET/files/{filename:path}: Une route pour récupérer un fichier depuis le système de stockage.
    6. DELETE/file/{filename:path}: Une route qui permet de supprimer le fichier associé à filename.
    7. GET/prefix/{prefix}: Une route pour récupérer un ensemble de fichiers sous le préfix "prefix".


Installation :
    1. Installation des dépendances :
    pip install fastapi pandas[all]

    2. Exécution du script : 
    uvicorn api.app:app --reload


Utilisation : 
    1. Créez un compte en envoyant une requête POST à l'URL http://127.0.0.1:8000/user/signup en utilisant les paramètres d'authentification de base.

    2. Connectez-vous en envoyant une requête GET à l'URL http://127.0.0.1:8000/user/whoami en utilisant les paramètres d'authentification de base.

    3. Téléchargez un fichier en envoyant une requête PUT à l'URL http://127.0.0.1:8000/files/{filename:path} en utilisant les paramètres d'authentification de base et en incluant un fichier dans le corps de la requête.

    4. Récupérez un fichier en envoyant une requête GET à l'URL http://127.0.0.1:8000/files/{filename:path} en utilisant les paramètres d'authentification de base.

    5. Supprimez un fichier en envoyant une requête DELETE à l'URL http://127.0.0.1:8000/files/{filename:path} en utilisant les paramètres d'authentification de base.
    
    6. Récupérez le chemin des fichiers dans un dossier spécifié d'un utilisateur en envoyant une requête GET à l'URL `http://127.0.0.1:8000/prefix/{prefix}