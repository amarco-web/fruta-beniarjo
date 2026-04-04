import streamlit as st
import pandas as pd

# 1. Diccionari de traduccions actualitzat a MARACUIA
traduccions = {
    "Valencià": {
        "titol": "🟣 Control de Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "menu_estat": "Estat Magatzem",
        "tria_finca": "Tria la Finca:",
        "tria_parcela": "Tria la Parcel·la:",
        "tria_lot": "Tria el Lot per a bolcar:",
        "kilos": "Kilos (Kg):",
        "capses": "Capses:",
        "tipus": "Tipus de Maracuia:",
        "botó_guardar": "💾 GUARDAR DADES",
        "botó_volcar": "🚜 REGISTRAR VOLCAT",
        "exit": "✅ REGISTRAT CORRECTAMENT",
        "pendent": "Aquí veuràs la maracuia que encara està en la cambra."
    },
    "Castellano": {
        "titol": "🟣 Control de Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "menu_estat": "Estado Almacén",
        "tria_finca": "Selecciona la Finca:",
        "tria_parcela": "Selecciona la Parcela:",
        "tria_lot": "Elige el Lote para volcar:",
        "kilos": "Kilos (Kg):",
        "capses": "Cajas:",
        "tipus": "Tipo de Maracuyá:",
        "botó_guardar": "💾 GUARDAR DATOS",
        "botó_volcar": "🚜 REGISTRAR VOLCADO",
        "exit": "✅ REGISTRADO CORRECTAMENTE",
        "pendent": "Aquí verás el maracuyá que aún está en la cámara."
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "menu_estat": "Stare Depozit",
        "tria_finca": "Selectați Ferma (Finca):",
        "tria_parcela": "Selectați Parcela:",
        "tria_lot": "Alegeți lotul de descărcat:",
        "kilos": "Kilograme (Kg):",
        "capses": "Lăzi (Cajas):",
        "tipus": "Tipul de maracuja:",
        "botó_guardar": "💾 SALVEAZĂ DATELE",
        "botó_volcar": "🚜 ÎNREGISTREAZĂ DESCĂRCAREA",
        "exit": "✅ ÎNREGISTRAT CU SUCCES",
        "pendent": "Aici veți vedea maracuja care este încă în depozit."
    }
}

dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"],
    "Sagra": ["Sagra"]
}

# Configuració de la pàgina amb icona morada
st.set_page_config(page_title="Maracuia Beniarjó", page_icon="🟣", layout="centered")

st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])

opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"], t["menu_estat"]])

if opcio == t["menu_entrada"]:
    st.header(f"📝 {t['menu_entrada']}")
    finca_sel = st.selectbox(t["tria_finca"], list(dades_fincas.keys()))
    llista_parcelas = dades_fincas[finca_sel]
    parcela_sel = st.selectbox(t["tria_parcela"], llista_parcelas)
    
    with st.form("form_entrada"):
        col1, col2 = st.columns(2)
        with col1:
            kg = st.number_input(t["kilos"], min_value=0.0, step=0.1)
        with col2:
            cajas = st.number_input(t["capses"], min_value=0, step=1)
        submit = st.form_submit_button(t["botó_guardar"])
        if submit:
            st.success(f"{t['exit']}: {kg}kg")

elif opcio == t["menu_volcat"]:
    st.header(f"🚜 {t['menu_volcat']}")
    lots_pendents = ["2025-01-15 | Castelló | Sagra", "2025-01-16 | Cooperativa | Eloy"]
    lot_triat = st.selectbox(t["tria_lot"], lots_pendents)
    
    with st.form("form_volcat"):
        kg_volcats = st.number_input(f"{t['kilos']} a bolcar:", min_value=0.0, step=0.1)
        submit_volcat = st.form_submit_button(t["botó_volcar"])
        if submit_volcat:
            st.success(f"✅ {t['exit']}: {kg_volcats}kg")

elif opcio == t["menu_estat"]:
    st.header(f"❄️ {t['menu_estat']}")
    st.info(t["pendent"])
