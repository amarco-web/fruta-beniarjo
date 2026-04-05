import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓ I URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "hui": "📋 Entrades de hui:",
        "kg_label": "Pes total (Kg):",
        "enters": "Enters",
        "decimals": "Decimals",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ Registrat correctament!",
        "cap_dada": "Encara no s'ha registrat res hui."
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "hui": "📋 Entradas de hoy:",
        "kg_label": "Peso total (Kg):",
        "enters": "Enteros",
        "decimals": "Decimales",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ ¡Registrado correctamente!",
        "cap_dada": "Aún no se ha registrado nada hoy."
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "hui": "📋 Înregistrări astăzi:",
        "kg_label": "Greutate (Kg):",
        "enters": "Întregi",
        "decimals": "Zecimale",
        "botó_guardar": "💾 SALVEAZĂ INTRAREA",
        "exit": "✅ Înregistrat cu succes!",
        "cap_dada": "Nicio înregistrare astăzi."
    }
}

dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# SELECTOR D'IDIOMA
st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], "Volcat (Pròximament)"])

def carregar_dades_hui():
    try:
        df = pd.read_csv(URL_CSV)
        avui = datetime.now().strftime("%d/%m/%Y")
        return df[df['Fecha'] == avui]
    except:
        return pd.DataFrame()

if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])
    
    st.markdown(f"### {t['kg_label']}")
    
    # --- LES RODES (ROLLERS) ---
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        # Roda per als enters (0 a 1000)
        kg_enters = st.selectbox(t["enters"], options=list(range(1001)), index=0)
    
    with col_r2:
        # Roda per als decimals (00 a 99)
        llista_decimals = [f"{i:02d}" for i in range(100)]
        kg_dec_text = st.selectbox(t["decimals"], options=llista_decimals, index=0)
    
    # Combinem el valor
    kg_total = float(f"{kg_enters}.{kg_dec_text}")
    st.info(f"📍 **{kg_enters},{kg_dec_text} Kg**")

    with st.form("form_final"):
        cajas = st.number_input("Cajas:", min_value=0, step=1)
        submit = st.form_submit_button(t["botó_guardar"])
        
        if submit:
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel,
                "Parcela": parcela_sel,
                "Tipo": "Campo",
                "Kg": str(kg_total).replace('.', ','),
                "Cajas": int(cajas),
                "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}",
                "Ref_Original": ""
            }
            try:
                res = requests.post(URL_APPS_SCRIPT, json=dades)
                if "Success" in res.text:
                    st.success(t["exit"])
                    st.balloons()
                    st.rerun()
                else: st.error(f"Error: {res.text}")
            except Exception as e: st.error(f"Error: {e}")

    # --- TAULA DE HUI ---
    st.divider()
    st.subheader(t["hui"])
    df_hui = carregar_dades_hui()
    if not df_hui.empty:
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas']].iloc[::-1], use_container_width=True)
    else:
        st.info(t["cap_dada"])