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
        "pesades": "Pesades acumulades",
        "tara_caixa": "Tara Caixa (kg)",
        "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut Actual",
        "net": "Pes Net Total",
        "afegeix": "➕ AFEGIR PESADA",
        "borrar_tot": "🗑️ REINICIAR",
        "botó_guardar": "💾 GUARDAR EN SHEET",
        "exit": "✅ Enviat al Google Sheets!",
        "hui": "📋 Registre de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "Registrar Entrada Campo",
        "pesades": "Pesadas acumuladas",
        "tara_caixa": "Tara Caja (kg)",
        "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto Actual",
        "net": "Peso Neto Total",
        "afegeix": "➕ AÑADIR PESADA",
        "borrar_tot": "🗑️ REINICIAR",
        "botó_guardar": "💾 GUARDAR EN SHEET",
        "exit": "✅ ¡Enviado al Google Sheets!",
        "hui": "📋 Registro de hoy:"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "Înregistrare intrare",
        "pesades": "Cântăriri acumulate",
        "tara_caixa": "Tara Lada (kg)",
        "tara_palet": "Tara Palet (kg)",
        "brut": "Greutate Brută",
        "net": "Greutate Netă Totală",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE",
        "borrar_tot": "🗑️ RESTART",
        "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "exit": "✅ Trimis cu succes!",
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
opcio = st.sidebar.radio("Menu", [t["menu_entrada"], "Volcat (Pròximament)"])

if opcio == t["menu_entrada"]:
    finca_sel = st.selectbox("Finca:", list(dades_fincas.keys()))
    parcela_sel = st.selectbox("Parcel·la:", dades_fincas[finca_sel])
    
    st.divider()
    
    # --- CONFIGURACIÓ DE TARA ---
    col_t1, col_t2, col_t3 = st.columns(3)
    tara_c = col_t1.number_input(t["tara_caixa"], value=0.5, step=0.05)
    n_palets = col_t2.number_input("Nº Palets", value=1, step=1)
    tara_p = col_t3.number_input(t["tara_palet"], value=15.0, step=0.5)

    st.divider()

    # --- SELECTORS DE CURSOR (SLIDERS) ESTIL IMATGE ---
    st.write(f"### {t['brut']}")
    
    # Sliders per a Kg i Decimals
    kg_slider = st.slider("Kg", 0, 1000, 0, step=1)
    dec_slider = st.slider("Decimals", 0, 95, 0, step=5) # Pas de 5 en 5 per a anar més ràpid
    
    pes_brut_actual = float(f"{kg_slider}.{dec_slider:02d}")
    
    # Visor digital gran
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #5D3FD3;">
            <h1 style="color: #5D3FD3; font-family: monospace; font-size: 60px; margin: 0;">
                {kg_slider}<span style="font-size: 30px;">,{dec_slider:02d}</span> <span style="font-size: 20px;">Kg</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)

    num_caps_pesada = st.number_input("Nº Capses d'aquesta pesada", value=1, step=1)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        st.session_state.llista_pesades.append({
            "brut": pes_brut_actual,
            "caps": num_caps_pesada
        })

    # --- LLISTA ACUMULADA ---
    if st.session_state.llista_pesades:
        st.write(f"#### {t['pesades']}")
        total_brut = 0
        total_caps = 0
        for i, p in enumerate(st.session_state.llista_pesades):
            st.write(f"⚖️ {i+1}. **{p['brut']} kg** ({p['caps']} caps.)")
            total_brut += p['brut']
            total_caps += p['caps']
        
        pes_tara_total = (total_caps * tara_c) + (n_palets * tara_p)
        pes_net_final = round(total_brut - pes_tara_total, 2)
        
        st.metric(label=t["net"], value=f"{pes_net_final} Kg", delta=f"Tara: -{round(pes_tara_total,2)} kg")

        c1, c2 = st.columns(2)
        if c1.button(t["borrar_tot"], use_container_width=True):
            st.session_state.llista_pesades = []
            st.rerun()

        if c2.button(t["botó_guardar"], type="primary", use_container_width=True):
            dades = {
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Finca": finca_sel,
                "Parcela": parcela_sel,
                "Tipo": "Campo",
                "Kg": str(pes_net_final).replace('.', ','),
                "Cajas": int(total_caps),
                "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{finca_sel[:3].upper()}",
                "Ref_Original": ""
            }
            try:
                res = requests.post(URL_APPS_SCRIPT, json=dades)
                if "Success" in res.text:
                    st.success(t["exit"])
                    st.session_state.llista_pesades = []
                    st.balloons()
                    st.rerun()
            except:
                st.error("Error")

    # --- TAULA DE HUI ---
    try:
        df = pd.read_csv(URL_CSV)
        avui = datetime.now().strftime("%d/%m/%Y")
        df_hui = df[df['Fecha'] == avui]
        if not df_hui.empty:
            st.divider()
            st.subheader(t["hui"])
            st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas']].iloc[::-1], use_container_width=True)
    except:
        pass