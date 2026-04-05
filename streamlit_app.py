import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓ I URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. TRADUCCIONS MILLORADES
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "hui": "📋 Entrades registrades hui:",
        "enters": "Kg (Enters)",
        "decimals": "Kg (Decimals)",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ Registrat correctament!",
        "cap_dada": "Encara no s'ha registrat res hui."
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "hui": "📋 Entradas registradas hoy:",
        "enters": "Kg (Enteros)",
        "decimals": "Kg (Decimales)",
        "botó_guardar": "💾 GUARDAR ENTRADA",
        "exit": "✅ ¡Registrado correctamente!",
        "cap_dada": "Aún no se ha registrado nada hoy."
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "hui": "📋 Înregistrări de astăzi:",
        "enters": "Kg (Întregi)",
        "decimals": "Kg (Zecimale)",
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
opcio = st.sidebar.radio("Navegació:", [t["menu_entrada"], t["menu_volcat"]])

# FUNCIÓ PER LLEGIR NOMÉS LES ENTRADES DE HUI
def carregar_dades_hui():
    try:
        df = pd.read_csv(URL_CSV)
        avui = datetime.now().strftime("%d/%m/%Y")
        # Filtrem perquè només apareguen les de hui
        df_hui = df[df['Fecha'] == avui]
        return df_hui
    except:
        return pd.DataFrame()

if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])
    
    # --- SELECTOR DE KG TIPUS RODA (Dues columnes) ---
    st.write(f"**{t['enters']} , {t['decimals']}**")
    col_int, col_dec = st.columns(2)
    with col_int:
        kg_int = st.number_input(t["enters"], min_value=0, max_value=5000, value=0, step=1)
    with col_dec:
        kg_dec = st.number_input(t["decimals"], min_value=0, max_value=99, value=0, step=1)
    
    kg_total = float(f"{kg_int}.{kg_dec:02d}")

    with st.form("form_entrada", clear_on_submit=True):
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
                    st.rerun() # Recarreguem per veure la dada a la taula de baix
                else: st.error(f"Error: {res.text}")
            except Exception as e: st.error(f"Error: {e}")

    # --- TAULA D'ENTRADES DE HUI ---
    st.divider()
    st.subheader(t["hui"])
    df_hui = carregar_dades_hui()
    if not df_hui.empty:
        # Mostrem les columnes més importants de les entrades de hui
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Tipo']].iloc[::-1], use_container_width=True)
    else:
        st.info(t["cap_dada"])

else:
    st.info("Secció de Volcat disponible en breu.")