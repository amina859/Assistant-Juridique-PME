# Assistant-Juridique-PME

MyPME est une API intelligente développée avec FastAPI qui répond à des questions juridiques via un système RAG (Retrieval-Augmented Generation).

Les composants principaux :

- `app.py` : backend FastAPI. Charge les PDF, construit (ou charge) un vectorstore FAISS et expose `/chat`.
- `interface.py` : interface Streamlit qui interroge le backend.
- `pdfs_juridiques/` : documents sources (.pdf).
- `faiss_index_juridique/` : répertoire où le vectorstore est sauvegardé après génération.

Ce README décrit la procédure complète pour exécuter l'application en local (Windows PowerShell). Adaptez les chemins et commandes si vous travaillez sur macOS / Linux.

## Prérequis

- Python 3.10 ou supérieur
- `pip` et `virtualenv` (ou venv intégré)
- Accès Internet (téléchargement des modèles Hugging Face)

## Étapes détaillées

1) Ouvrir PowerShell et se placer dans le dossier du projet :

```powershell
cd "C:\Users\DELL 5420\Documents\Big Data L3\Semestre 2\Gestion de projet IA\Assistant-Juridique-PME"
```

2) Créer et activer un environnement virtuel, puis installer les dépendances :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Sous macOS / Linux : `source .venv/bin/activate`

3) Créer un fichier `.env` à la racine du projet et ajouter au minimum :

```
API_KEY=VOTRE_CLE_MISTRAL
# Optionnel mais recommandé :
HF_TOKEN=VOTRE_HF_TOKEN
```

Remplacez `VOTRE_CLE_MISTRAL` par la clé API nécessaire pour l'API Mistral (ou autre fournisseur configuré). `HF_TOKEN` réduit les limites de débit lors du téléchargement des modèles.

4) Vérifier la présence des PDFs

Assurez-vous que `pdfs_juridiques/` contient des fichiers `.pdf`. S'il n'y en a pas, ajoutez vos documents avant de lancer le backend.

5) Démarrer le backend FastAPI

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Le premier démarrage peut prendre du temps : le modèle d'encodage Hugging Face sera téléchargé et l'index FAISS sera construit à partir des PDFs. Vérifiez que la sortie contient `Application startup complete.`

Accédez à la documentation interactive :

```
http://127.0.0.1:8000/docs
```

6) Démarrer l'interface Streamlit (nouveau terminal)

```powershell
streamlit run interface.py
```

Ouvrez l'URL indiquée (généralement `http://localhost:8501`) et posez vos questions.

7) Tests rapides

```powershell
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"message":"Bonjour"}'
```

## Résolution des problèmes courants

- `ImportError: cannot import name 'Mistral'` :
	- Le code utilise `from mistralai.client import Mistral`. Vérifiez que `mistralai` est installé dans le venv (`pip show mistralai`).

- `IndexError: list index out of range` lors de la création du vecteur :
	- Vérifiez que des documents ont bien été chargés depuis `pdfs_juridiques/`.
	- Pour reconstruire l'index : supprimez le dossier `faiss_index_juridique/` puis redémarrez le backend.

- `Warning: You are sending unauthenticated requests to the HF Hub` :
	- Ajoutez `HF_TOKEN` à `.env` pour éviter les limites et warnings.

- `Erreur : impossible de joindre le serveur.` dans Streamlit :
	- Assurez-vous que le backend est démarré et accessible sur `127.0.0.1:8000`.

- `missing ScriptRunContext` :
	- N'utilisez pas `python interface.py`. Lancez via `streamlit run interface.py`.

## Commandes récapitulatives

```powershell
cd "Assistant-Juridique-PME"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
streamlit run interface.py
```

## Remarques

- Pour la production, stockez les clés dans un gestionnaire de secrets et protégez CORS.
- Si vous voulez, je peux ajouter un script PowerShell `run.ps1` ou un `Makefile` pour automatiser ces étapes.

Bonne utilisation !
