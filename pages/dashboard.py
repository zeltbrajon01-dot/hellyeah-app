import streamlit as st
from config import get_supabase
import pandas as pd
import plotly.graph_objects as go

def card_metrica(titulo, valor, icono, color_fondo, color_texto):
    st.markdown(f"""
        <div style="
            background: {color_fondo};
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #F0F0F0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 1.6rem; margin-bottom: 12px;">{icono}</div>
            <div style="color: #888888; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px;">{titulo}</div>
            <div style="color: {color_texto}; font-size: 1.9rem; font-weight: 700; letter-spacing: -1px;">{valor}</div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_dashboard():
    st.markdown("""
        <h1 style="
            color: #1A1A1A;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        ">HellYeah Agency</h1>
        <p style="color: #AAAAAA; font-size: 0.9rem; margin-bottom: 32px; font-weight: 400;">Panel de control — Resumen general</p>
        <hr style="border: none; border-top: 1px solid #F0F0F0; margin-bottom: 32px;">
    """, unsafe_allow_html=True)

    sb = get_supabase()

    total_clientes = len(sb.table("clientes").select("id").execute().data)
    total_proyectos = len(sb.table("proyectos").select("id").execute().data)
    proyectos_activos = len(sb.table("proyectos").select("id").eq("estado", "En Proceso").execute().data)
    tareas_pendientes = len(sb.table("tareas").select("id").neq("estado", "Completada").execute().data)
    tareas_completadas = len(sb.table("tareas").select("id").eq("estado", "Completada").execute().data)

    pagos_cobrados = sb.table("pagos").select("monto").eq("estado", "Pagado").execute().data
    total_cobrado = sum([p["monto"] for p in pagos_cobrados]) if pagos_cobrados else 0

    pagos_pendientes_data = sb.table("pagos").select("monto").eq("estado", "Pendiente").execute().data
    total_pendiente = sum([p["monto"] for p in pagos_pendientes_data]) if pagos_pendientes_data else 0

    pagos_vencidos = sb.table("pagos").select("monto").eq("estado", "Vencido").execute().data
    total_vencido = sum([p["monto"] for p in pagos_vencidos]) if pagos_vencidos else 0

    st.markdown("### Resumen")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Clientes", total_clientes, "👥", "#FFFFFF", "#1A1A1A")
    with col2:
        card_metrica("Proyectos", total_proyectos, "📁", "#FFFFFF", "#1A1A1A")
    with col3:
        card_metrica("Activos", proyectos_activos, "🔄", "#FFFFFF", "#1A1A1A")
    with col4:
        card_metrica("Tareas pendientes", tareas_pendientes, "⚡", "#FFFFFF", "#1A1A1A")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Finanzas")
    col1, col2, col3 = st.columns(3)
    with col1:
        card_metrica("Total cobrado", f"${total_cobrado:,.2f}", "💵", "#F0FDF4", "#16A34A")
    with col2:
        card_metrica("Por cobrar", f"${total_pendiente:,.2f}", "⏳", "#FFFBEB", "#D97706")
    with col3:
        card_metrica("Vencido", f"${total_vencido:,.2f}", "🚨", "#FFF1F2", "#E11D48")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid #F0F0F0;'>", unsafe_allow_html=True)

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown("### Estado de Proyectos")
        proyectos_data = sb.table("proyectos").select("estado").execute().data
        if proyectos_data:
            df = pd.DataFrame(proyectos_data)
            df_count = df["estado"].value_counts().reset_index()
            df_count.columns = ["estado", "cantidad"]
            fig = go.Figure(data=[go.Pie(
                labels=df_count["estado"],
                values=df_count["cantidad"],
                hole=0.6,
                marker=dict(
                    colors=["#1A1A1A", "#555555", "#AAAAAA"],
                    line=dict(color="#FFFFFF", width=3)
                ),
                textinfo="label+percent",
                textfont=dict(size=12, color="#1A1A1A"),
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#1A1A1A", family="Montserrat"),
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay proyectos todavía.")

    with col_der:
        st.markdown("### Ingresos")
        pagos_data = sb.table("pagos").select("estado, monto").execute().data
        if pagos_data:
            df_pagos = pd.DataFrame(pagos_data)
            df_group = df_pagos.groupby("estado")["monto"].sum().reset_index()
            colores = {"Pagado": "#1A1A1A", "Pendiente": "#AAAAAA", "Vencido": "#E11D48"}
            fig2 = go.Figure()
            for _, row in df_group.iterrows():
                fig2.add_trace(go.Bar(
                    name=row["estado"],
                    x=[row["estado"]],
                    y=[row["monto"]],
                    marker=dict(
                        color=colores.get(row["estado"], "#AAAAAA"),
                        line=dict(color="#FFFFFF", width=2)
                    ),
                    text=f"${row['monto']:,.0f}",
                    textposition="outside",
                    textfont=dict(color="#1A1A1A", size=12),
                ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#1A1A1A", family="Montserrat"),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=False, showticklabels=False),
                showlegend=False,
                bargap=0.4,
                margin=dict(t=20, b=20, l=20, r=20),
                height=280
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay pagos todavía.")

    st.markdown("<hr style='border:none; border-top:1px solid #F0F0F0;'>", unsafe_allow_html=True)

    st.markdown("### Progreso de Tareas")
    total_tareas = tareas_pendientes + tareas_completadas
    if total_tareas > 0:
        porcentaje = int((tareas_completadas / total_tareas) * 100)
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
                <div style="background: #F5F5F7; border-radius: 100px; height: 8px; overflow: hidden; margin-top: 14px;">
                    <div style="background: #1A1A1A; width: {porcentaje}%; height: 100%; border-radius: 100px; transition: width 0.5s ease;"></div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='color:#1A1A1A; font-weight:600; font-size:0.9rem; margin-top:8px;'>{porcentaje}% completado</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#AAAAAA; font-size:0.8rem; margin-top:8px;'>{tareas_completadas} de {total_tareas} tareas completadas</p>", unsafe_allow_html=True)
    else:
        st.info("No hay tareas registradas todavía.")