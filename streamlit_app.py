import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. LA TEUA URL DE GOOGLE APPS SCRIPT
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "tria_finca": "Tria la Finca:",
        "tria_parcela": "Tria la Parcel·la:",
        "kilos": "Kilos (Kg):",
        "capses": "Capses:",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ Dades enviades correctament al full de càlcul!"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "tria_finca": "Selecciona la Finca:",
        "tria_parcela": "Selecciona la Parcela:",
        "kilos": "Kilos (Kg):",
        "capses": "Cajas:",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ ¡Datos enviados correctamente a la hoja de cálculo!"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "tria_finca": "Selectați Ferma:",
        "tria_parcela": "Selectați Parcela:",
        "kilos": "Kilograme (Kg):",
        "capses": "Lăzi (Cajas):",
        "botó_guardar": "💾 SALVEAZĂ INTRAREA",
        "exit": "✅ Date trimise cu succes în tabelul Google!"
    }
}

dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.set_page_config(page_title="Maracuia Beniarjó", page_icon="🟣")

# SELECTOR D'IDIOMA
st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"]])

if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox(t["tria_finca"], list(dades_fincas.keys()))
    parcela_sel = st.selectbox(t["tria_parcela"], dades_fincas[finca_sel])
    
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        kg = col1.number_input(t["kilos"], min_value=0.0, step=0.1)
        cajas = col2.number_input(t["capses"], min_value=0)
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            # Preparem les dades per enviar
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel,
                "Parcela": parcela_sel,
                "Tipo": "Campo",
                "Kg": str(kg).replace('.', ','),
                "Cajas": int(cajas),
                "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}",
                "Ref_Original": ""
            }
            
            try:
                response = requests.post(URL_APPS_SCRIPT, json=dades)
                if "Success" in response.text:
                    st.success(t["exit"])
                    st.balloons()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error de connexió: {e}")
else:
    st.info("La secció de Volcat estarà activa quan les entrades funcionen.")