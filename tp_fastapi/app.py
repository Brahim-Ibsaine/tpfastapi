from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict
import pandas as pd
from pathlib import Path
import os


# Création de l'application FastAPI
app = FastAPI()

# Création de la sécurité de base HTTP
security = HTTPBasic()

# ============================ READ SECURITIE's FILE AS DF ============================
seed = pd.read_csv("Secure/Credentials.txt", encoding="utf-8", sep=":")
# Middleware pour vérifier l'authentification basique
async def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    
    # Récupération du nom d'utilisateur et du mot de passe fournis
    user = credentials.username
    password = credentials.password

    # Si les identifiants ne sont pas valides, une exception HTTP est levée
    if user not in list(seed.UID) or password not in list(seed.PWD):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


# Route racine, renvoie un message de bienvenue
@app.get("/")
def index():
    return {"message": "Welcome to FAST API SERVER..."}

# Route pour l'enregistrement d'un nouvel utilisateur
@app.post("/user/signup")
async def signup(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    
    # Vérifier si le nom d'utilisateur est déjà pris
    if username in seed.UID.unique():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Ajouter les nouvelles informations d'identification 
    seed.loc[len(seed)]= [username, password]
    seed.to_csv("Secure/Credentials.txt", encoding="utf-8", sep=":", index=False)
        
    return {"message": "User created successfully"}

# Route qui ne peut être accédée que si l'authentification basique est validée
@app.get("/user/whoami")
async def whoami(user: str = Depends(verify_basic_auth)):
    return {"info": seed.loc[seed.UID == user]}

# Route pour envoyer un fichier dans le système de fichiers de l'utilisateur en cours
@app.put("/files/{filename:path}")
async def upload_file(filename: str, file: UploadFile = File(...), user: str = Depends(verify_basic_auth)):
    try:
        # Vérifier si le chemin d'accés existe, sinon le créer 
        path = os.getcwd()+"\\"+user+'\\'+'\\'.join(str(filename).split("/")[:-1])
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = Path(path) / Path(str(filename).split("/")[-1])
        
        # Ècrire le contenu du fichier téléchargé sur le chemin d'accès spécifié
        with filepath.open("wb") as buffer:
            buffer.write(await file.read())
        return {"message": f"File '{filename}' chargement avec succèes."}
    except Exception as e:
        print(e)
        return {"message": "Une erreur est survenue !"}
    
# Supprimer le fichier associé à filename qu’il existe ou non si l'utilisateur est authentifié
@app.delete("/files/{filename:path}")
def delete_file(filename: str, user: str = Depends(verify_basic_auth)):
    # Construction du chemin complet du fichier
    file_path = os.path.join(os.getcwd(), user+"\\"+filename)
    try:
        # Supprimer le fichier
        os.remove(file_path)
        return {"message": f"Le fichier {filename} a été supprimé avec succès."}
    except FileNotFoundError:
        return {"message": f"Le fichier {filename} n'existe pas."}
    except:
        return {"message": f"Une erreur est survenue lors de la suppression du fichier {filename}."}
    
# Fonction de récupération de fichier
def get_file_content(filename: str):
    file_path = Path(filename)
    if not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fichier introuvable")
    with open(file_path, "rb") as file:
        contents = file.read()
    return contents

# Route GET pour récupérer un fichier associé depuis le système de stockage
@app.get("/files/{filename:path}")
async def read_file(filename: str, user: str = Depends(verify_basic_auth)):
    file_content = get_file_content(user+"\\"+filename)
    return {"filename": filename, "content": file_content}

def list_files(path):
    files = []
    for entry in os.scandir(path):
        if entry.is_file():
            files.append(entry.path)
        elif entry.is_dir():
            files.extend(list_files(entry.path))
    return files

@app.get("/prefix/{prefix}", include_in_schema=False)
async def prefix_file(prefix: str, user: str = Depends(verify_basic_auth)):
    user_directory = user+"\\"+prefix
    print(user_directory)
    tree = list_files(user_directory)[0].replace(user+"\\", "")
    return {"Prefix": tree}
    