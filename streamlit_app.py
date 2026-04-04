import streamlit as st
import pandas as pd

# Configuració bàsica
st.set_page_config(page_title="Fruta Beniarjó", layout="centered")

st.title("🍎 Control de Fruta - Mirna")

# Menú de l'App
menu = st.sidebar.radio("Menú:", ["Registrar Entrada", "Estat Almacén", "Configuració"])

if menu == "Registrar Entrada":
    st.header("📝 Nova Entrada de Camp")
    
    with st.form("form_entrada"):
        finca = st.selectbox("Finca:", ["Castelló", "Cooperativa", "Tarraso", "Marapego", "Sagra"])
        parcela = st.text_input("Parcel·la (ex: Eloy, Santi...)")
        kg = st.number_input("Kilos (Kg):", min_value=0.0, step=0.1)
        cajas = st.number_input("Capses:", min_value=0, step=1)
        tipus = st.selectbox("Tipus:", ["Campo", "Recogido", "Industria"])
        
        submit = st.form_submit_button("💾 GUARDAR DADES")
        
        if submit:
            st.success(f"✅ Guardat: {kg}kg de {finca} ({parcela})")
            st.balloons()

elif menu == "Estat Almacén":
    st.header("❄️ Fruita en Cambra")
    st.info("Pròximament veuràs aquí el llistat de fruita pendent de confeccionar.")

else:
    st.header("⚙️ Configuració")
    st.write("Aquí connectarem el teu Google Sheets més endavant.")
