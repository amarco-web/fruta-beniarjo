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
        "brut": "Pes Brut de la Pesada", "afegeix": "➕ AFEGIR PESADA (NETA)",
        "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot de CAMP a bolcar:", "dispo": "Disponible en cambra:",
        "n_caps_volcar": "Quantes caixes vas a bolcar?", "botó_volcar": "💾 EXECUTAR VOLCAT I RECOLLIDA",
        "hui": "📋 Registres recents (🗑️ per esborrar):"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "brut": "Peso Bruto de la Pesada", "afegeix": "➕ AÑADIR PESADA (NETA)",
        "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote de CAMPO a volcar:", "dispo": "Disponible en cámara:",
        "n_caps_volcar": "¿Cuántas cajas vas a volcar?", "botó_volcar": "💾 EJECUTAR VOLCADO Y RECOGIDA",
        "hui": "📋 Registros recientes (🗑️ para borrar):"
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano"])
t = traduccions[idioma]

# FUNCIÓ PER OBTINDRE LA DATA CORRECTA (Forçar hora local Espanya aproximada)
def data_hui():
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%d/%m/%Y")

# LLEGIR DADES
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
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# --- SECCIÓ 1: ENTRADA ---
if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    # [Codi de cursors i tares...]
    kg_s = st.slider("Kg", 0, 1000, 0); dec_s = st.slider("Decimals", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    v_tc = st.number_input("Tara Caixa", 0.50); v_tp = st.number_input("Tara Palet", 15.0)
    v_nc = st.number_input("Nº Caixes", 1); v_np = st.number_input("Nº Palets", 1)

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
            c1.write(f"📅 {r['Fecha']} | {r['Finca']} | **{r['Kg']}kg** ({r['Tipo']})")
            if c2.button("🗑️", key=f"del_{i}_{r['ID_Lote']}"):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                st.cache_data.clear(); st.rerun()

# --- SECCIÓ 2: VOLCAT (CORREGIT) ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        # Stock de cambra = Campo - Volcado
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first','Parcela':'first'}).reset_index()
        # Molt important: Ara restem els que posa "Volcado"
        eix = df_total[df_total['Tipo'] == 'Volcado'].groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
        
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
                vr = st.number_input("Kg totals del bolcat:", value=float(round(vc * mitjana, 2)))
                
                if st.form_submit_button(t["botó_volcar"]):
                    # 1. Creem fila de VOLCADO (per a restar stock de la cambra)
                    d_volcat = {"Fecha": data_hui(), "Finca": d_l['Finca'], "Parcela": d_l['Parcela'], "Tipo": "Volcado", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"VOL-{int(time.time())}", "Ref_Original": d_l['ID_Lote']}
                    requests.post(URL_APPS_SCRIPT, json=d_volcat)
                    
                    # 2. Creem fila de RECOGIDO (nova entrada de fruita neta amb origen)
                    d_recollit = {"Fecha": data_hui(), "Finca": d_l['Finca'], "Parcela": d_l['Parcela'], "Tipo": "Recogido", "Kg": str(round(vr,2)).replace('.',','), "Cajas": int(vc), "ID_Lote": f"REC-{int(time.time())}", "Ref_Original": d_l['ID_Lote']}
                    requests.post(URL_APPS_SCRIPT, json=d_recollit)
                    
                    st.success("✅ Bolcat i Recollida registrats!")
                    st.cache_data.clear(); st.rerun()
        else: st.warning("No hi ha fruita de camp a la cambra.")