from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import re
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError(
        "API_KEY introuvable. Ajoutez-le dans le fichier .env ou dans les variables d'environnement."
    )

from mistralai.client import Mistral
client = Mistral(api_key=API_KEY)

FAISS_INDEX_PATH = "faiss_index_juridique"
PDF_DIR_NAME = "pdfs_juridiques"


def load_vectorstore():
    data_dir = Path(__file__).parent
    faiss_path = data_dir / FAISS_INDEX_PATH
    pdf_dir = data_dir / PDF_DIR_NAME

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if faiss_path.exists():
        vectorstore = FAISS.load_local(
            str(faiss_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )
        return vectorstore

    pdf_files = sorted(str(p) for p in pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"Aucun fichier PDF trouvé dans {pdf_dir}")

    documents = []
    for pdf_path in pdf_files:
        loader = PDFPlumberLoader(pdf_path)
        loaded = loader.load()
        if loaded:
            documents.extend(loaded)

    if not documents:
        raise ValueError("Aucun document PDF valide n'a été chargé.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    if not docs:
        raise ValueError("Aucune page n'a été produite après le découpage.")

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(str(faiss_path))
    return vectorstore


vectorstore = load_vectorstore()


# ── Extraction de citations depuis les métadonnées et le contenu des chunks ──

_LAW_PATTERNS = [
    r"(?:article|art\.?)\s+(?:L[\.\-]?)?\d+(?:[\-\.]\d+)*(?:\s+(?:du|de\s+la|de\s+l[\''])\s+[\w\s]+?(?=,|\.|;|$))?",
    r"loi\s+n[°o]?\s*\d{2,4}[\-/]\d{2,4}",
    r"décret\s+n[°o]?\s*\d{2,4}[\-/]\d{2,4}",
    r"acte\s+uniforme\s+[\w\s]+?(?=,|\.|;|\n|$)",
    r"\b(?:AUD(?:CG|CGI|CAP|SCGIE|TVS|PE)|OHADA|UEMOA|BCEAO|CIMA|Code\s+du\s+travail)\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _LAW_PATTERNS]


def _source_label(metadata: dict) -> str:
    source = metadata.get("source", "")
    page = metadata.get("page")
    if source:
        name = Path(source).stem
        name = re.sub(r"[_\-]+", " ", name).title()
        if page is not None:
            return f"{name} · p. {int(page) + 1}"
        return name
    return ""


def extract_citations(docs_with_scores: list) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []

    for doc, _score in docs_with_scores:
        label = _source_label(doc.metadata)
        if label and label not in seen:
            seen.add(label)
            results.append(label)

        for pattern in _COMPILED:
            for m in pattern.finditer(doc.page_content):
                raw = m.group(0).strip()
                clean = re.sub(r"\s+", " ", raw)[:60].rstrip(" ,;.")
                if len(clean) > 4 and clean.lower() not in seen:
                    seen.add(clean.lower())
                    results.append(clean[0].upper() + clean[1:])

        if len(results) >= 5:
            break

    return results[:5]


def compute_confidence(docs_with_scores: list) -> int:
    if not docs_with_scores:
        return 50

    distances = [score for _, score in docs_with_scores[:3]]
    avg_dist = sum(distances) / len(distances)

    confidence = max(40, min(100, int(100 - avg_dist * 30)))
    return confidence


def ask_rag(question: str) -> dict:
    docs_with_scores = vectorstore.similarity_search_with_score(question, k=3)

    context = "\n".join([doc.page_content for doc, _ in docs_with_scores])

    citations = extract_citations(docs_with_scores)
    confidence = compute_confidence(docs_with_scores)

    citation_hint = ""
    if citations:
        citation_hint = (
            "\nRéférences disponibles dans le contexte : "
            + ", ".join(citations[:3])
            + ".\nCite-les naturellement dans ta réponse si pertinent."
        )

    prompt = f"""Tu es Juris, un conseiller juridique expert en droit OHADA et droit du travail sénégalais. Tu travailles pour MyPME et tu aides les entrepreneurs et PME sénégalaises.

COMPORTEMENT :
- Parle comme un conseiller humain : naturel, chaleureux, direct.
- Réponds DIRECTEMENT sans jamais répéter ou reformuler la question.
- Adapte ton ton : simple pour les non-juristes, plus technique si la question l'exige.
- Ne fais JAMAIS de liste sauf quand tu décris une procédure étape par étape ou une énumération incontournable. Sinon, écris en texte fluide et naturel.
- Si tu donnes un conseil pratique, intègre-le naturellement dans ta réponse.
- Cite les articles de loi de manière fluide dans le texte, ex : "selon l'article 43 du Code du travail...".
- Sois concis. Pas de remplissage inutile. Sois bref et précis.
- Ajoute "Cette réponse a une valeur indicative et ne remplace pas un avocat." UNIQUEMENT quand la question porte sur un litige, une sanction, ou une situation légale sensible.
- Tu peux répondre à toutes les questions liées aux PME : création d'entreprise, statuts juridiques, fiscalité, contrats, droit du travail, OHADA, immatriculation, financement, etc.
- Refuse UNIQUEMENT les questions sans aucun lien avec le monde des affaires ou le droit en disant poliment que ce n'est pas ton domaine.
{citation_hint}

Contexte juridique :
{context}

Question : {question}

Réponds en français naturel et fluide :"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content

    return {
        "response": answer,
        "citations": citations,
        "confidence": confidence,
    }


# ── Hub de documents : listing + recherche + téléchargement ──────────────────

# Catégorisation simple par mots-clés présents dans le nom de fichier.
_CATEGORY_RULES = [
    (("travail", "emploi", "salari", "licenciement"), "Droit du travail"),
    (("ohada", "audcg", "auscgie", "aupcap", "acte uniforme"), "OHADA"),
    (("fiscal", "impot", "impôt", "tva", "uemoa"), "Fiscalité"),
    (("contrat", "bail", "vente", "commercial"), "Contrats"),
    (("societe", "société", "sarl", "sa ", "rccm"), "Droit des sociétés"),
]


def _categorize(filename: str) -> str:
    lower = filename.lower()
    for keywords, category in _CATEGORY_RULES:
        if any(kw in lower for kw in keywords):
            return category
    return "Général"


def _list_documents() -> list[dict]:
    pdf_dir = Path(__file__).parent / PDF_DIR_NAME
    if not pdf_dir.exists():
        return []

    docs = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        stat = pdf_path.stat()
        display_name = re.sub(r"[_\-]+", " ", pdf_path.stem).strip().title()
        docs.append(
            {
                "filename": pdf_path.name,
                "display_name": display_name,
                "category": _categorize(pdf_path.name),
                "size_kb": round(stat.st_size / 1024, 1),
            }
        )
    return docs


# ── FastAPI App ───────────────────────────────────────────────────────────────

app = FastAPI(title="MyPME · Assistant Juridique API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def root():
    return {"status": "ok", "message": "MyPME · Assistant Juridique API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


class Question(BaseModel):
    message: str


@app.post("/chat")
def chat(q: Question):
    return ask_rag(q.message)


@app.get("/documents")
def list_documents(q: str = ""):
    """
    Liste les documents de la base de connaissances.
    Si `q` est fourni, filtre par mot-clé sur le nom de fichier et la catégorie
    (insensible à la casse, sans accents stricts).
    """
    docs = _list_documents()

    if q:
        needle = q.strip().lower()
        docs = [
            d
            for d in docs
            if needle in d["display_name"].lower()
            or needle in d["category"].lower()
            or needle in d["filename"].lower()
        ]

    return {"count": len(docs), "documents": docs}


@app.get("/documents/download/{filename}")
def download_document(filename: str):
    """Télécharge un PDF de la base de connaissances par son nom de fichier exact."""
    # Sécurité : empêcher toute traversée de répertoire (../, chemins absolus, etc.)
    safe_name = Path(filename).name
    if safe_name != filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    pdf_dir = Path(__file__).parent / PDF_DIR_NAME
    file_path = pdf_dir / safe_name

    try:
        file_path = file_path.resolve()
        pdf_dir_resolved = pdf_dir.resolve()
        if pdf_dir_resolved not in file_path.parents and file_path != pdf_dir_resolved:
            raise HTTPException(status_code=400, detail="Chemin invalide.")
    except (OSError, RuntimeError):
        raise HTTPException(status_code=400, detail="Chemin invalide.")

    if not file_path.exists() or file_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="Document introuvable.")

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=safe_name,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)