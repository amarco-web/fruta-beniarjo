import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. LA TEUA URL (VERSIÓ 5 O SUPERIOR)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyryYeSXGhmhCsmve6wNv7yn_mrRKvRaD2bdweUdwmTGzQgWChRBjctkB1mI-hGR2w7/exec"

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {"titol": "🟣 Control Maracuia", "menu_entrada": "📥 Entrada", "menu_volcat": "🚜 Volcat", "hui": "📋 Entrades de hui:", "buit": "No hi ha dades hui.", "dispo": "Disponible:"},
    "Castellano": {"titol": "🟣 Control Maracuyá", "menu_entrada": "📥 Entrada", "menu_volcat": "🚜 Volcado", "hui": "📋 Entradas de hoy:", "buit": "No hay datos hoy.", "dispo": "Disponible:"},
    "Română": {"titol": "🟣 Control Maracuja", "menu_entrada": "📥 Intrare", "menu_volcat": "🚜 Răsturnare", "hui": "📋 Înregistrări astăzi:", "buit": "Nicio dată astăzi.", "dispo": "Disponibil:"}
}

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

# 3. LECTURA INSTANTÀNIA (SENSE CSV)
@st.cache_data(ttl=1) # Actualitza cada segon
def carregar_dades_reals():
    try:
        res = requests.get(URL_APPS_SCRIPT)
        json_data = res.json()
        df = pd.DataFrame(json_data[1:], columns=json_data[0])
        df['Kg'] = pd.to_numeric(df['Kg'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        df['Cajas'] = pd.to_numeric(df['Cajas'], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Fecha", "Finca", "Parcela", "Tipo", "Kg", "Cajas", "ID_Lote", "Ref_Original"])

df_total = carregar_dades_reals()

st.title(t["titol"])
opcion = st.sidebar.radio("Menu", [t["menu_entrada"], t["menu_volcat"]])

if opcion == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])
    
    kg_s = st.slider("Kg", 0, 1000, 0)
    dec_s = st.slider("Dec", 0, 99, 0)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"<div style='background-color:#f0f2f6;padding:10px;border-radius:10px;text-align:center;'><h1>{kg_s},{dec_s:02d} Kg</h1></div>", unsafe_allow_html=True)
    
    if st.button("💾 GUARDAR ENTRADA", type="primary", use_container_width=True):
        id_l = f"L-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(p_brut).replace('.', ','), "Cajas": 1, "ID_Lote": id_l, "Ref_Original": ""}
        requests.post(URL_APPS_SCRIPT, json=d)
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.subheader(t["hui"])
    avui = datetime.now().strftime("%d/%m/%Y")
    if not df_total.empty:
        df_hui = df_total[(df_total['Fecha'].astype(str).str.contains(avui)) & (df_total['Tipo'] == 'Campo')]
        if not df_hui.empty:
            for _, r in df_hui.iterrows():
                c1, c2 = st.columns([4, 1])
                c1.write(f"📍 {r['Finca']} - {r['Kg']}kg")
                if c2.button("🗑️", key=r['ID_Lote']):
                    requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": r['ID_Lote']})
                    st.cache_data.clear(); st.rerun()
        else: st.info(t["buit"])

elif opcion == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in','_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        dispo = stk[stk['Kg_N'] > 0.1]
        if not dispo.empty:
            l_sel = st.selectbox("Lot:", dispo['ID_Lote'] + " | " + dispo['Finca'])
            lot_id = l_sel.split(" | ")[0]
            kg_queden = dispo[dispo['ID_Lote'] == lot_id]['Kg_N'].values[0]
            st.metric(t["dispo"], f"{round(kg_queden,2)} Kg")
            v_kg = st.number_input("Kg a bolcar:", 0.0, float(kg_queden))
            if st.button("💾 REGISTRAR VOLCAT"):
                d_v = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": "Volcat", "Parcela": "Volcat", "Tipo": "Recogido", "Kg": str(v_kg).replace('.',','), "Cajas": 0, "ID_Lote": f"V-{datetime.now().strftime('%M%S')}", "Ref_Original": lot_id}
                requests.post(URL_APPS_SCRIPT, json=d_v)
                st.cache_data.clear(); st.rerun()
        else: st.warning("No hi ha estoc.")