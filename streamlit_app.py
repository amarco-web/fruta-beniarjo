import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. DICCIONARI DE TRADUCCIONS (Interfície multilingüe -> Dades en Castellà)
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "tria_finca": "Tria la Finca:",
        "tria_parcela": "Tria la Parcel·la:",
        "tria_lot": "Tria el Lot per a bolcar:",
        "kg_disponibles": "Kg disponibles en cambra:",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "botó_volcar": "🚜 REGISTRAR VOLCAT",
        "exit": "✅ Registrat correctament!",
        "no_lots": "No hi ha lots pendents en la cambra."
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "tria_finca": "Selecciona la Finca:",
        "tria_parcela": "Selecciona la Parcela:",
        "tria_lot": "Elige el Lote para volcar:",
        "kg_disponibles": "Kg disponibles en cámara:",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "botó_volcar": "🚜 REGISTRAR VOLCADO",
        "exit": "✅ ¡Registrado correctamente!",
        "no_lots": "No hay lotes pendientes en la cámara."
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "tria_finca": "Selectați Ferma:",
        "tria_parcela": "Selectați Parcela:",
        "tria_lot": "Alegeți lotul de descărcat:",
        "kg_disponibles": "Kg disponibile în depozit:",
        "botó_guardar": "💾 SALVEAZĂ INTRAREA",
        "botó_volcar": "🚜 ÎNREGISTREAZĂ DESCĂRCAREA",
        "exit": "✅ Înregistrat cu succes!",
        "no_lots": "Nu există loturi în depozit."
    }
}

# 2. CONFIGURACIÓ DE FINQUES
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

# 3. CONFIGURACIÓ PÀGINA
st.set_page_config(page_title="Maracuia Beniarjó", page_icon="🟣", layout="centered")

# 4. CONNEXIÓ GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. SELECTOR D'IDIOMA (Barra lateral)
st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
        else:
            st.warning("No hi ha lots pendents en la cambra.")
    else:
        st.error("La base de dades està buida.")
