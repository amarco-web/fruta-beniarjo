import streamlit as st

# 1. Diccionari de finques i parcel·les exactes
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"],
    "Sagra": ["Sagra"]
}

st.set_page_config(page_title="Fruta Beniarjó", layout="centered")
st.title("🍎 Control de Fruta - Mirna")

menu = st.sidebar.radio("Menú:", ["Registrar Entrada", "Estat Almacén"])

if menu == "Registrar Entrada":
    st.header("📝 Nova Entrada de Camp")
    
    with st.form("form_entrada"):
        # PRIMER DESPLEGABLE: FINCA
        finca_sel = st.selectbox("Tria la Finca:", list(dades_fincas.keys()))
        
        # SEGON DESPLEGABLE: PARCEL·LA (Depèn de la Finca triada)
        parcela_sel = st.selectbox("Tria la Parcel·la:", dades_fincas[finca_sel])
        
        col1, col2 = st.columns(2)
        with col1:
            kg = st.number_input("Kilos (Kg):", min_value=0.0, step=0.1)
        with col2:
            cajas = st.number_input("Capses:", min_value=0, step=1)
            
        submit = st.form_submit_button("💾 GUARDAR DADES ENTRADA")
        
        if submit:
            st.success(f"✅ REGISTRAT: {kg}kg en {finca_sel} ({parcela_sel})")
            st.balloons()
else:
    st.info("Estat del magatzem pròximament...")
