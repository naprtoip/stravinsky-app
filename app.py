import streamlit as st
import pandas as pd
import random
import os
import shutil

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Stravinsky Masterclass v1.5", layout="centered")

# --- LINK AL TUO DATABASE ---
# Il link che hai fornito trasformato per la lettura automatica e l'editing
SHEET_READ_URL = "https://docs.google.com/spreadsheets/d/1UugrePwGoo_KlOxsv-7hvg2YzYtLuQy4bV3rCFCjxSc/export?format=csv"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1UugrePwGoo_KlOxsv-7hvg2YzYtLuQy4bV3rCFCjxSc/edit?usp=sharing"

# --- GESTIONE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ Stravinsky Masterclass")
    st.subheader("Accesso Studenti - Conservatorio di Milano")
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
        return pd.DataFrame({"Domanda": ["Errore nel caricamento"], "Risposta": ["Verifica il link Excel"]})

df = load_data()
domande = df.iloc[:, 0].tolist()
risposte = df.iloc[:, 1].tolist() if len(df.columns) > 1 else ["N/A"] * len(domande)

# --- INTERFACCIA PRINCIPALE ---
st.title("🎼 Dashboard Esercitazioni")

if 'indice' not in st.session_state:
    st.session_state.indice = 0

# Box Domanda (Stile Blackwell)
st.info(f"**DOMANDA:** {domande[st.session_state.indice]}")
risposta_utente = st.text_input("Digita la tua risposta:", key="ans_input")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Verifica"):
        corretta = str(risposte[st.session_state.indice]).strip().lower()
        utente = risposta_utente.strip().lower()
        if utente in corretta and len(utente) > 2:
            st.success("ECCELLENTE! 🎉")
            st.balloons()
        else:
            st.error(f"NON ESATTO. La risposta era: {risposte[st.session_state.indice]}")

with col2:
    if st.button("🔄 Prossima"):
        st.session_state.indice = random.randint(0, len(domande)-1)
        st.rerun()

with col3:
    st.link_button("📊 Apri Excel", SHEET_EDIT_URL)

st.divider()

# --- SIDEBAR: GESTIONE & CONTRIBUTI ---
with st.sidebar:
    st.header("✍️ Area Collaborativa")
    st.write("Vuoi aggiungere una domanda?")
    st.link_button("➕ Inserisci nel Database", SHEET_EDIT_URL)
    
    st.divider()
    
    st.header("⚙️ Gestione Evento")
    nome_ev = st.text_input("ID Sessione", "Esercitazione_Milano")
    
    if st.button("📁 Crea Cartelle Evento"):
        os.makedirs(f"eventi/{nome_ev}/reminders", exist_ok=True)
        os.makedirs(f"eventi/{nome_ev}/mask", exist_ok=True)
        st.success(f"Cartelle per {nome_ev} pronte!")

    if st.button("🗑️ Chiudi ed Elimina Evento", type="primary"):
        path = f"eventi/{nome_ev}"
        if os.path.exists(path):
            shutil.rmtree(path)
            st.warning("Tutti i file dell'evento sono stati eliminati.")
