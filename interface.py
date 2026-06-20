import streamlit as st
import requests

st.set_page_config(
    page_title="MyPME",
    page_icon="⚖",
    layout="centered"
)

# ── Style personnalisé ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500&display=swap');

body { font-family: 'Inter', sans-serif; }

.titre {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #0F1F3D;
    text-align: center;
    margin-bottom: 0;
}
.sous-titre {
    text-align: center;
    color: #7A8296;
    font-size: 0.9rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── En-tête ──
st.markdown('<div class="titre">⚖ MyPME</div>', unsafe_allow_html=True)
st.markdown('<div class="sous-titre">Assistant juridique · Droit OHADA · Droit du travail sénégalais</div>', unsafe_allow_html=True)
st.divider()

# ── Historique ──
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant juridique spécialisé en **droit OHADA** et **droit du travail sénégalais**. Posez-moi vos questions."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ──
if question := st.chat_input("Posez votre question juridique…"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours…"):
            try:
                res = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": question}
                )
                response = res.json()["response"]
            except:
                response = "Erreur : impossible de joindre le serveur."
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})