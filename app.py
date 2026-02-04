import streamlit as st
import pandas as pd
import random
import os
import shutil
import webbrowser

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Stravinsky Masterclass v1.2", layout="centered")

# --- ESTETICA CUSTOM (MILANO STYLE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .question-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #d4af37; /* Oro Blackwell */
        margin: 20px 0;
        font-family: 'Georgia', serif;
        font-size: 1.2rem;
    }
    .stButton>button { border-radius: 12px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_input=True)

# --- FUNZIONI DI SERVIZIO ---
def crea_cartelle_evento(nome_evento):
    base = f"eventi/{nome_evento}"
    os.makedirs(f"{base}/reminders", exist_ok=True)
    os.makedirs(f"{base}/mask", exist_ok=True)
    return base

def elimina_evento(nome_evento):
    path = f"eventi/{nome_evento}"
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False

# --- GESTIONE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏛️ Stravinsky Masterclass")
    st.subheader("Area Riservata Studenti")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Accedi"):
        if user == "admin" and password == "stravinsky2026": # Credenziali demo
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenziali non valide")
    st.stop()

# --- CARICAMENTO DATI (DAL TUO EXCEL) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WoBGPp_rsK626pbppGmKl_b7Nx84dtHuuoCdqIO0ilM/gviz/tq?tqx=out:csv"

@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()
domande_list = df.iloc[:, 0].dropna().tolist()

# --- INTERFACCIA PRINCIPALE ---
st.title("🎼 Dashboard Esercitazioni")
st.write(f"Studente: **{os.getlogin() if hasattr(os, 'getlogin') else 'Studente Milano'}**")

# Gestione Evento nella Sidebar
with st.sidebar:
    st.header("⚙️ Gestione Sessione")
    nome_ev = st.text_input("ID Evento", "Esercitazione_Stravinsky")
    if st.button("📁 Crea Cartelle Evento"):
        path = crea_cartelle_evento(nome_ev)
        st.success(f"Struttura creata!")
    
    if st.button("🗑️ Chiudi ed Elimina Evento", type="primary"):
        if elimina_evento(nome_ev):
            st.warning("Tutti i file correlati sono stati eliminati.")

# Logica Quiz
if 'indice' not in st.session_state:
    st.session_state.indice = 0

st.markdown(f'<div class="question-box">{domande_list[st.session_state.indice]}</div>', unsafe_allow_input=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 Prossima Domanda"):
        st.session_state.indice = random.randint(0, len(domande_list)-1)
        st.rerun()

with c2:
    query = f"Igor Stravinsky {domande_list[st.session_state.indice]}"
    link = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; border-radius:12px; height:3em; background-color:#d4af37; color:black; border:none; font-weight:bold; cursor:pointer;">🔍 Approfondisci Online</button></a>', unsafe_allow_input=True)