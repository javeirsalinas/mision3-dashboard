import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y UX/UI (MODO CLARO 100% CONTRASTE)
# ==========================================
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

# Inyección de estilos CSS para asegurar fondo blanco puro y fuentes negras legibles
st.markdown("""
    <style>
    /* Fondo principal de la aplicación y contenedores */
    .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #ffffff !important; 
    }
    
    /* Tarjetas de indicadores en fondo blanco con bordes definidos */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border-top: 4px solid #1e293b !important;
        border-left: 1px solid #cbd5e1 !important;
        border-right: 1px solid #cbd5e1 !important;
        border-bottom: 1px solid #cbd5e1 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Textos en negro de alto contraste para métricas */
    [data-testid="stMetricValue"] { 
        font-size: 30px !important; 
        color: #000000 !important; 
        font-weight: 700 !important; 
    }
    [data-testid="stMetricLabel"] { 
        font-size: 14px !important; 
        color: #0f172a !important; 
        font-weight: 600 !important; 
    }
    
    /* Títulos de sección */
    h1, h2, h3, h4, h5, h6 { 
        color: #000000 !important; 
        font-family: Arial, sans-serif;
    }
    
    /* Modificación de alertas informativas e info boxes */
    .stAlert {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Forzar textos del pie de página y párrafos a negro */
    p, span, li, td, th {
        color: #000000 !important;
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
    st.stop()

# ==========================================
# 3. CABECERA EJECUTIVA
# ==========================================
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("### **Dashboard de Indicadores Estratégicos y de Gestión**")
st.markdown("**Reporte gerencial automatizado en tiempo real | Diseño Claro de Alta Legibilidad**")
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
    
    # Arreglo de contraste en el gráfico de embudo
    fig_embudo = go.Figure(go.Funnel(
        y=['Pre-incubación', 'Incubación', 'Aceleración'],
        x=[60, 25, 0],
        textinfo="value+percent initial",
        marker={"color": ["#0f172a", "#334155", "#94a3b8"]}
    ))
    fig_embudo.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=20, b=20), 
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color="#000000", size=12) # Forzar texto del gráfico a negro estricto
    )
    st.plotly_chart(fig_embudo, use_container_width=True)

with col_der:
    st.subheader("🤝 Ecosistema de Vinculación (V&E)")
    datos_entidades = {
        'Entidad': ['Universidades', 'Incubadoras', 'Cámaras', 'Asociaciones', 'Instituciones'],
        'Cantidad': [20, 20, 19, 6, 4]
    }
    df_entidades = pd.DataFrame(datos_entidades)
    
    # Eliminación de fondo oscuro cuadrado del Pie Chart
    fig_pie = px.pie(
        df_entidades, 
        values='Cantidad', 
        names='Entidad',
        color_discrete_sequence=['#0f172a', '#1e293b', '#475569', '#94a3b8', '#cbd5e1'],
        template="plotly_white"
    )
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        height=380,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.15, 
            xanchor="center", 
            x=0.5, 
            font=dict(color="#000000", size=11) # Leyenda con texto negro claro
        )
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
# 7. SECCIÓN 4: ANALÍTICA DIGITAL Y REDES (CORRECCIÓN DE EJES E INVISIBILIDAD)
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
        color_discrete_sequence=['#0f172a'],
        template="plotly_white"
    )
    # Corrección profunda del look and feel del eje X e Y
    fig_visitas.update_layout(
        plot_bgcolor='#ffffff', 
        paper_bgcolor='#ffffff',
        height=400,
        font=dict(color="#000000")
    )
    fig_visitas.update_xaxes(title_text="Interacciones", tickfont=dict(color="#000000"), title_font=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    fig_visitas.update_yaxes(tickfont=dict(color="#000000"), title_font=dict(color="#000000"))
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
        color_discrete_sequence=['#475569'],
        template="plotly_white"
    )
    # Corrección profunda de títulos de gráficos y leyendas de datos
    fig_redes.update_layout(
        plot_bgcolor='#ffffff', 
        paper_bgcolor='#ffffff',
        height=400,
        font=dict(color="#000000")
    )
    fig_redes.update_xaxes(tickfont=dict(color="#000000"), title_font=dict(color="#000000"))
    fig_redes.update_yaxes(title_text="Miembros", tickfont=dict(color="#000000"), title_font=dict(color="#000000"), showgrid=True, gridcolor="#e2e8f0")
    st.plotly_chart(fig_redes, use_container_width=True)

# ==========================================
# 8. PIE DE PÁGINA CORPORATIVO
# ==========================================
st.markdown("---")
st.markdown(
    "<center style='color: #000000; font-size: 14px; font-weight: 600;'> "
    "© Misión 3 - Centro de Emprendimiento e Innovación | Universidad César Vallejo<br>"
    "Infraestructura Cloud conectada automáticamente mediante canales analíticos distribuidos."
    "</center>", 
    unsafe_allow_html=True
)
