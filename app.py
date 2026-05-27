import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y UX/UI
# ==========================================
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

# Estilo CSS avanzado para la paleta institucional (Azul Marino y Oro)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { font-size: 32px; color: #002147; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 15px; color: #475569; font-weight: 500; }
    
    /* Diseño de tarjetas KPIs estilo gerencial */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-top: 4px solid #C5A059;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    h1 { color: #002147; font-family: 'Georgia', serif; font-weight: 700; }
    h2, h3 { color: #002147; font-family: 'Sans-serif'; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CONEXIÓN BLINDADA A GOOGLE SHEETS
# ==========================================
@st.cache_data(ttl="5m")
def cargar_datos():
    # Inicializa la conexión
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # URL directa de tu Google Sheet
    url_directa = "https://docs.google.com/spreadsheets/d/1aEIyDmHuHxzei8IRqMFKYDIZ1Hc3lvQoU6odzyuiL9M/edit?usp=sharing"
    
    # Leemos la primera pestaña disponible automáticamente para evitar el Error 400
    return conn.read(spreadsheet=url_directa)

try:
    df = cargar_datos()
except Exception as e:
    st.error("⚠️ Error de conexión con Google Sheets")
    st.info("""
    **Por favor verifica lo siguiente:**
    1. Que tu Google Sheet siga configurado en modo **"Cualquier persona con el enlace puede leer"** (botón azul Compartir).
    2. Que la primera pestaña (la que está más a la izquierda abajo) tenga los datos bien estructurados.
    """)
    st.exception(e)
    st.stop()

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.caption("Reporte automatizado en tiempo real dirigido a la Alta Dirección Universitaria")
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
    # Gráfico de Embudo
    fig_embudo = go.Figure(go.Funnel(
        y=['Pre-incubación', 'Incubación', 'Aceleración'],
        x=[60, 25, 0],
        textinfo="value+percent initial",
        marker={"color": ["#002147", "#1e3a60", "#C5A059"]}
    ))
    fig_embudo.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    # Datos de entidades aliadas
    datos_entidades = {
        'Entidad': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
        'Cantidad': [20, 20, 19, 6, 4]
    }
    df_entidades = pd.DataFrame(datos_entidades)
    
    fig_pie = px.pie(
        df_entidades, 
        values='Cantidad', 
        names='Entidad',
        color_discrete_sequence=['#002147', '#C5A059', '#334155', '#64748b', '#cbd5e1']
    )
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
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
    # Tráfico de los canales del centro
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
        color_discrete_sequence=['#002147']
    )
    fig_visitas.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=380)
    st.plotly_chart(fig_visitas, use_container_width=True)

with col_v2:
    # Métricas de redes sociales
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
        color_discrete_sequence=['#C5A059']
    )
    fig_redes.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=380)
    st.plotly_chart(fig_redes, use_container_width=True)

# ==========================================
# 8. PIE DE PÁGINA
# ==========================================
st.markdown("---")
st.markdown(
    "<center style='color: #64748b; font-size: 14px;'>"
    "© Misión 3 - Centro de Emprendimiento e Innovación | Universidad César Vallejo<br>"
    "Infraestructura Cloud conectada automáticamente mediante canales analíticos distribuidos."
    "</center>", 
    unsafe_allow_html=True
)
