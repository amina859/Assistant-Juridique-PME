from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import glob
import os


# Chargement du fichier .env
load_dotenv()

# Configuration Gemini avec la clé
API_KEY = os.getenv("API_KEY")

from mistralai import Mistral
client = Mistral(api_key=API_KEY)

# Chemin pour sauvegarder le vectorstore
FAISS_INDEX_PATH = "faiss_index_juridique"

def load_vectorstore():
    if os.path.exists(FAISS_INDEX_PATH):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH, 
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    
    # Sinon, créer le vectorstore
    pdf_files = glob.glob("pdfs_juridiques/*.pdf")
    loaders = [PDFPlumberLoader(f) for f in pdf_files]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Sauvegarder le vectorstore
    vectorstore.save_local(FAISS_INDEX_PATH)
    return vectorstore


vectorstore = load_vectorstore()


def ask_rag(question: str):
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])
    
    # 2. Créer le prompt pour Mistral
    prompt = f"""Tu es Juris, un conseiller juridique expert en droit OHADA et droit du travail sénégalais. Tu travailles pour MyPME et tu aides les entrepreneurs et PME sénégalaises.

    COMPORTEMENT :
    - Parle comme un conseiller humain : naturel, chaleureux, direct.
    - Réponds DIRECTEMENT sans jamais répéter ou reformuler la question.
    - Adapte ton ton : simple pour les non-juristes, plus technique si la question l'exige.
    - Ne fais JAMAIS de liste sauf quand tu décris une procédure étape par étape ou une énumération incontournable. Sinon, écris en texte fluide et naturel.
    - Si tu donnes un conseil pratique, intègre-le naturellement dans ta réponse.
    - Cite les articles de loi de manière fluide dans le texte, ex : "selon l'article 43 du Code du travail...".
    - Sois concis. Pas de remplissage inutile. Ne sois pas long dans tes réponses, sois bref et précis.
    - Ajoute "Cette réponse a une valeur indicative et ne remplace pas un avocat." UNIQUEMENT quand la question porte sur un litige, une sanction, ou une situation légale sensible.
    - Tu peux répondre à toutes les questions liées aux PME : création d'entreprise, statuts juridiques, fiscalité, contrats, droit du travail, OHADA, immatriculation, financement, etc.
    - Refuse UNIQUEMENT les questions sans aucun lien avec le monde des affaires ou le droit (météo, sport, cuisine, etc.) en disant poliment que ce n'est pas ton domaine.

    Contexte juridique :
    {context}

    Question : {question}

    Réponds en français naturel et fluide :"""
        
    # 3. Générer avec Gemini
    response = client.chat.complete(model="mistral-small-latest", messages=[{"role": "user", "content": prompt}])
    
    # Retour de la réponse générée
    return response.choices[0].message.content


# FastAPI App
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Question(BaseModel):
    message: str

@app.post("/chat")
def chat(q: Question):
    return {"response": ask_rag(q.message)}