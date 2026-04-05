import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓ I URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. ESTIL CSS (Bola gegant + número flotant)
st.markdown("""
    <style>
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 45px !important;
        height: 45px !important;
        background-color: #5D3FD3 !important;
        border: 3px solid white !important;
    }
    div[data-testid="stThumbValue"] {
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
        background-color: #5D3FD3 !important;
        padding: 5px !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Registrar Entrada Camp",
        "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Caixes dalt la bàscula",
        "n_palets": "Nº Palets dalt la bàscula",
        "brut": "Pes Brut de la Pesada",
        "afegeix": "➕ AFEGIR PESADA (NETA)",
        "net_total": "Pes Net Total del Lot",
        "botó_guardar": "💾 GUARDAR TOT EN SHEET",
        "tria_lot": "Selecciona el Lot a bolcar:",
        "disponible": "Disponible en cambra:",
        "n_caps_volcar": "Quantes caixes vas a bolcar?",
        "botó_volcar": "💾 REGISTRAR VOLCAT",
        "hui": "📋 Registre de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Registrar Entrada Campo",
        "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)",
        "tara_palet": "Tara Palet (kg)",
        "n_caps": "Nº Cajas sobre báscula",
        "n_palets": "Nº Palets sobre báscula",
        "brut": "Peso Bruto de la Pesada",
        "afegeix": "➕ AÑADIR PESADA (NETA)",
        "net_total": "Peso Neto Total del Lote",
        "botó_guardar": "💾 GUARDAR TODO EN SHEET",
        "tria_lot": "Selecciona el Lote a volcar:",
        "disponible": "Disponible en cámara:",
        "n_caps_volcar": "¿Cuántas cajas vas a volcar?",
        "botó_volcar": "💾 REGISTRAR VOLCADO",
        "hui": "📋 Registro de hoy:"
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

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# FUNCIÓ PER LLEGIR DADES
def carregar_tot():
    try:
        df = pd.read_csv(URL_CSV)
        if 'Kg' in df.columns:
            df['Kg'] = df['Kg'].astype(str).str.replace(',', '.').astype(float)
        return df
    except:
        return pd.DataFrame()

df_total = carregar_tot()

# ==========================================
# SECCIÓ 1: ENTRADA DE CAMP (RESTAURADA)
# ==========================================
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
        tara_tot = (v_n_caixes * v_tara_caixa) + (v_n_palets * v_tara_palet)
        pes_net = round(pes_brut - tara_tot, 2)
        st.session_state.llista_pesades.append({"net": pes_net, "caixes": v_n_caixes})

    if st.session_state.llista_pesades:
        st.divider()
        total_n = sum(p['net'] for p in st.session_state.llista_pesades)
        total_c = sum(p['caixes'] for p in st.session_state.llista_pesades)
        st.markdown(f"### 🏁 {t['net_total']}")
        st.metric(label="", value=f"{round(total_n, 2)} Kg NETS", delta=f"{total_c} Caixes")

        c_b1, c_b2 = st.columns(2)
        if c_b1.button("🗑️ REINICIAR"):
            st.session_state.llista_pesades = []
            st.rerun()
        if c_b2.button(t["botó_guardar"], type="primary"):
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel, "Parcela": parcela_sel, "Tipo": "Campo",
                "Kg": str(round(total_n, 2)).replace('.', ','),
                "Cajas": int(total_c),
                "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}-{parcela_sel[:3].upper()}",
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

# ==========================================
# SECCIÓ 2: VOLCAT (AMB CONTROL D'ESTOC)
# ==========================================
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        entrades = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg': 'sum', 'Cajas': 'sum', 'Finca': 'first', 'Parcela': 'first'}).reset_index()
        eixides = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg': 'sum', 'Cajas': 'sum'}).reset_index()
        estoc = pd.merge(entrades, eixides, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in', '_out')).fillna(0)
        estoc['Kg_Net'] = estoc['Kg_in'] - estoc['Kg_out']
        estoc['Caps_Net'] = estoc['Cajas_in'] - estoc['Cajas_out']
        lots_disponibles = estoc[estoc['Kg_Net'] > 0.5]
        
        if not lots_disponibles.empty:
            lots_disponibles['Label'] = lots_disponibles['ID_Lote'] + " | " + lots_disponibles['Finca']
            lot_sel_label = st.selectbox(t["tria_lot"], lots_disponibles['Label'])
            dades_lot = lots_disponibles[lots_disponibles['Label'] == lot_sel_label].iloc[0]
            
            st.metric(t["disponible"], f"{round(dades_lot['Kg_Net'], 2)} Kg", f"{int(dades_lot['Caps_Net'])} Caixes")
            mitjana = dades_lot['Kg_in'] / dades_lot['Cajas_in']
            
            with st.form("form_volcat"):
                caps_v = st.number_input(t["n_caps_volcar"], min_value=1, max_value=int(dades_lot['Caps_Net']), value=1)
                pes_suggerit = round(caps_v * mitjana, 2)
                pes_real_v = st.number_input("Pes del volcat (Kg):", value=float(pes_suggerit), step=0.1)
                
                if st.form_submit_button(t["botó_volcar"]):
                    dades_v = {
                        "Fecha": datetime.now().strftime("%d/%m/%Y"),
                        "Finca": dades_lot['Finca'], "Parcela": dades_lot['Parcela'], "Tipo": "Recogido",
                        "Kg": str(round(pes_real_v, 2)).replace('.', ','),
                        "Cajas": int(caps_v),
                        "ID_Lote": f"V-{datetime.now().strftime('%M%S')}",
                        "Ref_Original": dades_lot['ID_Lote']
                    }
                    try:
                        res = requests.post(URL_APPS_SCRIPT, json=dades_v)
                        if "Success" in res.text:
                            st.success("✅ Volcat registrat!")
                            st.rerun()
                    except: st.error("Error")
        else: st.warning("No hi ha fruita a la cambra.")
    else: st.info("Sense dades.")

# --- TAULA DE HUI ---
try:
    df_hui = df_total[df_total['Fecha'] == datetime.now().strftime("%d/%m/%Y")]
    if not df_hui.empty:
        st.divider()
        st.subheader(t["hui"])
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas', 'Tipo']].iloc[::-1], use_container_width=True)
except: pass