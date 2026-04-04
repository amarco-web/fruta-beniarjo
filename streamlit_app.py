import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. DICCIONARI DE TRADUCCIONS
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
        "exit": "✅ Registrat correctament!"
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
        "exit": "✅ ¡Registrado correctamente!"
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
        "exit": "✅ Înregistrat cu succes!"
    }
}

dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.set_page_config(page_title="Maracuia Beniarjó", page_icon="🟣")

# CONNEXIÓ (Amb la ID del full directament)
conn = st.connection("gsheets", type=GSheetsConnection)

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"]])

# LLEGIR DADES
try:
    # Usem la ID que surt a la teva URL
    df_actual = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE", worksheet="Full 1", ttl=0)
    df_actual = df_actual.dropna(how="all")
except Exception as e:
    st.error(f"Error: {e}")
    df_actual = pd.DataFrame(columns=["Fecha", "Finca", "Parcela", "Tipo", "Kg", "Cajas", "ID_Lote", "Ref_Original"])

if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox(t["tria_finca"], list(dades_fincas.keys()))
    parcela_sel = st.selectbox(t["tria_parcela"], dades_fincas[finca_sel])
    
    with st.form("form_entrada", clear_on_submit=True):
        col1, col2 = st.columns(2)
        kg = col1.number_input("Kg:", min_value=0.0, step=0.1)
        cajas = col2.number_input("Cajas:", min_value=0)
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            id_lote = f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}-{parcela_sel[:3].upper()}"
            nova_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel,
                "Parcela": parcela_sel,
                "Tipo": "Campo",
                "Kg": kg,
                "Cajas": cajas,
                "ID_Lote": id_lote,
                "Ref_Original": ""
            }])
            df_final = pd.concat([df_actual, nova_fila], ignore_index=True)
            # GUARDAR
            conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE", worksheet="Full 1", data=df_final)
            st.success(t["exit"])
            st.cache_data.clear()

elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_actual.empty:
        campo = df_actual[df_actual['Tipo'] == 'Campo'].groupby('ID_Lote')['Kg'].sum()
        recollit = df_actual[df_actual['Tipo'] == 'Recogido'].groupby('Ref_Original')['Kg'].sum()
        stock = campo.subtract(recollit, fill_value=0)
        lots_amb_stock = stock[stock > 0.1]
        
        if not lots_amb_stock.empty:
            lot_triat = st.selectbox(t["tria_lot"], lots_amb_stock.index)
            st.metric(t["kg_disponibles"], f"{round(lots_amb_stock[lot_triat], 2)} Kg")
            
            with st.form("form_volcat", clear_on_submit=True):
                kg_volcat = st.number_input("Kg a bolcar:", min_value=0.0, max_value=float(lots_amb_stock[lot_triat]))
                submit_v = st.form_submit_button(t["botó_volcar"])
                if submit_v:
                    orig = df_actual[df_actual['ID_Lote'] == lot_triat].iloc[0]
                    fila_v = pd.DataFrame([{
                        "Fecha": datetime.now().strftime("%d/%m/%Y"),
                        "Finca": orig['Finca'],
                        "Parcela": orig['Parcela'],
                        "Tipo": "Recogido",
                        "Kg": kg_volcat,
                        "Cajas": 0,
                        "ID_Lote": f"VOL-{datetime.now().strftime('%H%M%S')}",
                        "Ref_Original": lot_triat
                    }])
                    df_final = pd.concat([df_actual, fila_v], ignore_index=True)
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE", worksheet="Full 1", data=df_final)
                    st.success(t["exit"])
                    st.cache_data.clear()
        else:
            st.warning("No hi ha lots pendents.")
