# Fullstack

## Requirements

- python3
- pipenv (Pour l'environment virtuel)
- pip command
- Django
- Node Js (npm)

## Setup

### Back-end


L'API a été fait en python avec Django. 
Pour ne lancer que le backend en local il faut faire a l'interieur du dossier backend les commandes ci-dessous en bash:
```bash
cd customBackend/
pipenv shell
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8080
```
L'url du backend: http://172.18.0.1:8080/

### Frontend : Web

#### WEB : Vue js

Pour lancer manuellement le frontend il faut faire ces commandes a la racines du repos :

```bash
cd vue-frontend/
npm install
npm run dev
```

L'url du frontend: http://172.18.0.1:5173/
