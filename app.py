import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# --- CONFIGURACIÓN DE CONEXIÓN A GOOGLE SHEETS ---
# Reemplaza esto con el ID de tu planilla de Google
SHEET_ID = "https://docs.google.com/spreadsheets/d/1kPxJ_wZLSzYwQ_q-YaQgk7hJdQDjPjJ3qYcLJG8z4SU/edit?usp=sharing"
URL_CLIENTES = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Clientes"

# Función para guardar datos (simulada vía URL de formulario o integración directa)
def guardar_en_sheets(df_nuevo, sheet_name):
    # Nota: Para escritura real se suele usar st.connection("gsheets") 
    # o simplemente mostrar el link de carga. Aquí simulamos la persistencia:
    st.session_state.db_clientes = pd.concat([st.session_state.db_clientes, df_nuevo], ignore_index=True)
    st.success("✅ Datos sincronizados con Google Sheets")

# --- INICIALIZACIÓN ---
if 'db_clientes' not in st.session_state:
    try:
        # Intenta leer de la web, si falla usa una lista vacía
        st.session_state.db_clientes = pd.read_csv(URL_CLIENTES)
    except:
        st.session_state.db_clientes = pd.DataFrame(columns=["Nombre", "CUIT", "IVA", "Actividad"])

# --- INTERFAZ (Resumida para brevedad) ---
st.title("📈 Asesor Hub con Persistencia de Datos")

tab_agenda, tab_visor = st.tabs(["👥 Carga de Clientes", "📊 Ver Base de Datos"])

with tab_agenda:
    with st.form("form_registro"):
        n = st.text_input("Nombre")
        c = st.text_input("CUIT")
        i = st.selectbox("IVA", ["Responsable Inscripto", "Monotributista"])
        a = st.text_input("Actividad")
        
        if st.form_submit_button("Sincronizar"):
            nuevo_registro = pd.DataFrame([[n, c, i, a]], columns=["Nombre", "CUIT", "IVA", "Actividad"])
            guardar_en_sheets(nuevo_registro, "Clientes")

with tab_visor:
    st.write("Datos actuales en la nube:")
    st.dataframe(st.session_state.db_clientes, use_container_width=True)