import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# 1. URL APPS SCRIPT
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbydcIn02OW80cs1Oua_vmCNvRLDgf1TDFRQe4Xv-efuL7_MxegZ08MgkMFh-hYrMr0H/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut de la Pesada", "n_caps": "Nº Caixes", "n_palets": "Nº Palets",
        "afegeix": "➕ AFEGIR PESADA (NETA)", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Lot de CAMP a bolcar:", "dispo": "Disponible:", "n_caps_volcar": "Caixes a bolcar?",
        "botó_volcar": "💾 EXECUTAR VOLCAT I RECOLLIDA", "hui": "📋 Registres recents (🗑️ esborrar):"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto", "n_caps": "Nº Cajas", "n_palets": "Nº Palets",
        "afegeix": "➕ AÑADIR PESADA (NETA)", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Lote de CAMPO a volcar:", "dispo": "Disponible:", "n_caps_volcar": "¿Cajas a volcar?",
        "botó_volcar": "💾 EJECUTAR VOLCADO Y RECOGIDA", "hui": "📋 Registros recientes (🗑️ borrar):"
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano"])
t = traduccions[idioma]

def data_hui():
    # Forcem la data d'Espanya (+2 hores sobre UTC)
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%d/%m/%Y")

@st.cache_data(ttl=2)
def carregar_dades():
    try:
        res = requests.get(f"{URL_APPS_SCRIPT}?cache={time.time()}")
        json_data = res.json()
        df = pd.DataFrame(json_data[1:], columns=json_data[0])
        # NETEJA DE COLUMNES I DADES
        df.columns = df.columns.str.strip()
        for col in ['Kg', 'Cajas']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        return df
    except: return pd.DataFrame()

df_total = carregar_dades()
st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# --- SECCIÓ 1: ENTRADA ---
if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    col1, col2 = st.columns(2)
    v_tc = col1.number_input(t["tara_caixa"], 0.50); v_tp = col2.number_input(t["tara_palet"], 15.0)
    
    st.markdown(f"### ⚖️ {t['brut']}")
    kg_s = st.slider("Kg", 0, 1000, 0); dec_s = st.slider("Decimals", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1>{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    v_nc = c1.number_input(t["n_caps"], 1); v_np = c2.number_input(t["n_palets"], 1)

    if st.button(t["afegeix"], use_container_width=True):
        t_n = round(p_brut - ((v_nc * v_tc) + (v_np * v_tp)), 2)
        st.session_state.llista_pesades.append({"net": t_n, "c": v_nc})

    if st.session_state.llista_pesades:
        sn = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        sc = sum(p['c'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{sn} Kg", f"{sc} Capses")
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            id_l = f"L-{int(time.time()*1000)}"
            d = {"Fecha": data_hui(), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(sn).replace('.', ','), "Cajas": int(sc), "ID_Lote": id_l, "Ref_Original": ""}
            requests.post(URL_APPS_SCRIPT, json=d)
            st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()

    st.divider()
    st.subheader(t["hui"])
    if not df_total.empty:
        for i, r in df_total.tail(10).iloc[::-1].iterrows():
            c1, c2 = st.columns([4, 1])
            data_v = str(r['Fecha']).split('T')[0]
            c1.write(f"📅 {data_v} | {r['Finca']} | **{r['Kg']}kg** ({r['Tipo']})")
            if c2.button("🗑️", key=f"del_{i}_{r['ID_Lote']}"):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                st.cache_data.clear(); st.rerun()

# --- SECCIÓ 2: VOLCAT ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty and 'Tipo' in df_total.columns:
        # Stock Cambra = Campo - Volcado
        c_df = df_total[df_total['Tipo'] == 'Campo']
        v_df = df_total[df_total['Tipo'] == 'Volcado']
        
        if not c_df.empty:
            ent = c_df.groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first'}).reset_index()
            eix = v_df.groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
            stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in','_out')).fillna(0)
            stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
            stk['Cap_N'] = stk['Cajas_in'] - stk['Cajas_out']
            dispo = stk[stk['Kg_N'] > 0.1]
            
            if not dispo.empty:
                dispo['Lab'] = dispo['ID_Lote'].str[-6:] + " | " + dispo['Finca'] + " (" + dispo['Kg_N'].astype(str) + "kg)"
                l_s = st.selectbox(t["tria_lot"], dispo['Lab'])
                d_l = dispo[dispo['Lab'] == l_s].iloc[0]
                st.metric(t["disponible"], f"{round(d_l['Kg_N'],2)} Kg", f"{int(d_l['Cap_N'])} Capses")
                
                with st.form("v"):
                    vc = st.number_input("Capses a bolcar", 1, int(d_l['Cap_N']) if d_l['Cap_N']>0 else 100)
                    mitjana = d_l['Kg_in']/d_l['Cajas_in'] if d_l['Cajas_in']>0 else 0
                    vr = st.number_input("Kg:", value=float(round(vc * mitjana, 2)))
                    if st.form_submit_button(t["botó_volcar"]):
                        # 1. Restem del Campo (Tipus Volcado)
                        dv = {"Fecha": data_hui(), "Finca": d_l['Finca'], "Parcela": "PROCESO", "Tipo": "Volcado", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"V-{int(time.time())}", "Ref_Original": d_l['ID_Lote']}
                        requests.post(URL_APPS_SCRIPT, json=dv)
                        # 2. Creem nova entrada (Tipus Recogido)
                        dr = {"Fecha": data_hui(), "Finca": d_l['Finca'], "Parcela": "NETO", "Tipo": "Recogido", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"R-{int(time.time())}", "Ref_Original": d_l['ID_Lote']}
                        requests.post(URL_APPS_SCRIPT, json=dr)
                        st.success("✅ Fet!"); st.cache_data.clear(); st.rerun()
            else: st.warning("No hi ha fruit de camp disponible.")
    else: st.info("Sense dades.")