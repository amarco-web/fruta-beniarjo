import streamlit as st

# 1. Diccionari de finques i parcel·les exactes (Dades de Beniarjó)
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"],
    "Sagra": ["Sagra"]
}

# Configuració de la pàgina
st.set_page_config(page_title="Control Fruita Beniarjó", layout="centered")

st.title("🍎 Control de Fruita - Mirna")

menu = st.sidebar.radio("Menú:", ["Registrar Entrada", "Estat Almacén"])

if menu == "Registrar Entrada":
    st.header("📝 Nova Entrada de Camp")
    
    # ⚠️ LES SELECCIONS FORA DEL FORM PERQUÈ SIGUEN DINÀMIQUES
    finca_sel = st.selectbox("Tria la Finca:", list(dades_fincas.keys()))
    
    # Ara la parcel·la canviarà AUTOMÀTICAMENT quan canviïs la finca
    llista_parcelas = dades_fincas[finca_sel]
    parcela_sel = st.selectbox("Tria la Parcel·la:", llista_parcelas)
    
    # Formulari només per a les dades numèriques i el botó de guardar
    with st.form("dades_numeriques"):
        col1, col2 = st.columns(2)
        with col1:
            kg = st.number_input("Kilos (Kg):", min_value=0.0, step=0.1)
        with col2:
            cajas = st.number_input("Capses:", min_value=0, step=1)
            
        tipus = st.selectbox("Tipus de Fruita:", ["Campo", "Recogido", "Industria"])
        
        submit = st.form_submit_button("💾 GUARDAR ENTRADA")
        
        if submit:
            # Aquí confirmem que s'ha guardat (de moment només visualment)
            st.success(f"✅ REGISTRAT: {kg}kg de {finca_sel} ({parcela_sel})")
            st.balloons()

elif menu == "Estat Almacén":
    st.header("❄️ Fruita en Cambra")
    st.info("Pròximament veuràs aquí el llistat pendent.")
