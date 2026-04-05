import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URL APPS SCRIPT
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbezps3hmJd44mDWLiaHGvDn1cvC4zqblgoYGJk1G3puGDbRu9_XP4eLGcO6FLhQvxEs/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut Pesada", "n_caps": "Nº Caixes", "n_palets": "Nº Palets",
        "afegeix": "➕ AFEGIR PESADA", "net_total": "Total Lot Acumulat", "botó_guardar": "💾 GUARDAR EN SHEET",
        "hui": "📋 Registres recents (🗑️ per esborrar):", "exit": "✅ Registrat!", "dispo": "Disponible:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto Pesada", "n_caps": "Nº Cajas", "n_palets": "Nº Palets",
        "afegeix": "➕ AÑADIR PESADA", "net_total": "Total Lote Acumulado", "botó_guardar": "💾 GUARDAR EN SHEET",
        "hui": "📋 Registros recientes (🗑️ para borrar):", "exit": "✅ ¡Hecho!", "dispo": "Disponible:"
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano"])
t = traduccions[idioma]

# LLEGIR DADES
@st.cache_data(ttl=2)
def carregar_dades():
    try:
        res = requests.get(f"{URL_APPS_SCRIPT}?cache={time.time()}")
        df = pd.DataFrame(res.json()[1:], columns=res.json()[0])
        # Neteja de columnes
        df.columns = df.columns.str.strip()
        df['Kg'] = pd.to_numeric(df['Kg'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        df['Cajas'] = pd.to_numeric(df['Cajas'], errors='coerce').fillna(0)
        return df
    except: return pd.DataFrame()

df_total = carregar_dades()

st.title(t["titol"])
opcio = st.sidebar.radio("Nav", [t["menu_entrada"], t["menu_volcat"]])

if opcio == t["menu_entrada"]:
    # --- SECCIÓ ENTRADA (TARES I PESADES) ---
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    col1, col2 = st.columns(2)
    v_tc = col1.number_input(t["tara_caixa"], 0.50)
    v_tp = col2.number_input(t["tara_palet"], 15.0)

    kg_s = st.slider("Kg", 0, 1000, 0)
    dec_s = st.slider("Dec", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1>{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    v_nc = c1.number_input(t["n_caps"], 1)
    v_np = c2.number_input(t["n_palets"], 1)

    if st.button(t["afegeix"], use_container_width=True):
        t_n = round(p_brut - ((v_nc * v_tc) + (v_np * v_tp)), 2)
        st.session_state.llista_pesades.append({"net": t_n, "c": v_nc})

    if st.session_state.llista_pesades:
        sn = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        sc = sum(p['c'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{sn} Kg Net", f"{sc} Capses")
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(sn).replace('.', ','), "Cajas": int(sc), "ID_Lote": f"L-{int(time.time())}", "Ref_Original": ""}
            requests.post(URL_APPS_SCRIPT, json=d)
            st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()

    # --- HISTORIAL DE CORRECCIÓ (PUNT 4) ---
    st.divider()
    st.subheader(t["hui"])
    if not df_total.empty:
        # Intentem filtrar per hui, si no hi ha res, mostrem els últims 5
        av = datetime.now().strftime("%d/%m/%Y")
        df_hui = df_total[df_total['Fecha'].astype(str).str.contains(av, na=False)]
        
        if df_hui.empty: # Si hui no hi ha res, agafem els últims del llistat
            df_mostrar = df_total.tail(5)
        else:
            df_mostrar = df_hui

        for _, r in df_mostrar.iloc[::-1].iterrows():
            c1, c2 = st.columns([4, 1])
            c1.write(f"📅 {r['Fecha']} | {r['Finca']} | **{r['Kg']}kg**")
            if c2.button("🗑️", key=f"del_{r['ID_Lote']}"):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                st.cache_data.clear(); st.rerun()

elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in','_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        dis = stk[stk['Kg_N'] > 0.1]
        if not dis.empty:
            l_s = st.selectbox("Lot:", dis['ID_Lote'] + " | " + dis['Finca'])
            lot_id = l_s.split(" | ")[0]
            val = dis[dis['ID_Lote'] == lot_id].iloc[0]
            st.metric(t["dispo"], f"{round(val['Kg_N'],2)} Kg")
            v_kg = st.number_input("Kg a bolcar:", 0.0, float(val['Kg_N']))
            if st.button("🚜 VOLCAR"):
                dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": "Volcat", "Parcela": "Volcat", "Tipo": "Recogido", "Kg": str(v_kg).replace('.',','), "Cajas": 0, "ID_Lote": f"V-{int(time.time())}", "Ref_Original": lot_id}
                requests.post(URL_APPS_SCRIPT, json=dv)
                st.cache_data.clear(); st.rerun()