import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URL DE L'APPS SCRIPT (VERSIÓ 6)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbydcIn02OW80cs1Oua_vmCNvRLDgf1TDFRQe4Xv-efuL7_MxegZ08MgkMFh-hYrMr0H/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut de la Pesada", "n_caps": "Nº Caixes dalt bàscula", "n_palets": "Nº Palets dalt bàscula",
        "afegeix": "➕ AFEGIR AQUESTA PESADA (NETA)", "net_total": "Pes Net Total del Lot", "botó_guardar": "💾 GUARDAR TOT EN EL REGISTRE",
        "hui": "📋 Registres recents (🗑️ per esborrar):", "dispo": "Disponible:", "tria_lot": "Selecciona el Lot:",
        "recomenat": "Pes suggerit:", "botó_volcar": "🚜 REGISTRAR VOLCAT", "exit": "✅ Fet!"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto de la Pesada", "n_caps": "Nº Cajas sobre bàscula", "n_palets": "Nº Palets sobre bàscula",
        "afegeix": "➕ AÑADIR ESTA PESADA (NETA)", "net_total": "Peso Neto Total del Lote", "botó_guardar": "💾 GUARDAR TODO EN EL REGISTRE",
        "hui": "📋 Registros recientes (🗑️ para borrar):", "dispo": "Disponible:", "tria_lot": "Selecciona el Lote:",
        "recomenat": "Peso sugerido:", "botó_volcar": "🚜 REGISTRAR VOLCADO", "exit": "✅ ¡Hecho!"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp", "menu_volcat": "🚜 Răsturnare / Prelucrare",
        "tara_caixa": "Lada (kg)", "tara_palet": "Palet (kg)",
        "brut": "Greutate Brută", "n_caps": "Nr. Lăzi pe cântar", "n_palets": "Nr. Paleți pe cântar",
        "afegeix": "➕ ADAUGĂ ACEASTĂ CÂNTĂRIRE", "net_total": "Total Lot Acumulat", "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "hui": "📋 Înregistrări recente (🗑️ șterge):", "dispo": "Disponibil:", "tria_lot": "Selectați lotul:",
        "recomenat": "Greutate sugerată:", "botó_volcar": "🚜 ÎNREGISTREAZĂ DESCĂRCAREA", "exit": "✅ Gata!"
    }
}

# 3. ESTIL I CONFIGURACIÓ
st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width: 45px; height: 45px; background-color: #5D3FD3; border: 3px solid white;} div[data-testid="stThumbValue"] {font-size: 22px !important; font-weight: bold; color: white; background-color: #5D3FD3; padding: 5px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

# FUNCIÓ LLEGIR DADES REALS
@st.cache_data(ttl=2)
def carregar_dades():
    try:
        res = requests.get(f"{URL_APPS_SCRIPT}?cache={time.time()}")
        df = pd.DataFrame(res.json()[1:], columns=res.json()[0])
        df['Kg'] = pd.to_numeric(df['Kg'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        df['Cajas'] = pd.to_numeric(df['Cajas'], errors='coerce').fillna(0)
        return df
    except: return pd.DataFrame()

df_total = carregar_dades()
st.title(t["titol"])
opcio = st.sidebar.radio("Menu", [t["menu_entrada"], t["menu_volcat"]])

# --- SECCIÓ 1: ENTRADA ---
if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    col1, col2 = st.columns(2)
    v_tc = col1.number_input(t["tara_caixa"], 0.50)
    v_tp = col2.number_input(t["tara_palet"], 15.0)

    kg_s = st.slider("Kg", 0, 1000, 0)
    dec_s = st.slider("Decimals", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1>{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    v_nc = c1.number_input(t["n_caps"], 1)
    v_np = c2.number_input(t["n_palets"], 1)

    if st.button(t["afegeix"], use_container_width=True):
        t_n = round(p_brut - ((v_nc * v_tc) + (v_np * v_tp)), 2)
        st.session_state.llista_pesades.append({"net": t_n, "c": v_nc, "p": v_np})

    if st.session_state.llista_pesades:
        sn = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        sc = sum(p['c'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{sn} Kg Net", f"{sc} Capses")
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("🗑️ RESET"): st.session_state.llista_pesades = []; st.rerun()
        if col_b2.button(t["botó_guardar"], type="primary"):
            id_l = f"L-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(sn).replace('.', ','), "Cajas": int(sc), "ID_Lote": id_l, "Ref_Original": ""}
            if "Success" in requests.post(URL_APPS_SCRIPT, json=d).text:
                st.success(t["exit"]); st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()

    st.divider()
    st.subheader(t["hui"])
    if not df_total.empty:
        for _, r in df_total.tail(10).iloc[::-1].iterrows():
            c1, c2 = st.columns([4, 1])
            c1.write(f"📅 {r['Fecha']} | {r['Finca']} | **{r['Kg']}kg** ({r['Tipo']})")
            if c2.button("🗑️", key=f"del_{r['ID_Lote']}"):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                st.cache_data.clear(); st.rerun()

# --- SECCIÓ 2: VOLCAT ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in','_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        stk['Cap_N'] = stk['Cajas_in'] - stk['Cajas_out']
        dis = stk[stk['Kg_N'] > 0.1]
        if not dis.empty:
            dis['Lab'] = dis['ID_Lote'].str[-6:] + " | " + dis['Finca'] + " (" + dis['Kg_N'].astype(str) + "kg)"
            l_s = st.selectbox(t["tria_lot"], dis['Lab'])
            d_l = dis[dis['Lab'] == l_s].iloc[0]
            st.metric(t["dispo"], f"{round(d_l['Kg_N'],2)} Kg", f"{int(d_l['Cap_N'])} Capses")
            with st.form("v"):
                vc = st.number_input(t["n_caps_volcar"], 1, int(d_l['Cap_N']) if d_l['Cap_N']>0 else 100)
                mitjana = d_l['Kg_in']/d_l['Cajas_in'] if d_l['Cajas_in']>0 else 0
                vr = st.number_input("Kg:", value=float(round(vc * mitjana, 2)))
                if st.form_submit_button(t["botó_volcar"]):
                    dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": d_l['Finca'], "Parcela": "VOLCAT", "Tipo": "Recogido", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"V-{int(time.time())}", "Ref_Original": d_l['ID_Lote']}
                    requests.post(URL_APPS_SCRIPT, json=dv)
                    st.cache_data.clear(); st.rerun()
        else: st.warning("Buit.")