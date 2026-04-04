import streamlit as st
from datetime import datetime

# 1. TRADUCCIONS (UI multilingüe -> Dades en Castellà)
traduccions = {
    "Valencià": {
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "botó_guardar": "💾 GUARDAR DADES",
        "tipus_campo": "Campo",
        "tipus_recollit": "Recogido"
    },
    "Castellano": {
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "botó_guardar": "💾 GUARDAR DATOS",
        "tipus_campo": "Campo",
        "tipus_recollit": "Recogido"
    },
    "Română": {
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "botó_guardar": "💾 SALVEAZĂ DATELE",
        "tipus_campo": "Campo", # Es guarda en Castellà
        "tipus_recollit": "Recogido" # Es guarda en Castellà
    }
}

# 2. Dades de finques
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title("🟣 Control Maracuia - Beniarjó")

opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"]])

if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])
    
    with st.form("form_entrada"):
        kg = st.number_input("Kg:", min_value=0.0)
        cajas = st.number_input("Capses / Cajas:", min_value=0)
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            # GENEREM L'ID DE LOT (Traçabilitat)
            id_lote = f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}"
            
            # DADES QUE ANIRAN AL GOOGLE SHEETS (Sempre en Castellà)
            dades_a_guardar = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel,
                "Parcela": parcela_sel,
                "Tipo": "Campo", # Valor fix en Castellà
                "Kg": kg,
                "Cajas": cajas,
                "ID_Lote": id_lote,
                "Ref_Original": "" # Buit perquè és una entrada nova
            }
            st.success(f"Dades preparades per al registre (Castellano): {dades_a_guardar['Tipo']}")
            st.write(f"ID Generat: {id_lote}")

elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    st.write("Aquí l'App buscarà els 'ID_Lote' que tenen tipus 'Campo' per a crear una nova fila de tipus 'Recogido'.")
