import streamlit as st
import pandas as pd
import random
import os
import shutil

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Stravinsky Masterclass", layout="centered")

# --- LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ Accesso Studenti")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Accedi"):
        if user == "admin" and password == "stravinsky2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenziali errate")
    st.stop()

# --- CARICAMENTO DATI ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WoBGPp_rsK626pbppGmKl_b7Nx84dtHuuoCdqIO0ilM/gviz/tq?tqx=out:csv"

@st.cache_data
def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame({"Domande": ["Errore nel caricamento del file Excel."]})

df = load_data()
domande_list = df.iloc[:, 0].dropna().tolist()

# --- INTERFACCIA ---
st.title("🎼 Stravinsky Masterclass")

if 'indice' not in st.session_state:
    st.session_state.indice = 0

# Box Domanda
st.info(f"**DOMANDA:** {domande_list[st.session_state.indice]}")

# Pulsanti Azione
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Prossima Domanda"):
        st.session_state.indice = random.randint(0, len(domande_list)-1)
        st.rerun()

with col2:
    query = f"Igor Stravinsky {domande_list[st.session_state.indice]}"
    link_google = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    # Metodo sicuro per il link
    st.link_button("🔍 Approfondisci Online", link_google, type="primary")

st.divider()

# --- GESTIONE EVENTI (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Gestione Evento")
    nome_ev = st.text_input("Nome Sessione", value="Esercitazione_Milano")
    
    if st.button("📁 Crea Cartelle"):
        os.makedirs(f"eventi/{nome_ev}/reminders", exist_ok=True)
        os.makedirs(f"eventi/{nome_ev}/mask", exist_ok=True)
        st.success(f"Cartelle per {nome_ev} create!")

    if st.button("🗑️ Elimina Evento", help="Cancella tutti i file relativi"):
        path = f"eventi/{nome_ev}"
        if os.path.exists(path):
            shutil.rmtree(path)
            st.warning(f"Evento {nome_ev} eliminato con successo.")
        else:
            st.error("Nessun evento trovato con questo nome.")
