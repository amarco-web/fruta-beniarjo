import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ID del teu fitxer (està en la URL)
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"

st.set_page_config(page_title="Control Maracuia", page_icon="🟣")
conn = st.connection("gsheets", type=GSheetsConnection)

# LLEGIR DADES
try:
    # Intentem llegir usant la ID directa
    df_actual = conn.read(spreadsheet=SHEET_ID, worksheet="Full 1", ttl=0)
    df_actual = df_actual.dropna(how="all")
except Exception as e:
    st.error(f"Error de lectura: {e}")
    df_actual = pd.DataFrame(columns=["Fecha", "Finca", "Parcela", "Tipo", "Kg", "Cajas", "ID_Lote", "Ref_Original"])

st.title("🟣 Control Maracuia - Beniarjó")

opcio = st.sidebar.radio("Navegació:", ["Registrar Entrada", "Volcat"])

if opcio == "Registrar Entrada":
    with st.form("entrada"):
        finca = st.selectbox("Finca:", ["Cooperativa", "Tarraso", "Castelló", "Marapego"])
        kg = st.number_input("Kg:", min_value=0.0)
        if st.form_submit_button("💾 GUARDAR"):
            nova_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca,
                "Tipo": "Campo",
                "Kg": kg,
                "ID_Lote": f"L-{datetime.now().strftime('%M%S')}"
            }])
            df_final = pd.concat([df_actual, nova_fila], ignore_index=True)
            
            # EL MOMENT DE L'ESCRIPTURA
            try:
                conn.update(spreadsheet=SHEET_ID, worksheet="Full 1", data=df_final)
                st.success("✅ Guardat al compte de l'empresa!")
                st.cache_data.clear()
            except Exception as e:
                st.error("❌ Google Workspace ha bloquejat l'escriptura.")
                st.info("Això sol ser perquè l'administrador de l'empresa ha de 'confiar' en aquesta App.")
                st.write(f"Detall de l'error: {e}")

else:
    st.write("Secció de volcat llista per a quan funcione la connexió.")
