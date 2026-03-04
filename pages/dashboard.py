import streamlit as st
from config import get_supabase
import pandas as pd
import plotly.graph_objects as go

def card_metrica(titulo, valor, icono, color):
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}44);
            border-left: 4px solid {color};
            border-radius: 12px;
            padding: 20px;
            margin: 5px 0;
        ">
            <div style="font-size: 2rem;">{icono}</div>
            <div style="color: #aaa; font-size: 0.85rem; margin-top: 5px;">{titulo}</div>
            <div style="color: white; font-size: 1.8rem; font-weight: bold;">{valor}</div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_dashboard():
    st.markdown("""
        <h1 style="
            background: linear-gradient(90deg, #C6FF00, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: bold;
        ">🔥 HellYeah Agency — Panel de Control</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    sb = get_supabase()

    total_clientes = len(sb.table("clientes").select("id").execute().data)
    total_proyectos = len(sb.table("proyectos").select("id").execute().data)
    proyectos_activos = len(sb.table("proyectos").select("id").eq("estado", "En Proceso").execute().data)
    tareas_pendientes = len(sb.table("tareas").select("id").neq("estado", "Completada").execute().data)
    tareas_completadas = len(sb.table("tareas").select("id").eq("estado", "Completada").execute().data)

    pagos_cobrados = sb.table("pagos").select("monto").eq("estado", "Pagado").execute().data
    total_cobrado = sum([p["monto"] for p in pagos_cobrados]) if pagos_cobrados else 0

    pagos_pendientes = sb.table("pagos").select("monto").eq("estado", "Pendiente").execute().data
    total_pendiente = sum([p["monto"] for p in pagos_pendientes]) if pagos_pendientes else 0

    pagos_vencidos = sb.table("pagos").select("monto").eq("estado", "Vencido").execute().data
    total_vencido = sum([p["monto"] for p in pagos_vencidos]) if pagos_vencidos else 0

    st.markdown("### 📌 Resumen General")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Clientes totales", total_clientes, "👥", "#4ECDC4")
    with col2:
        card_metrica("Total Proyectos", total_proyectos, "📁", "#4A90D9")
    with col3:
        card_metrica("Proyectos Activos", proyectos_activos, "🔄", "#C6FF00")
    with col4:
        card_metrica("Tareas Pendientes", tareas_pendientes, "⚡", "#FF6B6B")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💰 Resumen Financiero")
    col1, col2, col3 = st.columns(3)
    with col1:
        card_metrica("Total Cobrado", f"${total_cobrado:,.2f}", "💵", "#2ECC71")
    with col2:
        card_metrica("Por Cobrar", f"${total_pendiente:,.2f}", "⏳", "#F39C12")
    with col3:
        card_metrica("Vencido", f"${total_vencido:,.2f}", "🚨", "#E74C3C")

    st.markdown("---")
    st.markdown("### 📊 Estado de Proyectos")

    proyectos_data = sb.table("proyectos").select("estado").execute().data
    if proyectos_data:
        df = pd.DataFrame(proyectos_data)
        df_count = df["estado"].value_counts().reset_index()
        df_count.columns = ["estado", "cantidad"]
        fig = go.Figure(data=[go.Pie(
            labels=df_count["estado"],
            values=df_count["cantidad"],
            hole=0.0,
            marker=dict(colors=["#FFA500", "#4A90D9", "#2ECC71"]),
            textinfo="label+percent+value",
            textfont=dict(size=13, color="white"),
        )])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(t=30, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay proyectos registrados todavía.")

    st.markdown("---")
    st.markdown("### ✅ Progreso General de Tareas")
    total_tareas = tareas_pendientes + tareas_completadas
    if total_tareas > 0:
        porcentaje = int((tareas_completadas / total_tareas) * 100)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div style="background: #333; border-radius: 20px; height: 35px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #C6FF00, #4ECDC4);
                        width: {porcentaje}%; height: 100%; border-radius: 20px;
                        display: flex; align-items: center; justify-content: center;
                        color: black; font-weight: bold;">{porcentaje}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='color:white; margin-top:8px;'>{tareas_completadas} de {total_tareas}</p>", unsafe_allow_html=True)
    else:
        st.info("No hay tareas registradas todavía.")