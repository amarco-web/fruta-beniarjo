import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URL APPS SCRIPT (VERSIÓ 5)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyryYeSXGhmhCsmve6wNv7yn_mrRKvRaD2bdweUdwmTGzQgWChRBjctkB1mI-hGR2w7/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut Pesada", "n_caps": "Nº Caixes dalt bàscula", "n_palets": "Nº Palets dalt bàscula",
        "afegeix": "➕ AFEGIR PESADA (NETA)", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot:", "dispo": "Disponible en cambra:", "n_caps_volcar": "Caixes a bolcar:",
        "botó_volcar": "💾 REGISTRAR VOLCAT", "hui": "📋 Registre de hui (🗑️ per esborrar):", "exit": "✅ Fet!"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto Pesada", "n_caps": "Nº Cajas sobre báscula", "n_palets": "Nº Palets sobre báscula",
        "afegeix": "➕ AÑADIR PESADA (NETA)", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote:", "dispo": "Disponible en cámara:", "n_caps_volcar": "¿Cuántas cajas vas a volcar?",
        "botó_volcar": "💾 REGISTRAR VOLCADO", "hui": "📋 Registro de hoy (🗑️ para borrar):", "exit": "✅ ¡Hecho!"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp", "menu_volcat": "🚜 Răsturnare / Prelucrare",
        "tara_caixa": "Lada (kg)", "tara_palet": "Palet (kg)",
        "brut": "Greutate Brută", "n_caps": "Nr. Lăzi pe cântar", "n_palets": "Nr. Paleți pe cântar",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE (NETĂ)", "net_total": "Greutate Netă Totală Lot", "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "tria_lot": "Selectați lotul:", "dispo": "Disponibil:", "n_caps_volcar": "Câte lăzi răsturnați?",
        "botó_volcar": "💾 ÎNREGISTREAZĂ DESCĂRCAREA", "hui": "📋 Înregistrări astăzi (🗑️ șterge):", "exit": "✅ Gata!"
    }
}

# 3. CONFIGURACIÓ I ESTILS
st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width: 45px; height: 45px; background-color: #5D3FD3; border: 3px solid white;} div[data-testid="stThumbValue"] {font-size: 20px !important; font-weight: bold; color: white; background-color: #5D3FD3; padding: 5px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

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
opcio = st.sidebar.radio("Nav", [t["menu_entrada"], t["menu_volcat"]])

if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    st.markdown(f"#### ⚙️ 1. Tares")
    col1, col2 = st.columns(2)
    v_tc = col1.number_input(t["tara_caixa"], 0.50)
    v_tp = col2.number_input(t["tara_palet"], 15.0)

    st.markdown(f"### ⚖️ 2. {t['brut']}")
    kg_s = st.slider("Kg", 0, 1000, 0)
    dec_s = st.slider("Dec", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1>{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    st.markdown(f"#### 📦 3. Quantitats")
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
        av = datetime.now().strftime("%d/%m/%Y")
        df_h = df_total[(df_total['Fecha'].astype(str).str.contains(av)) & (df_total['Tipo'] == 'Campo')]
        for _, r in df_h.iterrows():
            c1, c2 = st.columns([4, 1])
            c1.write(f"📍 {r['Finca']} ({r['Parcela']}) - **{r['Kg']}kg**")
            if c2.button("🗑️", key=r['ID_Lote']):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                st.cache_data.clear(); st.rerun()

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
                vc = st.number_input(t["n_caps_volcar"], 1, int(d_l['Cap_N']) if d_l['Cap_N']>0 else 1)
                vr = st.number_input("Kg reals:", value=float(round(vc*(d_l['Kg_in']/d_l['Cajas_in']),2)) if d_l['Cajas_in']>0 else 0.0)
                if st.form_submit_button(t["botó_volcar"]):
                    dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": d_l['Finca'], "Parcela": "VOLCAT", "Tipo": "Recogido", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"V-{datetime.now().strftime('%M%S')}", "Ref_Original": d_l['ID_Lote']}
                    requests.post(URL_APPS_SCRIPT, json=dv)
                    st.cache_data.clear(); st.rerun()