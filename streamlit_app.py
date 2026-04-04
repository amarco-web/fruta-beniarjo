import streamlit as st

# 1. Diccionari de traduccions
traduccions = {
    "Valencià": {
        "titol": "🍎 Control de Fruita - Mirna",
        "menu_entrada": "Registrar Entrada",
        "menu_estat": "Estat Magatzem",
        "tria_finca": "Tria la Finca:",
        "tria_parcela": "Tria la Parcel·la:",
        "kilos": "Kilos (Kg):",
        "capses": "Capses:",
        "tipus": "Tipus de Fruita:",
        "botó_guardar": "💾 GUARDAR DADES",
        "exit": "✅ REGISTRAT CORRECTAMENT",
        "pendent": "Pròximament veuràs aquí el llistat pendent."
    },
    "Castellano": {
        "titol": "🍎 Control de Fruta - Mirna",
        "menu_entrada": "Registrar Entrada",
        "menu_estat": "Estado Almacén",
        "tria_finca": "Selecciona la Finca:",
        "tria_parcela": "Selecciona la Parcela:",
        "kilos": "Kilos (Kg):",
        "capses": "Cajas:",
        "tipus": "Tipo de Fruta:",
        "botó_guardar": "💾 GUARDAR DATOS",
        "exit": "✅ REGISTRADO CORRECTAMENTE",
        "pendent": "Próximamente verás aquí el listado pendiente."
    },
    "Română": {
        "titol": "🍎 Controlul Fructelor - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_estat": "Stare Depozit",
        "tria_finca": "Selectați Ferma (Finca):",
        "tria_parcela": "Selectați Parcela:",
        "kilos": "Kilograme (Kg):",
        "capses": "Lăzi (Cajas):",
        "tipus": "Tipul de fructe:",
        "botó_guardar": "💾 SALVEAZĂ DATELE",
        "exit": "✅ ÎNREGISTRAT CU SUCCES",
        "pendent": "În curând veți vedea lista aici."
    }
}

# 2. Dades de finques (Noms propis, no canvien)
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"],
    "Sagra": ["Sagra"]
}

st.set_page_config(page_title="Fruta Beniarjó", layout="centered")

# SELECTOR D'IDIOMA A LA BARRA LATERAL
st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])

# Assignem les paraules de l'idioma triat
t = traduccions[idioma]

st.title(t["titol"])

menu = st.sidebar.radio(t["menu_entrada"], [t["menu_entrada"], t["menu_estat"]])

if menu == t["menu_entrada"]:
    st.header(f"📝 {t['menu_entrada']}")
    
    finca_sel = st.selectbox(t["tria_finca"], list(dades_fincas.keys()))
    llista_parcelas = dades_fincas[finca_sel]
    parcela_sel = st.selectbox(t["tria_parcela"], llista_parcelas)
    
    with st.form("dades_numeriques"):
        col1, col2 = st.columns(2)
        with col1:
            kg = st.number_input(t["kilos"], min_value=0.0, step=0.1)
        with col2:
            cajas = st.number_input(t["capses"], min_value=0, step=1)
            
        tipus = st.selectbox(t["tipus"], ["Campo", "Recogido", "Industria"])
        
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            st.success(f"{t['exit']}: {kg}kg - {finca_sel} ({parcela_sel})")
            st.balloons()

elif menu == t["menu_estat"]:
    st.header(f"❄️ {t['menu_estat']}")
    st.info(t["pendent"])
