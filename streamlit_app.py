import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# 1. URL DE L'APPS SCRIPT (Versió 5)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyryYeSXGhmhCsmve6wNv7yn_mrRKvRaD2bdweUdwmTGzQgWChRBjctkB1mI-hGR2w7/exec"

# 2. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp", "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut", "n_caps": "Nº Caixes", "n_palets": "Nº Palets",
        "afegeix": "➕ AFEGIR PESADA", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot:", "dispo": "Disponible:", "n_caps_volcar": "Caixes a bolcar:",
        "botó_volcar": "💾 REGISTRAR VOLCAT", "hui": "📋 Entrades de hui (🗑️ per esborrar):", "exit": "✅ Registrat!",
        "buit": "Encara no hi ha registres hui."
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo", "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto", "n_caps": "Nº Cajas", "n_palets": "Nº Palets",
        "afegeix": "➕ AÑADIR PESADA", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote:", "dispo": "Disponible:", "n_caps_volcar": "Cajas a volcar:",
        "botó_volcar": "💾 REGISTRAR VOLCADO", "hui": "📋 Entradas de hoy (🗑️ para borrar):", "exit": "✅ ¡Hecho!",
        "buit": "No hay registros hoy."
    },
    "Română": {
        "titol": "🟣 Control Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp", "menu_volcat": "🚜 Răsturnare / Prelucrare",
        "tara_caixa": "Greutate Lada (kg)", "tara_palet": "Greutate Palet (kg)",
        "brut": "Greutate Brută", "n_caps": "Nr. Lăzi", "n_palets": "Nr. Paleți",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE", "net_total": "Greutate Netă Totală Lot", "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "tria_lot": "Selectați lotul:", "dispo": "Disponibil:", "n_caps_volcar": "Câte lăzi?",
        "botó_volcar": "💾 ÎNREGISTREAZĂ DESCĂRCAREA", "hui": "📋 Înregistrări astăzi (🗑️ șterge):", "exit": "✅ Gata!",
        "buit": "Nicio înregistrare astăzi."
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# ESTIL CURSOR
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width: 45px; height: 45px; background-color: #5D3FD3; border: 3px solid white;} div[data-testid="stThumbValue"] {font-size: 20px !important; font-weight: bold; color: white; background-color: #5D3FD3; padding: 5px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

# LLEGIR DADES
@st.cache_data(ttl=2)
def carregar_dades():
    try:
        res = requests.get(f"{URL_APPS_SCRIPT}?t={time.time()}")
        json_data = res.json()
        df = pd.DataFrame(json_data[1:], columns=json_data[0])
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

    col1, col2 = st.columns(2)
    v_tara_c = col1.number_input(t["tara_caixa"], value=0.50)
    v_tara_p = col2.number_input(t["tara_palet"], value=15.0)

    kg_s = st.slider("Kg", 0, 1000, 0, step=1)
    dec_s = st.slider("Decimals", 0, 99, 0, step=1)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1 style="color:#5D3FD3;margin:0;">{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    v_n_c = c1.number_input(t["n_caps"], value=1, min_value=0)
    v_n_p = c2.number_input(t["n_palets"], value=1, min_value=0)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        t_net = round(p_brut - ((v_n_c * v_tara_c) + (v_n_p * v_tara_p)), 2)
        st.session_state.llista_pesades.append({"net": t_net, "caixes": v_n_c})

    if st.session_state.llista_pesades:
        s_n = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        s_c = sum(p['caixes'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{s_n} Kg Net", f"{s_c} Capses")
        if st.button(t["botó_guardar"], type="primary", use_container_width=True):
            id_l = f"L-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(s_n).replace('.', ','), "Cajas": int(s_c), "ID_Lote": id_l, "Ref_Original": ""}
            requests.post(URL_APPS_SCRIPT, json=d)
            st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()

    # --- LLISTAT DE HUI PER A CORREGIR ---
    st.divider()
    st.subheader(t["hui"])
    avui = datetime.now().strftime("%d/%m/%Y")
    
    if not df_total.empty:
        # Filtrem assegurant que la data siga text i coincidisca
        df_hui = df_total[(df_total['Fecha'].astype(str).str.contains(avui)) & (df_total['Tipo'] == 'Campo')]
        
        if not df_hui.empty:
            for _, row in df_hui.iterrows():
                c1, c2 = st.columns([4, 1])
                c1.write(f"📍 {row['Finca']} ({row['Parcela']}) - **{row['Kg']}kg**")
                if c2.button("🗑️", key=row['ID_Lote']):
                    requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": row['ID_Lote']})
                    st.cache_data.clear(); st.rerun()
        else:
            st.info(t["buit"])

elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg':'sum','Cajas':'sum','Finca':'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg':'sum','Cajas':'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in','_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        stk['Cap_N'] = stk['Cajas_in'] - stk['Cajas_out']
        dispo = stk[stk['Kg_N'] > 0.1]
        if not dispo.empty:
            dispo['Lab'] = dispo['ID_Lote'].str[-6:] + " | " + dispo['Finca'] + " (" + dispo['Kg_N'].round(1).astype(str) + "k