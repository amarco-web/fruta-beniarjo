import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyryYeSXGhmhCsmve6wNv7yn_mrRKvRaD2bdweUdwmTGzQgWChRBjctkB1mI-hGR2w7/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxiCwg9zaAyTeQjLstotGOHcAq4lSZdPwwlzRIdoKYbePXt7zBZP5MlH5DLhCqHh3kTLyMavOLWexq/pub?gid=0&single=true&output=csv"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut", "n_caps": "Nº Caixes", "n_palets": "Nº Palets",
        "afegeix": "➕ AFEGIR PESADA", "net_total": "Total Lot", "botó_guardar": "💾 GUARDAR TOT",
        "tria_lot": "Lot:", "dispo": "Disponible:", "botó_volcar": "💾 VOLCAR",
        "hui": "📋 Entrades de hui:", "buit": "No hi ha registres hui."
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto", "n_caps": "Nº Cajas", "n_palets": "Nº Palets",
        "afegeix": "➕ AÑADIR PESADA", "net_total": "Total Lote", "botó_guardar": "💾 GUARDAR TODO",
        "tria_lot": "Lote:", "dispo": "Disponible:", "botó_volcar": "💾 VOLCAR",
        "hui": "📋 Entradas de hoy:", "buit": "No hay registros hoy."
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp", "menu_volcat": "🚜 Răsturnare",
        "tara_caixa": "Lada (kg)", "tara_palet": "Palet (kg)",
        "brut": "Greutate Brută", "n_caps": "Nr. Lăzi", "n_palets": "Nr. Paleți",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE", "net_total": "Total Lot", "botó_guardar": "💾 SALVEAZĂ",
        "tria_lot": "Lot:", "dispo": "Disponibil:", "botó_volcar": "💾 RĂSTURNARE",
        "hui": "📋 Înregistrări astăzi:", "buit": "Nicio înregistrare astăzi."
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣")
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width:45px;height:45px;background-color:#5D3FD3;border:3px solid white;} div[data-testid="stThumbValue"] {font-size:20px !important;font-weight:bold;color:white;background-color:#5D3FD3;padding:5px;border-radius:8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("Limbă", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

@st.cache_data(ttl=2)
def carregar_dades():
    try:
        res = requests.get(f"{URL_CSV}&cache={time.time()}")
        df = pd.read_csv(res.url)
        df['Kg'] = pd.to_numeric(df['Kg'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        df['Cajas'] = pd.to_numeric(df['Cajas'], errors='coerce').fillna(0)
        df['Fecha'] = df['Fecha'].astype(str).str.strip()
        return df
    except: return pd.DataFrame()

df_total = carregar_dades()
st.title(t["titol"])
opcio = st.sidebar.radio("Nav", [t["menu_entrada"], t["menu_volcat"]])

if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])
    c1, c2 = st.columns(2)
    v_tc = c1.number_input(t["tara_caixa"], 0.50)
    v_tp = c2.number_input(t["tara_palet"], 15.0)
    kg_s = st.slider("Kg", 0, 1000, 0)
    dec_s = st.slider("Dec", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1>{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    v_nc = c1.number_input(t["n_caps"], 1)
    v_np = c2.number_input(t["n_palets"], 1)
    if st.button(t["afegeix"], use_container_width=True):
        st.session_state.llista_pesades.append({"net": round(p_brut-((v_nc*v_tc)+(v_np*v_tp)),2), "c": v_nc})
    if st.session_state.llista_pesades:
        sn = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        sc = sum(p['c'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{sn} Kg", f"{sc} C")
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            id_l = f"L-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(sn).replace('.', ','), "Cajas": int(sc), "ID_Lote": id_l, "Ref_Original": ""}
            requests.post(URL_APPS_SCRIPT, json=d)
            st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()
    st.divider()
    st.subheader(t["hui"])
    av = datetime.now().strftime("%d/%m/%Y")
    if not df_total.empty:
        df_h = df_total[(df_total['Fecha'].str.contains(av, na=False)) & (df_total['Tipo'] == 'Campo')]
        if not df_h.empty:
            for _, r in df_h.iterrows():
                c1, c2 = st.columns([4, 1])
                c1.write(f"📍 {r['Finca']} - **{r['Kg']}kg**")
                if c2.button("🗑️", key=r['ID_Lote']):
                    requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                    st.cache_data.clear(); st.rerun()
        else: st.info(t["buit"])

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
            st.metric(t["dispo"], f"{round(d_l['Kg_N'],2)} Kg")
            with st.form("v"):
                vc = st.number_input("Capses", 1, int(d_l['Cap_N']) if d_l['Cap_N']>0 else 1)
                vr = st.number_input("Kg:", value=float(round(vc*(d_l['Kg_in']/d_l['Cajas_in']),2)) if d_l['Cajas_in']>0 else 0.0)
                if st.form_submit_button(t["botó_volcar"]):
                    dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": d_l['Finca'], "Parcela": "VOLCAT", "Tipo": "Recogido", "Kg": str(vr).replace('.',','), "Cajas": int(vc), "ID_Lote": f"V-{datetime.now().strftime('%M%S')}", "Ref_Original": d_l['ID_Lote']}
                    requests.post(URL_APPS_SCRIPT, json=dv)
                    st.cache_data.clear(); st.rerun()
        else: st.warning("Buit.")