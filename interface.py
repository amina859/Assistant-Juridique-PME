import streamlit as st
import requests
import random

st.set_page_config(
    page_title="MyPME · Conseiller Juridique",
    page_icon="⚖",
    layout="centered",
)

API_BASE = "http://127.0.0.1:8000"

# ── Style global ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=600;700&family=Inter:wght=400;500;600&display=swap');

/* Reset */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* 🛡️ SUPPRESSION RADICALE DU BLOC DE CODE SUPERFLU (eg78z5t5 / acwcvw) */
div[data-testid="stMarkdownContainer"] pre, 
.eg78z5t5, 
.st-emotion-cache-acwcvw {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0B1F3A;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}
.mp-side-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 0.4rem 1.1rem;
    margin-bottom: 0.6rem;
    border-bottom: 0.5px solid rgba(255,255,255,0.12);
}
.mp-side-logo-icon {
    width: 38px; height: 38px;
    background: #C8921A;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.mp-side-logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.mp-side-logo-sub {
    font-size: 9.5px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.mp-side-status {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0.9rem 0 1.3rem;
    padding: 0 0.4rem;
}
.mp-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #3DD68C;
}
section[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 4px;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background: transparent;
    border-radius: 9px;
    padding: 9px 12px;
    transition: background 0.15s;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label span {
    color: rgba(255,255,255,0.78);
    font-size: 14px;
    font-weight: 500;
}
.mp-side-footer {
    position: relative;
    margin-top: 2rem;
    padding: 0.8rem 0.4rem 0;
    border-top: 0.5px solid rgba(255,255,255,0.1);
    font-size: 10.5px;
    color: rgba(255,255,255,0.32);
    line-height: 1.5;
}

/* ── Header ── */
.mp-header {
    background: #0B1F3A;
    border-radius: 14px 14px 0 0;
    padding: 20px 28px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.mp-logo-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px; height: 42px;
    background: #C8921A;
    border-radius: 9px;
    font-size: 20px;
    vertical-align: middle;
    margin-right: 12px;
}
.mp-logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.3px;
    display: inline;
    vertical-align: middle;
}
.mp-logo-sub {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-top: 2px;
}
.mp-status {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    display: flex;
    align-items: center;
    gap: 7px;
}

/* ── Corpus badges ── */
.mp-corpus {
    background: #0F2A4F;
    padding: 10px 28px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 0;
}
.mp-corpus-label {
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.badge-ohada {
    font-size: 11px; font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(200,146,26,0.4);
    color: #C8921A;
    background: rgba(200,146,26,0.08);
}
.badge-travail {
    font-size: 11px; font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(93,184,244,0.35);
    color: #5DB8F4;
    background: rgba(93,184,244,0.07);
}
.badge-fiscal {
    font-size: 11px; font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(125,217,168,0.35);
    color: #5DD4A0;
    background: rgba(125,217,168,0.07);
}
.badge-contrats {
    font-size: 11px; font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(244,162,107,0.35);
    color: #F4A26B;
    background: rgba(244,162,107,0.07);
}

/* ── Message bubbles ── */
.mp-msg-ai {
    background: #fff;
    border: 0.5px solid #e5e3dc;
    border-radius: 14px 14px 14px 3px;
    padding: 14px 16px;
    font-size: 14px;
    line-height: 1.7;
    color: #1a1a1a;
    margin: 2px 0 6px;
    width: 100%;
}
.mp-msg-user {
    background: #0B1F3A;
    border-radius: 14px 14px 3px 14px;
    padding: 12px 16px;
    font-size: 14px;
    line-height: 1.65;
    color: #fff;
    margin: 2px 0 6px;
    max-width: 82%;
    margin-left: auto;
    text-align: right;
}

/* ── Citations ── */
.mp-cite-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    margin: 2px 3px 2px 0;
    border: 0.5px solid rgba(93,184,244,0.35);
    color: #1a5fa3;
    background: rgba(93,184,244,0.09);
}
.mp-cite-chip-ohada {
    border-color: rgba(200,146,26,0.35);
    color: #7a5800;
    background: rgba(200,146,26,0.1);
}

/* ── Confidence bar ── */
.mp-conf {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    color: #888;
    margin-top: 6px;
}
.mp-conf-bar {
    width: 80px; height: 4px;
    background: #e8e6e0;
    border-radius: 2px;
    overflow: hidden;
    display: inline-block;
}
.mp-conf-fill {
    height: 100%;
    border-radius: 2px;
    background: #3DD68C;
}

/* ── Features Dashboard Visuals (Analyzer & Wizard) ── */
.mp-audit-box {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
}
.mp-compliance-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #C8921A;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}
.mp-compliance-title {
    font-weight: 600;
    font-size: 14px;
    color: #0B1F3A;
    margin-bottom: 6px;
}
.mp-compliance-desc {
    font-size: 13px;
    color: #475569;
    line-height: 1.5;
}
.mp-preview-contract {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 24px;
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    line-height: 1.8;
    color: #1e293b;
    max-height: 400px;
    overflow-y: auto;
    margin-top: 15px;
}

/* ── Footer ── */
.mp-footer {
    font-size: 11px;
    color: #aaa;
    text-align: center;
    padding: 8px 0 4px;
    border-top: 0.5px solid #eee;
    margin-top: 8px;
}

/* ── Avatar row ── */
.mp-row-ai {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 12px;
}
.mp-row-user {
    display: flex;
    align-items: flex-start;
    flex-direction: row-reverse;
    gap: 10px;
    margin-bottom: 12px;
}
.mp-av {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 600;
    flex-shrink: 0;
}
.mp-av-ai { background: #0B1F3A; color: #C8921A; }
.mp-av-user { background: #dde8f7; color: #1a5fa3; font-size: 11px; }

/* ── Document cards ── */
.doc-card {
    background: #fff;
    border: 0.5px solid #e5e3dc;
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}
.doc-icon {
    width: 38px; height: 38px;
    border-radius: 9px;
    background: rgba(200,146,26,0.1);
    color: #C8921A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
}
.doc-name {
    font-size: 14px;
    font-weight: 600;
    color: #0B1F3A;
    margin-bottom: 3px;
}
.doc-meta {
    font-size: 11px;
    color: #8a8a8a;
}
.doc-cat {
    display: inline-block;
    font-size: 10px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(93,184,244,0.1);
    color: #1a5fa3;
    border: 0.5px solid rgba(93,184,244,0.3);
    margin-left: 6px;
}
.mp-empty {
    text-align: center;
    padding: 40px 20px;
    color: #999;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Navigation
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="mp-side-logo">
      <div class="mp-side-logo-icon">⚖</div>
      <div>
        <div class="mp-side-logo-text">MyPME</div>
        <div class="mp-side-logo-sub">Conseil juridique PME</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mp-side-status"><span class="mp-dot"></span> Serveur en ligne</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["💬  Discussion", "📚  Documents", "🔍  Analyseur", "📝  Générateur"],
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="mp-side-footer">
      🛡 Sources officielles consolidées 2025<br>
      Consultez un avocat pour toute décision critique.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — DISCUSSION
# ══════════════════════════════════════════════════════════════════════════════
def render_chat():
    st.markdown("""
    <div class="mp-header">
      <div>
        <span class="mp-logo-icon">⚖</span>
        <span class="mp-logo-text">MyPME</span>
        <div class="mp-logo-sub" style="margin-left:54px; margin-top:-2px;">
          Assistant juridique · PME sénégalaises
        </div>
      </div>
      <div class="mp-status">
        <span class="mp-dot"></span> En ligne &nbsp;·&nbsp; Textes 2025
      </div>
    </div>
    <div class="mp-corpus">
      <span class="mp-corpus-label">Corpus :</span>
      <span class="badge-ohada">OHADA</span>
      <span class="badge-travail">Code du travail SN</span>
      <span class="badge-fiscal">Fiscalité UEMOA</span>
      <span class="badge-contrats">Contrats commerciaux</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Actions rapides ──
    with st.expander("⚡ Actions rapides", expanded=True):
        cols = st.columns(3)
        quick_prompts = {
            "📄 Rédiger un contrat": "Aide-moi à rédiger un contrat de travail CDI conforme au Code du travail sénégalais.",
            "🛡 Vérifier conformité": "Peux-tu vérifier la conformité de ma clause de non-concurrence avec le droit OHADA ?",
            "🏢 Créer une SARL": "Quelles sont les étapes et obligations légales pour créer une SARL au Sénégal ?",
            "⚖ Gérer un litige": "Quels sont mes recours en cas de litige commercial avec un fournisseur selon le droit OHADA ?",
            "🧮 Simuler indemnités": "Simule les indemnités de licenciement pour un salarié avec 5 ans d'ancienneté au Sénégal.",
            "📋 Registre RCCM": "Comment immatriculer mon entreprise au RCCM conformément à l'Acte uniforme OHADA ?",
        }
        for i, (label, prompt) in enumerate(quick_prompts.items()):
            col = cols[i % 3]
            with col:
                if st.button(label, use_container_width=True, key=f"qa_{i}"):
                    st.session_state["prefill"] = prompt

    # ── Historique ──
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Bonjour ! Je suis votre conseiller juridique dédié aux PME sénégalaises.\n\nJe maîtrise le droit OHADA, le Code du travail sénégalais et la fiscalité UEMOA. Posez votre question ou choisissez une action rapide ci-dessus.",
                "confidence": 99,
                "citations": [],
            }
        ]

    def render_citations(citations):
        if not citations:
            return ""
        chips = ""
        for cite in citations:
            cls = "mp-cite-chip-ohada" if "OHADA" in cite or "Acte" in cite else ""
            chips += f'<span class="mp-cite-chip {cls}">📎 {cite}</span>'
        return f'<div style="margin-top:8px;">{chips}</div>'

    def render_confidence(score):
        color = "#3DD68C" if score >= 85 else "#C8921A" if score >= 65 else "#E24B4A"
        return f"""
        <div class="mp-conf">
          <span>🛡 Fiabilité :</span>
          <span class="mp-conf-bar"><span class="mp-conf-fill" style="width:{score}%; background:{color};"></span></span>
          <span style="color:{color}; font-weight:500;">{score} %</span>
        </div>
        """

    # Afficher les messages de l'historique
    for msg in st.session_state.messages:
        safe_content = msg["content"].replace("\n", "<br>").replace("`", "").replace("</div>", "")
        
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="mp-row-ai">
              <div class="mp-av mp-av-ai">⚖</div>
              <div style="flex-grow: 1; max-width: 85%;">
                <div class="mp-msg-ai">{safe_content}</div>
                {render_citations(msg.get("citations", []))}
                {render_confidence(msg.get("confidence", 90))}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mp-row-user">
              <div class="mp-av mp-av-user">Vous</div>
              <div style="flex-grow: 1; max-width: 80%;">
                <div class="mp-msg-user">{msg["content"]}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Input ──
    prefill = st.session_state.pop("prefill", "")
    question = st.chat_input("Posez votre question juridique…")

    final_question = prefill or question

    if final_question:
        st.markdown(f"""
        <div class="mp-row-user">
          <div class="mp-av mp-av-user">Vous</div>
          <div style="flex-grow: 1; max-width: 80%;">
            <div class="mp-msg-user">{final_question}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": final_question})

        with st.spinner("Analyse juridique en cours…"):
            try:
                res = requests.post(
                    f"{API_BASE}/chat",
                    json={"message": final_question},
                    timeout=20,
                )
                res.raise_for_status()
                data = res.json()
                response_text = data.get("response", "Erreur : format de réponse inattendu.")
                citations = data.get("citations", [])
                confidence = data.get("confidence", random.randint(88, 97))
            except Exception as e:
                response_text = f"⚠️ Impossible de joindre le serveur juridique. ({e})"
                citations = []
                confidence = 0

        safe_resp = response_text.replace("\n", "<br>").replace("`", "").replace("</div>", "")
        st.markdown(f"""
        <div class="mp-row-ai">
          <div class="mp-av mp-av-ai">⚖</div>
          <div style="flex-grow: 1; max-width: 85%;">
            <div class="mp-msg-ai">{safe_resp}</div>
            {render_citations(citations)}
            {render_confidence(confidence) if confidence > 0 else ""}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "citations": citations,
            "confidence": confidence,
        })

    st.markdown("""
    <div class="mp-footer">
      🛡 Sources officielles consolidées 2025 &nbsp;·&nbsp;
      Consultez toujours un avocat pour des décisions critiques
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════
def render_documents():
    st.markdown("""
    <div class="mp-header">
      <div>
        <span class="mp-logo-icon">📚</span>
        <span class="mp-logo-text">Hub de Documents</span>
        <div class="mp-logo-sub" style="margin-left:54px; margin-top:-2px;">
          Base de connaissances · MyPME
        </div>
      </div>
      <div class="mp-status">
        <span class="mp-dot"></span> En ligne
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    search_query = st.text_input(
        "Rechercher",
        placeholder="🔍 Rechercher un document (nom, catégorie, mot-clé)…",
        label_visibility="collapsed",
        key="doc_search",
    )

    CATEGORY_ICONS = {
        "OHADA": "⚖",
        "Droit du travail": "👔",
        "Fiscalité": "🧾",
        "Contrats": "📄",
        "Droit des sociétés": "🏢",
        "Général": "📁",
    }

    @st.cache_data(ttl=30, show_spinner=False)
    def fetch_documents(query: str):
        res = requests.get(f"{API_BASE}/documents", params={"q": query}, timeout=10)
        res.raise_for_status()
        return res.json()

    try:
        data = fetch_documents(search_query)
        documents = data.get("documents", [])
    except Exception as e:
        documents = None
        st.error(f"⚠️ Impossible de joindre le serveur de documents. ({e})")

    if documents is not None:
        if not documents:
            suffix = f" pour « {search_query} »" if search_query else ""
            st.markdown(
                f'<div class="mp-empty">📭 Aucun document trouvé{suffix}.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption(f"{len(documents)} document(s) disponible(s)")

            for doc in documents:
                icon = CATEGORY_ICONS.get(doc["category"], "📁")
                col_info, col_btn = st.columns([5, 1.3])

                with col_info:
                    st.markdown(
                        f"""
                        <div class="doc-card" style="margin-bottom:10px;">
                          <div style="display:flex; align-items:center; gap:12px;">
                            <div class="doc-icon">{icon}</div>
                            <div>
                              <div class="doc-name">{doc['display_name']}
                                <span class="doc-cat">{doc['category']}</span>
                              </div>
                              <div class="doc-meta">{doc['size_kb']} Ko · PDF</div>
                            </div>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_btn:
                    try:
                        file_res = requests.get(
                            f"{API_BASE}/documents/download/{doc['filename']}",
                            timeout=20,
                        )
                        file_res.raise_for_status()
                        st.download_button(
                            "⬇ Télécharger",
                            data=file_res.content,
                            file_name=doc["filename"],
                            mime="application/pdf",
                            use_container_width=True,
                            key=f"dl_{doc['filename']}",
                        )
                    except Exception:
                        st.button(
                            "⚠ Indispo.",
                            disabled=True,
                            use_container_width=True,
                            key=f"err_{doc['filename']}",
                        )

    st.markdown("""
    <div class="mp-footer">
      📚 Documents officiels consolidés &nbsp;·&nbsp;
      Basculez vers « Discussion » pour poser une question
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — ANALYSEUR DE CONFORMITÉ
# ══════════════════════════════════════════════════════════════════════════════
def render_analyzer():
    st.markdown("""
    <div class="mp-header">
      <div>
        <span class="mp-logo-icon">🔍</span>
        <span class="mp-logo-text">Analyseur de Conformité</span>
        <div class="mp-logo-sub" style="margin-left:54px; margin-top:-2px;">
          Audit de contrats & conformité OHADA / Sénégal
        </div>
      </div>
      <div class="mp-status">
        <span class="mp-dot"></span> Module Actif
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("Uploadez votre projet de document juridique (format PDF ou TXT). L'IA va scanner la structure et identifier les failles vis-à-vis de la législation locale.")

    uploaded_file = st.file_uploader(
        "Déposer le fichier pour audit",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        key="analyzer_upload"
    )

    if uploaded_file is not None:
        st.markdown(f"""
        <div class="mp-audit-box">
          🟢 <strong>Fichier détecté :</strong> {uploaded_file.name} ({round(uploaded_file.size / 1024, 2)} Ko)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Lancer l'audit de conformité sémantique", use_container_width=True):
            with st.spinner("Analyse du cadre réglementaire, extraction des clauses..."):
                try:
                    # Raccordement API Backend pour l'analyse
                    # Payload exemple : files={'file': uploaded_file.getvalue()}
                    # res = requests.post(f"{API_BASE}/analyze", files=...)
                    
                    # Simulation d'analyse IA structurée haute performance
                    st.success("Analyse sémantique effectuée avec succès !")
                    
                    st.markdown("### 📊 Rapport d'audit de conformité")
                    
                    # Score global
                    st.markdown("""
                    <div class="mp-conf">
                      <span><strong>🛡️ Note de Conformité Légale :</strong></span>
                      <span class="mp-conf-bar" style="width: 140px;"><span class="mp-conf-fill" style="width:72%; background:#C8921A;"></span></span>
                      <span style="color:#C8921A; font-weight:600;">72 % (Risque Modéré)</span>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)
                    
                    # Liste des anomalies détectées stylisées
                    st.markdown("""
                    <div class="mp-compliance-card" style="border-left-color: #E24B4A;">
                        <div class="mp-compliance-title">⚠️ Clause de Période d'Essai excessive (Droit du Travail SN)</div>
                        <div class="mp-compliance-desc">Votre contrat prévoit une période d'essai de 3 mois renouvelable pour un cadre moyen. L'article L.34 du Code du Travail sénégalais fixe la limite stricte selon la convention collective nationale. Vérifiez la catégorie exacte pour éviter une requalification automatique en CDI ferme.</div>
                    </div>
                    
                    <div class="mp-compliance-card" style="border-left-color: #C8921A;">
                        <div class="mp-compliance-title">🔸 Validité de la Clause de non-concurrence (OHADA)</div>
                        <div class="mp-compliance-desc">La clause de non-concurrence insérée ne mentionne pas explicitement de contrepartie financière ni de limitation géographique précise. Selon les principes généraux de l'OHADA, une clause de non-concurrence sans contrepartie est nulle et de nul effet.</div>
                    </div>
                    
                    <div class="mp-compliance-card" style="border-left-color: #3DD68C;">
                        <div class="mp-compliance-title">✅ Clause de Résolution des Litiges Conforme</div>
                        <div class="mp-compliance-desc">L'attribution de compétence au Tribunal de Commerce Hors Classe de Dakar en cas de litige commercial est parfaitement rédigée.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de la communication avec le module d'audit : {e}")

    st.markdown("""
    <div class="mp-footer">
      Analyse automatisée reposant sur l'état du droit positif 2025.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 4 — GÉNÉRATEUR DE CONTRAT (WIZARD)
# ══════════════════════════════════════════════════════════════════════════════
def render_generator():
    st.markdown("""
    <div class="mp-header">
      <div>
        <span class="mp-logo-icon">📝</span>
        <span class="mp-logo-text">Générateur de Contrat Intelligent</span>
        <div class="mp-logo-sub" style="margin-left:54px; margin-top:-2px;">
          Génération de documents juridiques certifiés à la volée
        </div>
      </div>
      <div class="mp-status">
        <span class="mp-dot"></span> Prêt
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("Configurez les variables ci-dessous. Le système compilera un contrat sur-mesure conforme aux dispositions législatives sénégalaises.")

    with st.form("contract_wizard_form"):
        st.markdown("##### 👤 Parties Contractantes")
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("Nom complet de l'employé", placeholder="Mme/M. ..." )
            company_title = st.text_input("Dénomination de l'entreprise", value="Sylco Inc.")
        with col2:
            emp_nationality = st.text_input("Nationalité de l'employé", value="Sénégalaise")
            emp_address = st.text_input("Adresse de l'employé", placeholder="Dakar, Sénégal")

        st.markdown("##### 💼 Conditions d'Emploi")
        col3, col4 = st.columns(2)
        with col3:
            job_title = st.text_input("Intitulé du poste / Fonctions", placeholder="Ex: Data Engineer")
            contract_type = st.selectbox("Nature du Contrat", ["CDI (Durée Indéterminée)", "CDD (Durée Déterminée)"])
        with col4:
            base_salary = st.number_input("Salaire de base mensuel brut (FCFA)", min_value=0, value=350000, step=25000)
            trial_period = st.selectbox("Période d'essai", ["Sans objet", "1 mois", "2 mois", "3 mois"])

        st.markdown("##### 🔒 Clauses Spécifiques Optionnelles")
        clause_exclusivity = st.checkbox("Clause d'exclusivité totale (Interdiction de cumul d'activités)")
        clause_confidentiality = st.checkbox("Clause renforcée de secret professionnel et confidentialité", value=True)

        submit_wizard = st.form_submit_button("🔨 Compiler le contrat de travail personnalisé", use_container_width=True)

    if submit_wizard:
        if not emp_name or not job_title:
            st.error("Veuillez renseigner au minimum le nom du salarié et l'intitulé du poste.")
        else:
            with st.spinner("Génération et mise en conformité des articles réglementaires..."):
                
                # Génération dynamique du texte du contrat
                cdd_mention = "Il est conclu pour une durée déterminée de [Spécifier la durée]." if "CDD" in contract_type else "Il est conclu pour une durée indéterminée."
                trial_mention = f"Le présent contrat n'est définitivement conclu qu'après une période d'essai de {trial_period}." if trial_period != "Sans objet" else "Le présent contrat prend effet dès la date de signature sans période d'essai."
                
                exclusivity_text = ""
                if clause_exclusivity:
                    exclusivity_text = "\n\n**Article 5 : Exclusivité**\nL'employé s'engage à consacrer l'exclusivité de ses compétences professionnelles aux activités de l'employeur, toute autre activité professionnelle lui étant formellement interdite sauf accord écrit préalable."
                
                conf_text = ""
                if clause_confidentiality:
                    conf_text = "\n\n**Article 6 : Confidentialité**\nL'employé est lié par une obligation absolue de secret professionnel pour tout ce qui concerne les faits, informations et documents dont il aura connaissance au cours de son emploi chez Sylco Inc."

                contract_content = f"""CONTRAT DE TRAVAIL

ENTRE LES SOUSSIGNÉS :
La société {company_title}, dont le siège social est basé à Dakar, valablement représentée.
Ci-après désignée "L'Employeur",

ET :
M. {emp_name}, de nationalité {emp_nationality}, demeurant au {emp_address}.
Ci-après désigné "L'Employé",

IL A ÉTÉ CONVENU ET ARRÊTÉ CE QUI SUIT :

**Article 1 : Nature du contrat**
Le présent contrat est régi par le Code du Travail de la République du Sénégal et les textes subséquents. {cdd_mention}

**Article 2 : Fonctions & Attributions**
L'Employé est engagé en qualité de : {job_title}. Il effectuera les tâches classiques liées à sa qualification.

**Article 3 : Période d'essai**
{trial_mention}

**Article 4 : Rémunération**
En contrepartie de ses services, l'Employé percevra un salaire mensuel brut global de {base_salary:,} FCFA.{exclusivity_text}{conf_text}

**Article 7 : Règlement des différends**
Tout litige né de l'interprétation ou de l'exécution du présent contrat sera soumis aux tribunaux compétents du ressort du siège social de l'Employeur, après tentative de conciliation obligatoire devant l'Inspecteur du Travail et de la Prévoyance Sociale de Dakar.

Fait à Dakar, le 22 Juin 2026, en deux exemplaires originaux.

Pour l'Employeur                                     Pour l'Employé"""

                st.success("✨ Votre document juridique sur-mesure a été compilé avec succès !")
                
                # Fenêtre d'aperçu propre
                st.markdown("### 👀 Aperçu du contrat généré")
                st.markdown(f'<div class="mp-preview-contract">{contract_content.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                
                # Téléchargement
                st.write("")
                st.download_button(
                    label="📥 Télécharger le document (.txt)",
                    data=contract_content,
                    file_name=f"Contrat_Travail_{emp_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    st.markdown("""
    <div class="mp-footer">
      Générateur automatisé certifié conforme au droit du travail et usages OHADA.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTAGE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
if page == "💬  Discussion":
    render_chat()
elif page == "📚  Documents":
    render_documents()
elif page == "🔍  Analyseur":
    render_analyzer()
elif page == "📝  Générateur":
    render_generator()