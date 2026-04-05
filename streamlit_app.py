import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. URLS I CONFIGURACIÓ
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. ESTIL CSS (Bola del cursor gegant)
st.markdown("""
    <style>
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 35px;
        height: 35px;
        background-color: #5D3FD3;
        border: 2px solid white;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] > div {
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "tara_caixa": "Tara Caixa (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Caixes pesades",
        "n_palets": "Nº Palets pesats",
        "brut": "Pes Brut Actual",
        "afegeix": "➕ AFEGIR PESADA NETEJADA",
        "net_total": "Pes Net Total Acumulat",
        "botó_guardar": "💾 GUARDAR TOT EN SHEET",
        "hui": "📋 Registre de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "tara_caixa": "Tara Caja (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Cajas pesadas",
        "n_palets": "Nº Palets pesados",
        "brut": "Peso Bruto Actual",
        "afegeix": "➕ AÑADIR PESADA LIMPIA",
        "net_total": "Peso Neto Total Acumulado",
        "botó_guardar": "💾 GUARDAR TODO EN SHEET",
        "hui": "📋 Registro de hoy:"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "tara_caixa": "Tara Lada (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nr. Lăzi cântărite",
        "n_palets": "Nr. Paleți cântăriți",
        "brut": "Greutate Brută",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE NETĂ",
        "net_total": "Greutate Netă Totală",
        "botó_guardar": "💾 SALVEAZĂ TOT",
        "hui": "📋 Înregistrări astăzi:"
    }
}

dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

if 'llista_pesades' not in st.session_state:
    st.session_state.llista_pesades = []

# IDIOMA
st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])

# SELECCIÓ FINCA
finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])

st.divider()

# --- 1. DALT: TARES ---
st.markdown(f"#### ⚙️ Configurar Tares")
col_t1, col_t2 = st.columns(2)
with col_t1:
    v_tara_caixa = st.number_input(t["tara_caixa"], value=0.50, step=0.01)
with col_t2:
    v_tara_palet = st.number_input(t["tara_palet"], value=15.0, step=0.5)

st.divider()

# --- 2. MIG: CURSORS DE PES ---
st.markdown(f"### ⚖️ {t['brut']}")
kg_s = st.slider("Kg", 0, 1500, 0, step=1)
dec_s = st.slider("Decimals", 0, 99, 0, step=1)
pes_brut = float(f"{kg_s}.{dec_s:02d}")

# Visor Digital
st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 15px; text-align: center; border: 3px solid #5D3FD3;">
        <h1 style="color: #5D3FD3; font-family: monospace; font-size: 80px; margin: 0;">
            {kg_s}<span style="font-size: 40px;">,{dec_s:02d}</span> <span style="font-size: 25px;">Kg</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# --- 3. BAIX: QUANTITATS I AFEGIR ---
st.markdown(" ")
col_q1, col_q2 = st.columns(2)
with col_q1:
    v_n_caixes = st.number_input(t["n_caps"], value=1, min_value=0)
with col_q2:
    v_n_palets = st.number_input(t["n_palets"], value=1, min_value=0)

if st.button(t["afegeix"], type="secondary", use_container_width=True):
    # Càlcul del net d'aquesta pesada
    tara_total_pesada = (v_n_caixes * v_tara_caixa) + (v_n_palets * v_tara_palet)
    pes_net_pesada = round(pes_brut - tara_total_pesada, 2)
    
    st.session_state.llista_pesades.append({
        "brut": pes_brut,
        "net": pes_net_pesada,
        "caixes": v_n_caixes,
        "palets": v_n_palets
    })

# --- RESUM I ENVIAMENT ---
if st.session_state.llista_pesades:
    st.divider()
    total_net = sum(p['net'] for p in st.session_state.llista_pesades)
    total_caixes = sum(p['caixes'] for p in st.session_state.llista_pesades)
    
    st.markdown(f"### 📦 {t['net_total']}")
    st.metric(label="", value=f"{round(total_net, 2)} Kg Net", delta=f"{total_caixes} Caixes totals")

    # Llista detallada
    with st.expander("Veure detall de pesades"):
        for i, p in enumerate(st.session_state.llista_pesades):
            st.write(f"Pesada {i+1}: Brut {p['brut']}kg - Tara ({p['caixes']}C + {p['palets']}P) = **{p['net']} kg Net**")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ REINICIAR", use_container_width=True):
            st.session_state.llista_pesades = []
            st.rerun()
    with col_btn2:
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel, "Parcela": parcela_sel, "Tipo": "Campo",
                "Kg": str(round(total_net, 2)).replace('.', ','),
                "Cajas": int(total_caixes),
                "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}",
                "Ref_Original": ""
            }
            try:
                res = requests.post(URL_APPS_SCRIPT, json=dades)
                if "Success" in res.text:
                    st.success("✅ Guardat al Sheets!")
                    st.session_state.llista_pesades = []
                    st.balloons()
                    st.rerun()
            except: st.error("Error de connexió")

# --- HISTORIAL HUI ---
try:
    df = pd.read_csv(URL_CSV)
    df_hui = df[df['Fecha'] == datetime.now().strftime("%d/%m/%Y")]
    if not df_hui.empty:
        st.divider()
        st.subheader(t["hui"])
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas']].iloc[::-1], use_container_width=True)
except: pass