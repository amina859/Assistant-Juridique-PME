import streamlit as st
import requests
import random

st.set_page_config(
    page_title="MyPME · Conseiller Juridique",
    page_icon="⚖",
    layout="centered",
)

# ── Style global ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

/* Reset */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

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
.mp-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3DD68C;
}

/* ── Corpus badges ── */
.mp-corpus {
    background: #0F2A4F;
    border-radius: 0;
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
    max-width: 88%;
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
    margin-bottom: 4px;
}
.mp-row-user {
    display: flex;
    align-items: flex-start;
    flex-direction: row-reverse;
    gap: 10px;
    margin-bottom: 4px;
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
</style>
""", unsafe_allow_html=True)


# ── En-tête ───────────────────────────────────────────────────────────────────
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

# ── Actions rapides ────────────────────────────────────────────────────────────
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

# ── Historique ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bonjour ! Je suis votre conseiller juridique dédié aux PME sénégalaises.\n\nJe maîtrise le **droit OHADA**, le **Code du travail sénégalais** et la **fiscalité UEMOA**. Posez votre question ou choisissez une action rapide ci-dessus.",
            "confidence": 99,
            "citations": [],
        }
    ]

def render_citations(citations):
    """Render citation chips as HTML."""
    if not citations:
        return ""
    chips = ""
    for cite in citations:
        cls = "mp-cite-chip-ohada" if "OHADA" in cite or "Acte" in cite else ""
        chips += f'<span class="mp-cite-chip {cls}">📎 {cite}</span>'
    return f'<div style="margin-top:8px;">{chips}</div>'

def render_confidence(score):
    """Render a confidence bar."""
    color = "#3DD68C" if score >= 85 else "#C8921A" if score >= 65 else "#E24B4A"
    return f"""
    <div class="mp-conf">
      <span>🛡 Fiabilité :</span>
      <span class="mp-conf-bar"><span class="mp-conf-fill" style="width:{score}%; background:{color};"></span></span>
      <span style="color:{color}; font-weight:500;">{score} %</span>
    </div>
    """

# Afficher les messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"""
        <div class="mp-row-ai">
          <div class="mp-av mp-av-ai">⚖</div>
          <div>
            <div class="mp-msg-ai">{msg["content"].replace(chr(10), "<br>").replace("**", "<strong>").replace("**", "</strong>")}</div>
            {render_citations(msg.get("citations", []))}
            {render_confidence(msg.get("confidence", 90))}
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="mp-row-user">
          <div class="mp-av mp-av-user">Vous</div>
          <div class="mp-msg-user">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill", "")
question = st.chat_input("Posez votre question juridique…")

# Action rapide ou saisie manuelle
final_question = prefill or question

if final_question:
    # Afficher message utilisateur
    st.markdown(f"""
    <div class="mp-row-user">
      <div class="mp-av mp-av-user">Vous</div>
      <div class="mp-msg-user">{final_question}</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": final_question})

    # Appel API
    with st.spinner("Analyse juridique en cours…"):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
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

    # Afficher réponse IA
    st.markdown(f"""
    <div class="mp-row-ai">
      <div class="mp-av mp-av-ai">⚖</div>
      <div>
        <div class="mp-msg-ai">{response_text.replace(chr(10), "<br>")}</div>
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mp-footer">
  🛡 Sources officielles consolidées 2025 &nbsp;·&nbsp;
  Consultez toujours un avocat pour des décisions critiques
</div>
""", unsafe_allow_html=True)