import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Misión 3 - Dashboard Ejecutivo",
    page_icon="🏛️",
    layout="wide"
)

# --- ESTILO PROFESIONAL (CSS) ---
st.markdown("""
    <style>
    /* Fondo y tipografía */
    .main { background-color: #f4f7f9; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #002147; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 16px; color: #64748b; }
    
    /* Tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-left: 5px solid #C5A059;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Títulos */
    h1 { color: #002147; font-family: 'Georgia', serif; border-bottom: 2px solid #C5A059; padding-bottom: 10px; }
    h2 { color: #002147; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A DATOS ---
# Nota: En producción, el URL va en .streamlit/secrets.toml
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl="5m") # Se actualiza cada 5 minutos
except:
    st.error("Por favor, conecta tu Google Sheet en los secretos de Streamlit.")
    st.stop()

# --- HEADER ---
st.title("🏛️ Centro de Emprendimiento e Innovación - Misión 3")
st.markdown("**Reporte de Indicadores Clave de Gestión (KPIs) - Alta Dirección**")

# --- BLOQUE 1: ESTADO TECNOLÓGICO Y FORMACIÓN ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Comité Plataforma", "OPERATIVO", delta="✓")
with col2:
    st.metric("Calculadora Valor", "ACTIVA", delta="100%")
with col3:
    st.metric("Consultoría Inn.", "PROYECTO", delta="En curso", delta_color="normal")
with col4:
    st.metric("Curso E&I", "TRANSVERSAL", delta="Activo")

st.markdown("---")

# --- BLOQUE 2: EMBUDO DE INNOVACIÓN Y VINCULACIÓN ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🚀 Pipeline de Emprendimiento")
    # Gráfico de Embudo (Funnel)
    fig_funnel = go.Figure(go.Funnel(
        y = ["Pre-incubación", "Incubación", "Aceleración"],
        x = [60, 25, 0],
        textinfo = "value+percent initial",
        marker = {"color": ["#002147", "#1a3a5a", "#C5A059"]}
    ))
    fig_funnel.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=350)
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_right:
    st.subheader("🤝 Ecosistema (V&E)")
    # Datos de entidades
    entidades = {'Tipo': ['Univ.', 'Incub.', 'Cámaras', 'Asoc.', 'Inst.'], 'Cant': [20, 20, 19, 6, 4]}
    df_ent = pd.DataFrame(entidades)
    fig_pie = px.pie(df_ent, values='Cant', names='Tipo', 
                     color_discrete_sequence=['#002147', '#C5A059', '#475569', '#94a3b8', '#e2e8f0'])
    fig_pie.update_layout(showlegend=True, height=350, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- BLOQUE 3: IMPACTO DIGITAL Y VISITAS ---
st.markdown("---")
st.subheader("🌐 Tráfico de Plataformas y Comunidad Digital")
c1, c2 = st.columns(2)

with c1:
    visitas_data = {'Plataforma': ['ATIPAQ', 'Mentores', 'Miraflores', 'Pre-inc.', 'Incub.', 'Callao'],
                    'Pax': [243, 114, 64, 60, 25, 7]}
    df_vis = pd.DataFrame(visitas_data).sort_values('Pax')
    fig_vis = px.bar(df_vis, x='Pax', y='Plataforma', orientation='h', 
                     title="Visitas / Participantes por Canal",
                     color_discrete_sequence=['#002147'])
    st.plotly_chart(fig_vis, use_container_width=True)

with c2:
    redes_data = {'Red': ['TikTok', 'Instagram', 'Facebook', 'LinkedIn', 'YouTube'],
                  'Seguidores': [3000, 2000, 2000, 1000, 200]}
    df_redes = pd.DataFrame(redes_data)
    fig_redes = px.bar(df_redes, x='Red', y='Seguidores', 
                       title="Comunidad Digital Total",
                       color_discrete_sequence=['#C5A059'])
    st.plotly_chart(fig_redes, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2024 Misión 3 - Universidad César Vallejo | Datos actualizados desde Google Sheets")
