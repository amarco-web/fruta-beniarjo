import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. URLS
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbxwgSEzm3LBQ-ss2Ps_xuf6-MAUzSuYaKLt3WLoXfDhOW0SxWRfXbFu1JMRzxVSIQ/exec"
SHEET_ID = "1W2f64UXUzdRB2Ib-oVQH2D_hJURiQALGz_XNdUF95zE"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. ESTIL CSS (Bola gegant + número flotant)
st.markdown("""
    <style>
    .stSlider [data-baseweb="slider"] [role="slider"] {
        width: 45px !important;
        height: 45px !important;
        background-color: #5D3FD3 !important;
        border: 3px solid white !important;
    }
    div[data-testid="stThumbValue"] {
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
        background-color: #5D3FD3 !important;
        padding: 5px !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUCCIONS
traduccions = {
    "Valencià": {
        "titol": "🟣 Control Maracuia - Mirna",
        "menu_entrada": "📥 Registrar Entrada Camp",
        "menu_volcat": "🚜 Volcat / Confecció",
        "tria_lot": "Selecciona el Lot a bolcar:",
        "disponible": "Disponible actualment:",
        "n_caps_volcar": "Quantes caixes vas a bolcar?",
        "pes_calculat": "Pes net suggerit (segons mitjana):",
        "botó_volcar": "💾 REGISTRAR VOLCAT PARCIAL",
        "exit_volcat": "✅ Volcat registrat. Estoc actualitzat.",
        "hui": "📋 Entrades de hui:"
    },
    "Castellano": {
        "titol": "🟣 Control Maracuyá - Mirna",
        "menu_entrada": "📥 Registrar Entrada Campo",
        "menu_volcat": "🚜 Volcado / Confección",
        "tria_lot": "Selecciona el Lote a volcar:",
        "disponible": "Disponible actualmente:",
        "n_caps_volcar": "¿Cuántas cajas vas a volcar?",
        "pes_calculat": "Peso neto sugerido (según media):",
        "botó_volcar": "💾 REGISTRAR VOLCADO PARCIAL",
        "exit_volcat": "✅ Volcado registrado. Stock actualizado.",
        "hui": "📋 Entradas de hoy:"
    }
}

st.set_page_config(page_title="Control Maracuia", page_icon="🟣", layout="centered")

# IDIOMA
st.sidebar.title("🌍 Idioma")
idioma = st.sidebar.selectbox("", ["Valencià", "Castellano"])
t = traduccions[idioma]

st.title(t["titol"])
opcio = st.sidebar.radio("Navegació", [t["menu_entrada"], t["menu_volcat"]])

# FUNCIÓ PER CARREGAR TOTA LA BASE DE DADES
def carregar_tot():
    try:
        df = pd.read_csv(URL_CSV)
        # Convertir Kg a número (per si venen amb coma de l'Excel)
        if 'Kg' in df.columns:
            df['Kg'] = df['Kg'].astype(str).str.replace(',', '.').astype(float)
        return df
    except:
        return pd.DataFrame()

df_total = carregar_tot()

# --- SECCIÓ 1: ENTRADA DE CAMP (Mantenim el que ja teníem) ---
if opcio == t["menu_entrada"]:
    st.header(t["menu_entrada"])
    # [Aquí aniria el codi de tares i cursors que ja hem validat abans...]
    # Per estalviar espai no el repeteixo tot, però s'ha de mantenir exactament igual.
    st.info("Utilitza la secció de pesatge habitual.")

# --- SECCIÓ 2: VOLCAT AMB CONTROL D'ESTOC ---
elif opcio == t["menu_volcat"]:
    st.header(t["menu_volcat"])
    
    if not df_total.empty:
        # 1. CALCULAR ESTOC REAL PER LOT
        # Sumem entrades (Campo)
        entrades = df_total[df_total['Tipo'] == 'Campo'].groupby('ID_Lote').agg({'Kg': 'sum', 'Cajas': 'sum', 'Finca': 'first', 'Parcela': 'first'}).reset_index()
        # Sumem eixides (Recogido)
        eixides = df_total[df_total['Tipo'] == 'Recogido'].groupby('Ref_Original').agg({'Kg': 'sum', 'Cajas': 'sum'}).reset_index()
        
        # Combinem per saber el que queda
        estoc = pd.merge(entrades, eixides, left_on='ID_Lote', right_on='Ref_Original', how='left', suffixes=('_in', '_out')).fillna(0)
        estoc['Kg_Net'] = estoc['Kg_in'] - estoc['Kg_out']
        estoc['Caps_Net'] = estoc['Cajas_in'] - estoc['Cajas_out']
        
        # Filtrem lots que encara tinguen fruita (> 0.5 kg per seguretat)
        lots_disponibles = estoc[estoc['Kg_Net'] > 0.5]
        
        if not lots_disponibles.empty:
            # Creem etiqueta per al selector
            lots_disponibles['Label'] = lots_disponibles['ID_Lote'] + " | " + lots_disponibles['Finca'] + " (" + lots_disponibles['Kg_Net'].astype(str) + " kg)"
            
            lot_sel_label = st.selectbox(t["tria_lot"], lots_disponibles['Label'])
            dades_lot = lots_disponibles[lots_disponibles['Label'] == lot_sel_label].iloc[0]
            
            st.metric(t["disponible"], f"{round(dades_lot['Kg_Net'], 2)} Kg", f"{int(dades_lot['Caps_Net'])} Caixes")
            
            # Càlcul de mitjana
            mitjana_kg_capsa = dades_lot['Kg_in'] / dades_lot['Cajas_in']
            
            with st.form("form_volcat"):
                caps_a_volcar = st.number_input(t["n_caps_volcar"], min_value=1, max_value=int(dades_lot['Caps_Net']), value=1)
                
                # Suggeriment automàtic de pes
                pes_suggerit = round(caps_a_volcar * mitjana_kg_capsa, 2)
                st.write(f"💡 {t['pes_calculat']} **{pes_suggerit} Kg**")
                
                # També deixem l'opció de pes manual si volen ser exactes
                pes_real_volcat = st.number_input("Pes real del volcat (Kg):", value=float(pes_suggerit), step=0.1)
                
                if st.form_submit_button(t["botó_volcar"]):
                    dades_v = {
                        "Fecha": datetime.now().strftime("%d/%m/%Y"),
                        "Finca": dades_lot['Finca'],
                        "Parcela": dades_lot['Parcela'],
                        "Tipo": "Recogido",
                        "Kg": str(round(pes_real_volcat, 2)).replace('.', ','),
                        "Cajas": int(caps_a_volcar),
                        "ID_Lote": f"V-{datetime.now().strftime('%M%S')}",
                        "Ref_Original": dades_lot['ID_Lote']
                    }
                    try:
                        res = requests.post(URL_APPS_SCRIPT, json=dades_v)
                        if "Success" in res.text:
                            st.success(t["exit_volcat"])
                            st.balloons()
                            st.rerun()
                    except: st.error("Error")
        else:
            st.warning("No hi ha cap palet disponible per a bolcar.")
    else:
        st.info("Encara no hi ha dades al registre.")

# --- TAULA DE HUI ---
try:
    avui = datetime.now().strftime("%d/%m/%Y")
    df_hui = df_total[df_total['Fecha'] == avui]
    if not df_hui.empty:
        st.divider()
        st.subheader(t["hui"])
        st.dataframe(df_hui[['Finca', 'Parcela', 'Kg', 'Cajas', 'Tipo']].iloc[::-1], use_container_width=True)
except: pass