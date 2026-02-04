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
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    domande_list = df.iloc[:, 0].dropna().tolist()
except Exception as e:
    st.error(f"Errore nel caricamento dell'Excel: {e}")
    domande_list = ["File non trovato o link non valido."]

# --- INTERFACCIA ---
st.title("🎼 Stravinsky Masterclass v1.2")

if 'indice' not in st.session_state:
    st.session_state.indice = 0

# Box Domanda
st.info(domande_list[st.session_state.indice])

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 Prossima"):
        st.session_state.indice = random.randint(0, len(domande_list)-1)
        st.rerun()

with c2:
    query = f"Igor Stravinsky {domande_list[st.session_state.indice]}"
    link = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; height:3em; background-color:gold; border-radius:10px;">🔍 Approfondisci</button></a>', unsafe_allow_input=True)

# Gestione Cartelle (Tua richiesta specifica)
with st.sidebar:
    st.header("Gestione Evento")
    nome_ev = st.text_input("ID Evento", "Sessione_1")
    if st.button("Crea Cartelle"):
        os.makedirs(f"eventi/{nome_ev}/reminders", exist_ok=True)
        os.makedirs(f"eventi/{nome_ev}/mask", exist_ok=True)
        st.success("Cartelle create!")
    if st.button("Elimina Tutto"):
        if os.path.exists(f"eventi/{nome_ev}"):
            shutil.rmtree(f"eventi/{nome_ev}")
            st.warning("Evento e file eliminati.")
