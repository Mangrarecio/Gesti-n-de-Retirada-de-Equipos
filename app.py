import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gestión Retirada De Equipos", layout="centered")

# CSS para ocultar menús de Streamlit y forzar negritas
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    p, label, .stMarkdown, .stButton {
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
def conectar_google_sheets():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Utilizamos las credenciales guardadas en Secrets
    credenciales = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    cliente = gspread.authorize(credenciales)
    # IMPORTANTE: Asegúrate de que la hoja en tu Drive se llame exactamente así
    return cliente.open("Gestión de Retirada de Equipos").sheet1

def guardar_datos(tipo, fecha, enfermero_dni, equipo, lugar, celador_dni):
    try:
        hoja = conectar_google_sheets()
        fila = [tipo, fecha.strftime("%d/%m/%Y"), enfermero_dni, equipo, lugar, celador_dni]
        hoja.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- CONTROL DE ACCESO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("Acceso Restringido")
    password = st.text_input("Introduce la clave de seguridad", type="password")
    if st.button("Acceder"):
        if password == "@1357#":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

# --- CUERPO DE LA APLICACIÓN ---
st.title("Gestión Retirada De Equipos")

tab1, tab2 = st.tabs(["🔴 RETIRADA DE EQUIPO", "🟢 ENTREGA DE EQUIPO"])

# Formulario de Retirada
with tab1:
    with st.form("form_retirada", clear_on_submit=True):
        st.markdown("### Datos de la Retirada")
        f_ret = st.date_input("Fecha de retirada")
        enf_ret = st.text_input("Nombre de enfermero y DNI")
        eq_ret = st.text_input("Equipo que se retira")
        lug_ret = st.text_input("Lugar de retirada")
        cel_ret = st.text_input("Nombre de celador y DNI")
        
        if st.form_submit_button("Registrar Movimiento"):
            if all([enf_ret, eq_ret, lug_ret, cel_ret]):
                if guardar_datos("RETIRADA", f_ret, enf_ret, eq_ret, lug_ret, cel_ret):
                    st.success("Registrado en Google Drive con éxito")
            else:
                st.warning("Completa todos los campos")

# Formulario de Entrega
with tab2:
    with st.form("form_entrega", clear_on_submit=True):
        st.markdown("### Datos de la Entrega")
        f_ent = st.date_input("Fecha de entrega")
        enf_ent = st.text_input("Nombre de enfermero y DNI")
        eq_ent = st.text_input("Equipo que se entrega")
        lug_ent = st.text_input("Lugar de entrega")
        cel_ent = st.text_input("Nombre de celador y DNI")
        
        if st.form_submit_button("Registrar Movimiento"):
            if all([enf_ent, eq_ent, lug_ent, cel_ent]):
                if guardar_datos("ENTREGA", f_ent, enf_ent, eq_ent, lug_ent, cel_ent):
                    st.success("Registrado en Google Drive con éxito")
            else:
                st.warning("Completa todos los campos")