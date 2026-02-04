import streamlit as st
import pandas as pd
import random
import os
import shutil

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Stravinsky Masterclass v1.5", layout="centered")

# --- LOGO E TITOLO ---
# Link al logo del Conservatorio di Milano (URL pubblico)
LOGO_URL = "https://www.consmilano.it/wp-content/uploads/2021/03/logo-conservatorio-milano.png"

st.image("logo.png", width=180)
st.title("🎼 Stravinsky Masterclass")
st.subheader("Conservatorio di Musica G. Verdi di Milano")

# --- LINK DATABASE ---
SHEET_READ_URL = "https://docs.google.com/spreadsheets/d/1UugrePwGoo_KlOxsv-7hvg2YzYtLuQy4bV3rCFCjxSc/export?format=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1UugrePwGoo_KlOxsv-7hvg2YzYtLuQy4bV3rCFCjxSc/edit?usp=sharing"

# --- GESTIONE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Accedi"):
        if user == "admin" and password == "stravinsky2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenziali non valide")
    st.stop()

# --- CARICAMENTO DATI ---
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_READ_URL)
        return df.dropna(subset=[df.columns[0]])
    except:
        return pd.DataFrame({"Domanda": ["Errore caricamento"], "Risposta": ["Errore"]})

df = load_data()
domande = df.iloc[:, 0].tolist()
risposte = df.iloc[:, 1].tolist() if len(df.columns) > 1 else ["N/A"] * len(domande)

# --- INTERFACCIA PRINCIPALE ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0

st.info(f"**DOMANDA:** {domande[st.session_state.indice]}")
risposta_utente = st.text_input("La tua risposta:", key="ans_input")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Verifica"):
        corretta = str(risposte[st.session_state.indice]).strip().lower()
        if risposta_utente.strip().lower() in corretta and len(risposta_utente) > 2:
            st.success("ECCELLENTE! 🎉")
            st.balloons()
        else:
            st.error(f"NON ESATTO. Risposta: {risposte[st.session_state.indice]}")

with col2:
    if st.button("🔄 Prossima"):
        st.session_state.indice = random.randint(0, len(domande)-1)
        st.rerun()

with col3:
    st.link_button("📊 Apri Excel", SHEET_EDIT_URL)

# --- SIDEBAR: ISTRUZIONI E GESTIONE ---
with st.sidebar:
    st.header("📖 Istruzioni Rapide")
    st.markdown("""
    1. Effettua il **Login**.
    2. Rispondi alla domanda e clicca **Verifica**.
    3. Usa **Prossima** per cambiare domanda.
    4. Usa la sidebar per **creare cartelle** evento (v1.2).
    """)
    
    st.divider()
    st.header("✍️ Collabora")
    st.link_button("➕ Aggiungi Domande", SHEET_EDIT_URL)
    
    st.divider()
    st.header("⚙️ Gestione Evento")
    nome_ev = st.text_input("ID Sessione", "Esercitazione_Milano")
    if st.button("📁 Crea Cartelle"):
        os.makedirs(f"eventi/{nome_ev}/reminders", exist_ok=True)
        os.makedirs(f"eventi/{nome_ev}/mask", exist_ok=True)
        st.success("Cartelle create!")
    if st.button("🗑️ Elimina Evento", type="primary"):
        path = f"eventi/{nome_ev}"
        if os.path.exists(path):
            shutil.rmtree(path)
            st.warning("File eliminati.")

