import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URL DE L'APPS SCRIPT (Versió 5)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyryYeSXGhmhCsmve6wNv7yn_mrRKvRaD2bdweUdwmTGzQgWChRBjctkB1mI-hGR2w7/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut de la Pesada", "n_caps": "Nº Caixes", "n_palets": "Nº Palets",
        "afegeix": "➕ AFEGIR PESADA (NETA)", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot:", "dispo": "Disponible:", "n_caps_volcar": "Caixes a bolcar:",
        "botó_volcar": "💾 REGISTRAR VOLCAT", "hui": "📋 Entrades de hui:", "exit": "✅ Registrat!",
        "buit": "No hi ha registres per a la data: ", "recomenat": "Pes suggerit:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto", "n_caps": "Nº Cajas", "n_palets": "Nº Palets",
        "afegeix": "➕ AÑADIR PESADA (NETA)", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote:", "dispo": "Disponible:", "n_caps_volcar": "Cajas a volcar:",
        "botó_volcar": "💾 REGISTRAR VOLCADO", "hui": "📋 Entradas de hoy:", "exit": "✅ ¡Hecho!",
        "buit": "Sin registros para la fecha: ", "recomenat": "Peso sugerido:"
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# ESTIL
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width: 45px; height: 45px; background-color: #5D3FD3; border: 3px solid white;} div[data-testid="stThumbValue"] {font-size: 20px !important; font-weight: bold; color: white; background-color: #5D3FD3; padding: 5px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castel