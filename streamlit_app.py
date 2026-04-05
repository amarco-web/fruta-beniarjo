import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓ I URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. ESTIL CSS (Bola del cursor gegant per a mòbil)
st.markdown("""
    <style>
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 45px !important;
        height: 45px !important;
        background-color: #5D3FD3 !important;
        border: 3px solid white !important;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] > div {
        font-size: 22px !important;
        font-weight: bold;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "menu_volcat": "Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Caixes dalt la bàscula",
        "n_palets": "Nº Palets dalt la bàscula",
        "brut": "Pes Brut de la Pesada",
        "afegeix": "➕ AFEGIR AQUESTA PESADA (NETA)",
        "net_total": "Pes Net Total del Lot",
        "botó_guardar": "💾 GUARDAR TOT EN EL REGISTRE",
        "hui": "📋 Registre d'entrades de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "menu_volcat": "Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Cajas sobre báscula",
        "n_palets": "Nº Palets sobre báscula",
        "brut": "Peso Bruto de la Pesada",
        "afegeix": "➕ AÑADIR ESTA PESADA (NETA)",
        "net_total": "Peso Neto Total del Lote",
        "botó_guardar": "💾 GUARDAR TODO EN EL REGISTRE",
        "hui": "📋 Registro de entradas de hoy:"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "menu_volcat": "Răsturnare / Prelucrare",
        "tara_caixa": "Tara Lada (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nr. Lăzi pe cântar",
        "n_palets": "Nr. Paleți pe cântar",
        "brut": "Greutate Brută Cântărire",
        "afegeix": "➕ ADAUGĂ ACEASTĂ CÂNTĂRIRE (NETĂ)",
        "net_total": "Greutate Netă Totală Lot",
        "botó_guardar": "💾 SALVEAZĂ TOT",
        "hui": "📋 Înregistrări astăzi:"
    }
}

# 4. CONFIGURACIÓ PÀGINA
st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# DADES FINQUES
dades_fincas = {
    "Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"],
    "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"],
    "Castelló": ["Castelló", "Sagra"],
    "Marapego": ["Lanelate", "Murcott", "Ortanique"]
}

# MEMÒRIA TEMPORAL
if 'llista_pesades' not in st.session_state:
    st.session_state.llista_pesades = []

# SELECTOR IDIOMA
st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# --- SECCIÓ 1: ENTRADA ---
if opcio == t["menu_entrada"]:
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])

    st.divider()
    st.markdown(f"#### ⚙️ 1. Configurar Tares")
    col_t1, col_t2 = st.columns(2)
    v_tara_caixa = col_t1.number_input(t["tara_caixa"], value=0.50, step=0.01)
    v_tara_palet = col_t2.number_input(t["tara_palet"], value=15.0, step=0.5)

    st.divider()
    st.markdown(f"### ⚖️ 2. {t['brut']}")
    kg_s = st.slider("Kg", 0, 1000, 0, step=1)
    dec_s = st.slider("Decimals", 0, 99, 0, step=1)
    pes_brut = float(f"{kg_s}.{dec_s:02d}")

    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 15px; text-align: center; border: 3px solid #5D3FD3;">
            <h1 style="color: #5D3FD3; font-family: monospace; font-size: 80px; margin: 0;">
                {kg_s}<span style="font-size: 40px;">,{dec_s:02d}</span> <span style="font-size: 25px;">Kg</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"#### 📦 3. Quantitats dalt la bàscula")
    col_q1, col_q2 = st.columns(2)
    v_n_caixes = col_q1.number_input(t["n_caps"], value=1, min_value=0)
    v_n_palets = col_q2.number_input(t["n_palets"], value=1, min_value=0)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        tara_total_pesada = (v_n_caixes * v_tara_caixa) + (v_n_palets * v_tara_palet)
        pes_net_pesada = round(pes_brut - tara_total_pesada, 2)
        st.session_state.llista_pesades.append({
            "net": pes_net_pesada,
            "caixes": v_n_caixes
        })

    if st.session_state.llista_pesades:
        st.divider()
        total_net = sum(p['net'] for p in st.session_state.llista_pesades)
        total_caixes = sum(p['caixes'] for p in st.session_state.llista_pesades)
        st.markdown(f"### 🏁 {t['net_total']}")
        st.metric(label="", value=f"{round(total_net, 2)} Kg NETS", delta=f"{total_caixes} Caixes")

        c_b1, c_b2 = st.columns(2)
        if c_b1.button("🗑️ REINICIAR"):
            st.session_state.llista_pesades = []
            st.rerun()
        if c_b2.button(t["botó_guardar"], type="primary"):
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
                    st.success("✅ Guardat!")
                    st.session_state.llista_pesades = []
                    st.balloons()
                    st.rerun()
            except: st.error("Error")

# --- HISTORIAL ---
elif opcio == t["menu_volcat"]:
    st.info("Secció de volcat pròximament...")

try:
    df = pd.read_csv(URL_CSV)
    df_hui = df[df['Fecha'] == datetime.now().strftime("%d/%m/%Y")]
    if not df_hui.empty:
        st.divider()
        st.subheader(t["hui"])
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas']].iloc[::-1], use_container_width=True)
except:
    pass