import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. URL DE L'APPS SCRIPT (Versió 3)
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbezps3hmJd44mDWLiaHGvDn1cvC4zqblgoYGJk1G3puGDbRu9_XP4eLGcO6FLhQvxEs/exec"

# 2. TRADUCCIONS COMPLETES
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Entrada Camp",
        "menu_volcat": "🚜 Volcat / Confecció",
        "tara_caixa": "Tara Caixa (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Pes Brut de la Pesada", "n_caps": "Nº Caixes dalt bàscula", "n_palets": "Nº Palets dalt bàscula",
        "afegeix": "➕ AFEGIR PESADA (NETA)", "net_total": "Pes Net Total Lot", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lot:", "disponible": "Disponible en cambra:",
        "n_caps_volcar": "Quantes caixes vas a bolcar?", "botó_volcar": "💾 REGISTRAR VOLCAT",
        "recomenat": "Pes net suggerit:", "hui": "📋 Entrades de hui (🗑️ per esborrar):", "exit": "✅ Registrat!"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Entrada Campo",
        "menu_volcat": "🚜 Volcado / Confección",
        "tara_caixa": "Tara Caja (kg)", "tara_palet": "Tara Palet (kg)",
        "brut": "Peso Bruto de la Pesada", "n_caps": "Nº Cajas sobre bàscula", "n_palets": "Nº Palets sobre bàscula",
        "afegeix": "➕ AÑADIR PESADA (NETA)", "net_total": "Peso Neto Total Lote", "botó_guardar": "💾 GUARDAR EN SHEET",
        "tria_lot": "Selecciona el Lote:", "disponible": "Disponible en cámara:",
        "n_caps_volcar": "¿Cuántas cajas vas a volcar?", "botó_volcar": "💾 REGISTRAR VOLCADO",
        "recomenat": "Peso neto sugerido:", "hui": "📋 Entradas de hoy (🗑️ para borrar):", "exit": "✅ ¡Hecho!"
    },
    "Română": {
        "titol": "🟣 Controlul Maracuja - Mirna",
        "menu_entrada": "📥 Intrare Câmp",
        "menu_volcat": "🚜 Răsturnare / Prelucrare",
        "tara_caixa": "Greutate Lada (kg)", "tara_palet": "Greutate Palet (kg)",
        "brut": "Greutate Brută Cântărire", "n_caps": "Nr. Lăzi pe cântar", "n_palets": "Nr. Paleți pe cântar",
        "afegeix": "➕ ADAUGĂ CÂNTĂRIRE (NETĂ)", "net_total": "Greutate Netă Totală Lot", "botó_guardar": "💾 SALVEAZĂ ÎN SHEET",
        "tria_lot": "Selectați lotul:", "disponible": "Disponibil în depozit:",
        "n_caps_volcar": "Câte lăzi răsturnați?", "botó_volcar": "💾 ÎNREGISTREAZĂ DESCĂRCAREA",
        "recomenat": "Greutate netă sugerată:", "hui": "📋 Înregistrări astăzi (🗑️ șterge):", "exit": "✅ Gata!"
    }
}

# 3. ESTIL CSS (Cursors i Visor)
st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")
st.markdown("""<style>.stSlider [data-baseweb="slider"] [role="slider"] {width: 45px; height: 45px; background-color: #5D3FD3; border: 3px solid white;} div[data-testid="stThumbValue"] {font-size: 22px !important; font-weight: bold; color: white; background-color: #5D3FD3; padding: 5px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

if 'llista_pesades' not in st.session_state: st.session_state.llista_pesades = []

st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano", "Română"])
t = traduccions[idioma]

# FUNCIÓ PER LLEGIR DADES
@st.cache_data(ttl=2)
def carregar_dades():
    try:
        response = requests.get(URL_APPS_SCRIPT)
        json_data = response.json()
        df = pd.DataFrame(json_data[1:], columns=json_data[0])
        df['Kg'] = pd.to_numeric(df['Kg'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        df['Cajas'] = pd.to_numeric(df['Cajas'], errors='coerce').fillna(0)
        return df
    except: return pd.DataFrame()

df_total = carregar_dades()

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# --- SECCIÓ 1: ENTRADA DE CAMP ---
if opcio == t["menu_entrada"]:
    fincas = {"Cooperativa": ["Eloy", "Santi", "Toni", "Neus", "Jesus"], "Tarraso": ["Alvocat", "Germana Cando", "Dalt Casa", "Casa"], "Castelló": ["Castelló", "Sagra"], "Marapego": ["Lanelate", "Murcott", "Ortanique"]}
    f_sel = st.selectbox("Finca:", list(fincas.keys()))
    p_sel = st.selectbox("Parcel·la:", fincas[f_sel])

    col_t1, col_t2 = st.columns(2)
    v_tara_c = col_t1.number_input(t["tara_caixa"], value=0.50, step=0.01)
    v_tara_p = col_t2.number_input(t["tara_palet"], value=15.0, step=0.5)

    st.markdown(f"### ⚖️ {t['brut']}")
    kg_s = st.slider("Kg", 0, 1000, 0, step=1)
    dec_s = st.slider("Decimals", 0, 99, 0, step=1)
    p_brut = float(f"{kg_s}.{dec_s:02d}")
    st.markdown(f"""<div style="background-color:#f0f2f6;padding:15px;border-radius:15px;text-align:center;border:3px solid #5D3FD3;"><h1 style="color:#5D3FD3;margin:0;">{kg_s},{dec_s:02d} Kg</h1></div>""", unsafe_allow_html=True)

    c_q1, c_q2 = st.columns(2)
    v_n_c = c_q1.number_input(t["n_caps"], value=1, min_value=0)
    v_n_p = c_q2.number_input(t["n_palets"], value=1, min_value=0)

    if st.button(t["afegeix"], type="secondary", use_container_width=True):
        t_net = round(p_brut - ((v_n_c * v_tara_c) + (v_n_p * v_tara_p)), 2)
        st.session_state.llista_pesades.append({"net": t_net, "caixes": v_n_c})

    if st.session_state.llista_pesades:
        t_net_t = round(sum(p['net'] for p in st.session_state.llista_pesades), 2)
        t_caps_t = sum(p['caixes'] for p in st.session_state.llista_pesades)
        st.metric(t["net_total"], f"{t_net_t} Kg", f"{t_caps_t} Capses")
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("🗑️ RESET"): st.session_state.llista_pesades = []; st.rerun()
        if col_b2.button(t["botó_guardar"], type="primary"):
            id_l = f"{datetime.now().strftime('%Y%m%d')}-{f_sel[:3].upper()}-{p_sel[:3].upper()}-{datetime.now().strftime('%H%M%S')}"
            d = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": f_sel, "Parcela": p_sel, "Tipo": "Campo", "Kg": str(t_net_t).replace('.', ','), "Cajas": int(t_caps_t), "ID_Lote": id_l, "Ref_Original": ""}
            if "Success" in requests.post(URL_APPS_SCRIPT, json=d).text:
                st.success(t["exit"]); st.session_state.llista_pesades = []; st.cache_data.clear(); st.rerun()

    # --- LLISTAT DE HUI PER A CORREGIR ---
    st.divider()
    st.subheader(t["hui"])
    avui = datetime.now().strftime("%d/%m/%Y")
    if not df_total.empty:
        df_hui = df_total[(df_total['Fecha'] == avui) & (df_total['Tipo'] == 'Campo')]
        for _, row in df_hui.iterrows():
            c1, c2 = st.columns([4, 1])
            c1.write(f"📍 {row['Finca']} ({row['Parcela']}) - **{row['Kg']}kg**")
            if c2.button("🗑️", key=row['ID_Lote']):
                requests.post(URL_APPS_SCRIPT, json={"action": "delete", "id_lote": row['ID_Lote']})
                st.cache_data.clear(); st.rerun()

# --- SECCIÓ 2: VOLCAT ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    if not df_total.empty:
        ent = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg': 'sum', 'Cajas': 'sum', 'Finca': 'first', 'Parcela': 'first'}).reset_index()
        eix = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg': 'sum', 'Cajas': 'sum'}).reset_index()
        stk = pd.merge(ent, eix, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in', '_out')).fillna(0)
        stk['Kg_N'] = stk['Kg_in'] - stk['Kg_out']
        stk['Cap_N'] = stk['Cajas_in'] - stk['Cajas_out']
        dispo = stk[stk['Kg_N'] > 0.1]
        if not dispo.empty:
            dispo['Lab'] = dispo['ID_Lote'].str[:8] + " | " + dispo['Finca'] + " (" + dispo['Kg_N'].round(1).astype(str) + "kg)"
            l_sel = st.selectbox(t["tria_lot"], dispo['Lab'])
            d_l = dispo[dispo['Lab'] == l_sel].iloc[0]
            st.metric(t["disponible"], f"{round(d_l['Kg_N'], 2)} Kg", f"{int(d_l['Cap_N'])} Capses")
            with st.form("f_v"):
                v_c = st.number_input(t["n_caps_volcar"], min_value=1, max_value=int(d_l['Cap_N']) if d_l['Cap_N'] > 0 else 1, value=1)
                v_p = round(v_c * (d_l['Kg_in'] / d_l['Cajas_in']), 2) if d_l['Cajas_in'] > 0 else 0
                st.write(f"💡 {t['recomenat']} {v_p} Kg")
                v_real = st.number_input("Kg:", value=float(v_p))
                if st.form_submit_button(t["botó_volcar"]):
                    dv = {"Fecha": datetime.now().strftime("%d/%m/%Y"), "Finca": d_l['Finca'], "Parcela": d_l['Parcela'], "Tipo": "Recogido", "Kg": str(round(v_real, 2)).replace('.', ','), "Cajas": int(v_c), "ID_Lote": f"V-{datetime.now().strftime('%M%S')}", "Ref_Original": d_l['ID_Lote']}
                    if "Success" in requests.post(URL_APPS_SCRIPT, json=dv).text:
                        st.success(t["exit"]); st.cache_data.clear(); st.rerun()
        else: st.warning("Buit.")