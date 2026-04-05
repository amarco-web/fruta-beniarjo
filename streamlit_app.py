import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. CONFIGURACIÓ I URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxiCwg9zaAyTeQjLstotGOHcAq4lSZdPwwlzRIdoKYbePXt7zBZP5MlH5DLhCqHh3kTLyMavOLWexq/pub?gid=0&single=true&output=csv"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp",
        "menu_volcat": "🚜 Volcat / Confecció",
        "finca": "Finca:", "parcela": "Parcel·la:",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut Actual", "n_caps": "Nº Caixes dalt bàscula", "n_palets": "Nº Palets dalt bàscula",
        "afegeix": "➕ AFEGIR PESADA", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot a bolcar:", "disponible": "Disponible en cambra:",
        "n_caps_volcar": "Quantes caixes vas a bolcar?", "botó_volcar": "💾 REGISTRAR VOLCAT",
        "recomenat": "Pes net suggerit:", "hui": "📋 Registre de hui:", "actualitzar": "🔄 ACTUALITZAR DADES"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo",
        "menu_volcat": "🚜 Volcado / Confección",
        "finca": "Finca:", "parcela": "Parcela:",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto Actual", "n_caps": "Nº Cajas sobre báscula", "n_palets": "Nº Palets sobre báscula",
        "afegeix": "➕ AÑADIR PESADA", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote a volcar:", "disponible": "Disponible en cámara:",
        "n_caps_volcar": "¿Cuántas cajas vas a volcar?", "botó_volcar": "💾 REGISTRAR VOLCADO",
        "recomenat": "Peso neto sugerido:", "hui": "📋 Registro de hoy:", "actualitzar": "🔄 ACTUALIZAR DATOS"
    },
    "Română": {
        "titol": "🟣 Control Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp",
        "menu_volcat": "🚜 Răsturnare / Prelucrare",
        "finca": "Ferma:", "parcela": "Parcela:",
        "tara_caixa": "Greutate Lada (kg)", "tara_palet": "Greutate Palet (kg)",
        "brut": "Greutate Brută", "n_caps": "Nr. Lăzi pe cântar", "n_palets": "Nr. Paleți pe cântar",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE", "net_total": "Greutate Netă Totală Lot", "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "tria_lot": "Selectați lotul:", "disponible": "Disponibil în depozit:",
        "n_caps_volcar": "Câte lăzi răsturnați?", "botó_volcar": "💾 ÎNREGISTREAZĂ DESCĂRCAREA",
        "recomenat": "Greutate netă sugerată:", "hui": "📋 Înregistrări astăzi:", "actualitzar": "🔄 ACTUALIZARE DATE"
    }
}

# 3. CONFIGURACIÓ
st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma / Limbă")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

if st.sidebar.button(t["actualitzar"]):
    st.cache_data.clear()
    st.rerun()

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# FUNCIÓ LLEGIR DADES AMB CACHE-BUSTER (Evita retards de Google)
@st.cache_data(ttl=10) # Només guarda la dada 10 segons
def carregar_tot():
    try:
        # Afegim un número aleatori al final de la URL perquè Google no ens done una versió vella
        url_fresca = f"{URL_CSV}&t={time.time()}"
        df = pd.read_csv(url_fresca)
        if 'Kg' in df.columns:
            # Netegem els kg per si venen amb coma
            df['Kg'] = df['Kg'].astype(str).str.replace(',', '.').astype(float)
        return df
    except Exception as e:
        return pd.DataFrame()

df_total = carregar_tot()

# --- SECCIÓ 1: ENTRADA ---
if opcio == t["menu_entrada"]:
    dades_fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox(t["finca"], list(dades_fincas.keys()))
    p_sel = st.selectbox(t["parcela"], dades_fincas[f_sel])

    col_t1, col_t2 = st.columns(2)
    v_tara_c = col_t1.number_input(t["tara_caixa"], value=0.50, step=0.01)
    v_tara_p = col_t2.number_input(t["tara_palet"], value=15.0, step=0.5)

    st.markdown(f"### ⚖️ {t['brut']}")
    kg_s = st.slider("Kg", 0, 1000, 0, step=1)
    dec_s = st.slider("Decimals", 0, 99, 0, step=1)
    p_brut = float(f"{kg_s}.{dec_s:02d}")

    st.markdown(f"""<div style="background-color: #f0f2f6; padding: 15px; border-radius: 15px; text-align: center; border: 3px solid #5D3FD3;"><h1 style="color: #5D3FD3; font-family: monospace; font-size: 60px; margin: 0;">{kg_s}<span style="font-size: 30px;">,{dec_s:02d}</span> Kg</h1></div>""", unsafe_allow_html=True)

    c_q1, c_q2 = st.columns(2)
    v_n_c = c_q1.number_input(t["n_caps"], value=1, min_value=0)
    v_n_p = c_q2.number_input(t["n_palets"], value=1, min_value=0)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        tara_tot = (v_n_c * v_tara_c) + (v_n_p * v_tara_p)
        st.session_state.llista_pesades.append({"net": round(p_brut - tara_tot, 2), "caixes": v_n_c})

    if st.session_state.llista_pesades:
        t_net = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        t_caps = sum(p['caixes'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{t_net} Kg", f"{t_caps} Capses")
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(t_net).replace('.', ','), "Cajas": int(t_caps), "ID_Lote": f"{datetime.now().strftime('%Y%m%d')}-{f_sel[:3].upper()}", "Ref_Original": ""}
            res = requests.post(URL_APPS_SCRIPT, json=d)
            if "Success" in res.text:
                st.success("✅ OK!"); st.session_state.llista_pesades = []; st.balloons(); st.cache_data.clear(); st.rerun()

# --- SECCIÓ 2: VOLCAT ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg': 'sum', 'Cajas': 'sum', 'Finca': 'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg': 'sum', 'Cajas': 'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in', '_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        stk['Cap_N'] = stk['Cajas_in'] - stk['Cajas_out']
        dispo = stk[stk['Kg_N'] > 0.1] # Umbral de 100 grams
        if not dispo.empty:
            dispo['Lab'] = dispo['ID_Lote'] + " | " + dispo['Finca'] + " (" + dispo['Kg_N'].round(2).astype(str) + "kg)"
            l_sel = st.selectbox(t["tria_lot"], dispo['Lab'])
            d_l = dispo[dispo['Lab'] == l_sel].iloc[0]
            st.metric(t["disponible"], f"{round(d_l['Kg_N'], 2)} Kg", f"{int(d_l['Cap_N'])} Capses")
            with st.form("f_v"):
                v_c = st.number_input(t["n_caps_volcar"], min_value=1, max_value=int(d_l['Cap_N']) if d_l['Cap_N'] > 0 else 1, value=1)
                mitjana = d_l['Kg_in'] / d_l['Cajas_in'] if d_l['Cajas_in'] > 0 else 0
                v_p = round(v_c * mitjana, 2)
                st.write(f"💡 {t['recomenat']} {v_p} Kg")
                v_real = st.number_input("Kg reals:", value=float(v_p))
                if st.form_submit_button(t["botó_volcar"]):
                    dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": d_l['Finca'], "Parcela": "VOLCAT", "Tipo": "Recogido", "Kg": str(round(v_real, 2)).replace('.', ','), "Cajas": int(v_c), "ID_Lote": f"V-{datetime.now().strftime('%M%S')}", "Ref_Original": d_l['ID_Lote']}
                    if "Success" in requests.post(URL_APPS_SCRIPT, json=dv).text: 
                        st.success("✅ OK!"); st.cache_data.clear(); st.rerun()
        else: st.warning("No hi ha fruita a la cambra disponible.")
    else: st.info("Sense dades en el registre.")

# --- HISTORIAL HUI ---
try:
    df_h = df_total[df_total['Fecha'] == datetime.now().strftime("%d/%m/%Y")]
    if not df_h.empty:
        st.divider(); st.subheader(t["hui"])
        st.dataframe(df_h[['Finca', 'Kg', 'Cajas', 'Tipo']].iloc[::-1], use_container_width=True)
except: pass