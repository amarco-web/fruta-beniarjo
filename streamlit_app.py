import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. ESTIL PERSONALITZAT PER A CURSORS GRANS (CSS)
st.markdown("""
    <style>
    /* Fer la bola del cursor més gran */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 30px;
        height: 30px;
        background-color: #5D3FD3;
        border: 2px solid white;
    }
    /* Fer el número que flota sobre la bola més gran */
    .stSlider [data-baseweb="slider"] [role="slider"] > div {
        font-size: 18px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "Registrar Entrada Camp",
        "tara_caixa": "Tara Caixa (kg)",
        "tara_palet": "Tara Palet (kg)",
        "afegeix": "➕ AFEGIR PESADA",
        "net": "Pes Net Total",
        "botó_guardar": "💾 GUARDAR TOT EN SHEET",
        "hui": "📋 Registre de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "tara_caixa": "Tara Caja (kg)",
        "tara_palet": "Tara Palet (kg)",
        "afegeix": "➕ AÑADIR PESADA",
        "net": "Peso Neto Total",
        "botó_guardar": "💾 GUARDAR TODO EN SHEET",
        "hui": "📋 Registro de hoy:"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "tara_caixa": "Tara Lada (kg)",
        "tara_palet": "Tara Palet (kg)",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE",
        "net": "Greutate Netă Totală",
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

st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], "Volcat (Pròximament)"])

if opcio == t["menu_entrada"]:
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])
    
    # --- PES BRUT AMB CURSORS MILLORATS ---
    st.markdown("### Pes Brut Actual")
    kg_slider = st.slider("Kg", 0, 1000, 0, step=1)
    dec_slider = st.slider("Decimals", 0, 99, 0, step=1)
    
    pes_brut_actual = float(f"{kg_slider}.{dec_slider:02d}")
    
    # Visor digital gran
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 15px; text-align: center; border: 3px solid #5D3FD3; margin-bottom: 20px;">
            <h1 style="color: #5D3FD3; font-family: monospace; font-size: 70px; margin: 0;">
                {kg_slider}<span style="font-size: 35px;">,{dec_slider:02d}</span> <span style="font-size: 20px;">Kg</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    num_caps_pesada = c1.number_input("Nº Capses d'aquesta pesada", value=1, min_value=1)
    tara_caixa_individual = c2.number_input(t["tara_caixa"], value=0.50, step=0.01)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        st.session_state.llista_pesades.append({
            "brut": pes_brut_actual,
            "caps": num_caps_pesada,
            "tara_c": tara_caixa_individual
        })

    # --- RESUM I CONFIGURACIÓ FINAL ---
    if st.session_state.llista_pesades:
        st.divider()
        total_brut = sum(p['brut'] for p in st.session_state.llista_pesades)
        total_caps = sum(p['caps'] for p in st.session_state.llista_pesades)
        total_tara_caps = sum(p['caps'] * p['tara_c'] for p in st.session_state.llista_pesades)
        
        # Agrupem ací Palets i Guardar
        col_f1, col_f2 = st.columns(2)
        n_palets = col_f1.number_input("Nº Palets totals", value=1, min_value=0)
        tara_palet_unitari = col_f2.number_input(t["tara_palet"], value=15.0, step=0.5)
        
        pes_tara_total = total_tara_caps + (n_palets * tara_palet_unitari)
        pes_net_final = round(total_brut - pes_tara_total, 2)
        
        st.metric(label=t["net"], value=f"{pes_net_final} Kg", delta=f"Tara total: -{round(pes_tara_total,2)} kg")

        # Botons d'acció
        cb1, cb2 = st.columns(2)
        if cb1.button("🗑️ REINICIAR", use_container_width=True):
            st.session_state.llista_pesades = []
            st.rerun()

        if cb2.button(t["botó_guardar"], type="primary", use_container_width=True):
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel, "Parcela": parcela_sel, "Tipo": "Campo",
                "Kg": str(pes_net_final).replace('.', ','),
                "Cajas": int(total_caps),
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

    # --- TAULA DE HUI ---
    try:
        df = pd.read_csv(URL_CSV)
        df_hui = df[df['Fecha'] == datetime.now().strftime("%d/%m/%Y")]
        if not df_hui.empty:
            st.divider()
            st.subheader(t["hui"])
            st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas']].iloc[::-1], use_container_width=True)
    except: pass