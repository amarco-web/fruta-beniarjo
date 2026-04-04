import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. TRADUCCIONS (Interfície multilingüe)
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
        "exit": "✅ Registrat correctament en el Google Sheets"
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
        "exit": "✅ Registrado correctamente en el Google Sheets"
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
        "exit": "✅ Înregistrat cu succes în Google Sheets"
    }
}

# 2. Dades de finques
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.set_page_config(page_title="Maracuia Beniarjó", page_icon="🟣")

# CONNEXIÓ AMB GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# SELECTOR D'IDIOMA
st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"]])

# LLEGIR DADES ACTUALS PER A CÀLCULS D'STOCK
df_actual = conn.read()

# --- SECCIÓ 1: ENTRADA DE CAMP ---
if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox(t["tria_finca"], list(dades_fincas.keys()))
    parcela_sel = st.selectbox(t["tria_parcela"], dades_fincas[finca_sel])
    
    with st.form("form_entrada"):
        col1, col2 = st.columns(2)
        kg = col1.number_input("Kg:", min_value=0.0, step=0.1)
        cajas = col2.number_input("Cajas:", min_value=0)
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            # Generar ID de Lot
            id_lote = f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}-{parcela_sel[:3].upper()}"
            
            # Crear nova fila
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
            
            # Unir dades i guardar
            df_final = pd.concat([df_actual, nova_fila], ignore_index=True)
            conn.update(data=df_final)
            st.success(t["exit"])
            st.balloons()

# --- SECCIÓ 2: VOLCAT (Lògica de Traçabilitat) ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    
    # Calcular stock per cada ID_Lote
    if not df_actual.empty:
        # Sumem Campo i restem Recogido per a cada lot
        campo = df_actual[df_actual['Tipo'] == 'Campo'].groupby('ID_Lote')['Kg'].sum()
        recollit = df_actual[df_actual['Tipo'] == 'Recogido'].groupby('Ref_Original')['Kg'].sum()
        stock = campo.subtract(recollit, fill_value=0)
        
        # Filtrar només els que tenen stock > 0
        lots_amb_stock = stock[stock > 0]
        
        if not lots_amb_stock.empty:
            lot_triat = st.selectbox(t["tria_lot"], lots_amb_stock.index)
            st.metric(t["kg_disponibles"], f"{lots_amb_stock[lot_triat]} Kg")
            
            with st.form("form_volcat"):
                kg_volcat = st.number_input("Kg a bolcar:", min_value=0.0, max_value=float(lots_amb_stock[lot_triat]))
                submit_v = st.form_submit_button(t["botó_volcar"])
                
                if submit_v:
                    # Crear fila "Recogido" vinculada al lot original
                    fila_v = pd.DataFrame([{
                        "Fecha": datetime.now().strftime("%d/%m/%Y"),
                        "Finca": df_actual[df_actual['ID_Lote'] == lot_triat]['Finca'].values[0],
                        "Parcela": df_actual[df_actual['ID_Lote'] == lot_triat]['Parcela'].values[0],
                        "Tipo": "Recogido",
                        "Kg": kg_volcat,
                        "Cajas": 0,
                        "ID_Lote": f"VOL-{datetime.now().strftime('%H%M%S')}",
                        "Ref_Original": lot_triat
                    }])
                    df_final = pd.concat([df_actual, fila_v], ignore_index=True)
                    conn.update(data=df_final)
                    st.success(t["exit"])
        else:
            st.warning("No hi ha lots pendents en la cambra.")
    else:
        st.error("La base de dades està buida.")
