import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y UX/UI (MODO CLARO ELEGANTE)
# ==========================================
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

# Inyección de CSS para forzar fondo blanco y letras negras/oscuras de alta legibilidad
st.markdown("""
    <style>
    /* Fondo principal de la aplicación (Blanco puro) */
    .main { 
        background-color: #ffffff !important; 
    }
    
    /* Forzar fondo blanco general en los bloques de Streamlit */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* Diseño de tarjetas KPIs (Fondo blanco brillante con bordes finos en gris) */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-top: 4px solid #0f172a !important; /* Línea superior negra/azul noche */
        border-left: 1px solid #e2e8f0 !important;
        border-right: 1px solid #e2e8f0 !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* Textos de los KPIs en Negro y Gris Oscuro de alto contraste */
    [data-testid="stMetricValue"] { 
        font-size: 30px !important; 
        color: #000000 !important; /* Letras negras para el valor principal */
        font-weight: 700 !important; 
    }
    [data-testid="stMetricLabel"] { 
        font-size: 14px !important; 
        color: #334155 !important; /* Gris oscuro para las etiquetas */
        font-weight: 600 !important; 
    }
    
    /* Configuración de títulos principales en Negro */
    h1 { 
        color: #000000 !important; 
        font-family: 'Helvetica Neue', Arial, sans-serif; 
        font-weight: 700; 
    }
    h2, h3 { 
        color: #0f172a !important; 
        font-family: Arial, sans-serif; 
        font-weight: 600; 
    }
    
    /* Forzar todos los textos secundarios y tablas a color negro/gris legible */
    p, span, li, td, th {
        color: #000000 !important;
    }
    
    /* Ajuste para las tablas nativas de Streamlit en fondo claro */
    .stTable {
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CONEXIÓN BLINDADA A GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl="5m")
def cargar_datos():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    return conn.read(spreadsheet=url_directa)

try:
    df = cargar_datos()
except Exception as e:
    st.error("⚠️ Error de conexión con Google Sheets")
    st.info("""
    **Por favor verifica lo siguiente:**
    1. Que tu Google Sheet siga en modo **"Cualquier persona con el enlace puede leer"**.
    2. Que la primera pestaña de la izquierda tenga tus datos correctamente organizados.
    """)
    st.exception(e)
    st.stop()

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.caption("Reporte gerencial automatizado en tiempo real | Diseño Claro de Alta Legibilidad")
st.markdown("---")

# ==========================================
# 4. SECCIÓN 1: ESTADO OPERATIVO DE PLATAFORMAS
# ==========================================
st.subheader("🏢 Estado de la Unidad y Plataformas")
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)

with col_p1:
    st.metric(label="Comité Plataforma", value="Funcionando", delta="✓ Activo", delta_color="normal")
with col_p2:
    st.metric(label="Dashboard Plataforma", value="Funcionando", delta="✓ Activo", delta_color="normal")
with col_p3:
    st.metric(label="Calculadora Valor", value="Funcionando", delta="✓ Activa", delta_color="normal")
with col_p4:
    st.metric(label="Consultoría Innovación", value="Proyecto", delta="En Diseño", delta_color="off")
with col_p5:
    st.metric(label="Curso E&I Transversal", value="Proyecto", delta="En Diseño", delta_color="off")

st.markdown("---")

# ==========================================
# 5. SECCIÓN 2: PIPELINE DE EMPRENDIMIENTO Y VINCULACIÓN
# ==========================================
col_izq, col_der = st.columns([1.2, 1])

with col_izq:
    st.subheader("🚀 Embudo del Emprendedor (E&I)")
    # Gráfico de Embudo adaptado al fondo claro con escala de grises y azul elegante
    fig_embudo = go.Figure(go.Funnel(
        y=['Pre-incubación', 'Incubación', 'Aceleración'],
        x=[60, 25, 0],
        textinfo="value+percent initial",
        marker={"color": ["#0f172a", "#334155", "#64748b"]} # Negro azulado, Gris Oscuro, Gris Medio
    ))
    fig_embudo.update_layout(
        template="plotly_white", # Fuerza el fondo interno de la gráfica a blanco
        margin=dict(l=20, r=20, t=20, b=20), 
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#000000") # Letras de los ejes en negro
    )
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    datos_entidades = {
        'Entidad': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
        'Cantidad': [20, 20, 19, 6, 4]
    }
    df_entidades = pd.DataFrame(datos_entidades)
    
    # Gráfico de tarta en tonos de contraste profesional
    fig_pie = px.pie(
        df_entidades, 
        values='Cantidad', 
        names='Entidad',
        color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
        template="plotly_white"
    )
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(color="#000000"))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ==========================================
# 6. SECCIÓN 3: RETOS, EVENTOS Y MENTORES
# ==========================================
col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.subheader("🎯 Innovación Abierta y Retos")
    st.info("**Retos Territoriales Activos:**\n* Miraflores\n* Callao Tech")
    st.metric(label="Innovación Abierta EU (Participantes)", value="1")
    st.metric(label="Polinización (Participantes)", value="1")

with col_r2:
    st.subheader("📅 Eventos Internacionales EULAC")
    datos_eventos = {
        'Sede / Evento': ['EULAC LIMA', 'EULAC CIX', 'EULAC AQP'],
        'Aforo Alcanzado': ['120 Pax', '120 Pax', '120 Pax']
    }
    st.table(pd.DataFrame(datos_eventos))

with col_r3:
    st.subheader("🧠 Capital Intelectual")
    st.metric(label="Red Global de Mentores", value="120 Profesionales", delta="Estrategas", delta_color="normal")
    st.caption("Mentores asignados para el soporte de proyectos de base científica y tecnológica.")

st.markdown("---")

# ==========================================
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES
# ==========================================
st.subheader("🌐 Visitas a Plataformas vs. Comunidad Digital")
col_v1, col_v2 = st.columns(2)

with col_v1:
    datos_visitas = {
        'Canal / Plataforma': ['ATIPAQ', 'Mentores', 'Miraflores', 'Pre-incubación', 'Incubación', 'Callao Tech'],
        'Interacciones': [243, 114, 64, 60, 25, 7]
    }
    df_visitas = pd.DataFrame(datos_visitas).sort_values(by='Interacciones')
    
    fig_visitas = px.bar(
        df_visitas, 
        x='Interacciones', 
        y='Canal / Plataforma', 
        orientation='h',
        title='Volumen de Tráfico y Participación por Canal',
        color_discrete_sequence=['#0f172a'], # Barra en Negro Corporativo
        template="plotly_white"
    )
    fig_visitas.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        height=380,
        font=dict(color="#000000")
    )
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    datos_redes = {
        'Red Social': ['TikTok', 'Instagram', 'Facebook', 'LinkedIn', 'YouTube'],
        'Miembros': [3000, 2000, 2000, 1000, 200]
    }
    df_redes = pd.DataFrame(datos_redes)
    
    fig_redes = px.bar(
        df_redes,
        x='Red Social',
        y='Miembros',
        title='Seguidores Totales en Canales Digitales',
        color_discrete_sequence=['#475569'], # Gris Oscuro
        template="plotly_white"
    )
    fig_redes.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        height=380,
        font=dict(color="#000000")
    )
    st.plotly_chart(fig_redes, use_container_width=True)

# ==========================================
# 8. PIE DE PÁGINA
# ==========================================
st.markdown("---")
st.markdown(
    "<center style='color: #000000; font-size: 14px; font-weight: 500;'> "
    "© Misión 3 - Centro de Emprendimiento e Innovación | Universidad César Vallejo<br>"
    "Infraestructura Cloud conectada automáticamente mediante canales analíticos distribuidos."
    "</center>", 
    unsafe_allow_html=True
)
