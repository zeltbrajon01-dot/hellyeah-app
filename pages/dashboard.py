import streamlit as st
from config import get_supabase
import pandas as pd
import plotly.graph_objects as go

def card_metrica(titulo, valor, icono, color_borde):
    st.markdown(f"""
        <div style="
            background: #FFFFFF;
            border-radius: 12px;
            padding: 20px 24px;
            border: 1px solid #E6E9EF;
            border-top: 3px solid {color_borde};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="color:#676879; font-size:0.75rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:10px;">{titulo}</div>
                    <div style="color:#323338; font-size:1.8rem; font-weight:700; letter-spacing:-1px;">{valor}</div>
                </div>
                <div style="font-size:1.5rem; opacity:0.7;">{icono}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_dashboard():
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h1 style="
                color: #323338;
                font-size: 1.6rem;
                font-weight: 700;
                letter-spacing: -0.3px;
                margin: 0 0 4px 0;
            ">Panel de Control</h1>
            <p style="color: #676879; font-size: 0.85rem; margin: 0;">
                Bienvenido de vuelta — aquí está tu resumen de hoy
            </p>
        </div>
        <hr style="border:none; border-top:1px solid #E6E9EF; margin: 20px 0 28px 0;">
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

    st.markdown("<p style='color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>RESUMEN GENERAL</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Clientes", total_clientes, "👥", "#4353FF")
    with col2:
        card_metrica("Proyectos", total_proyectos, "📁", "#6B5BFF")
    with col3:
        card_metrica("En proceso", proyectos_activos, "🔄", "#00C875")
    with col4:
        card_metrica("Tareas pendientes", tareas_pendientes, "⚡", "#FFCB00")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>RESUMEN FINANCIERO</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        card_metrica("Total cobrado", f"${total_cobrado:,.2f}", "💵", "#00C875")
    with col2:
        card_metrica("Por cobrar", f"${total_pendiente:,.2f}", "⏳", "#FFCB00")
    with col3:
        card_metrica("Vencido", f"${total_vencido:,.2f}", "🚨", "#E2445C")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown("""
            <div style="background:#FFFFFF; border-radius:12px; padding:20px 24px; border:1px solid #E6E9EF; box-shadow:0 2px 8px rgba(0,0,0,0.04); margin-bottom:16px;">
                <p style="color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:0 0 16px 0;">ESTADO DE PROYECTOS</p>
        """, unsafe_allow_html=True)

        proyectos_data = sb.table("proyectos").select("estado").execute().data
        if proyectos_data:
            df = pd.DataFrame(proyectos_data)
            df_count = df["estado"].value_counts().reset_index()
            df_count.columns = ["estado", "cantidad"]
            fig = go.Figure(data=[go.Pie(
                labels=df_count["estado"],
                values=df_count["cantidad"],
                hole=0.65,
                marker=dict(
                    colors=["#4353FF", "#00C875", "#FFCB00", "#E2445C"],
                    line=dict(color="#FFFFFF", width=2)
                ),
                textinfo="label+percent",
                textfont=dict(size=11, color="#323338"),
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#323338", family="Montserrat"),
                showlegend=True,
                legend=dict(
                    font=dict(size=11, color="#676879"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=260
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay proyectos todavía.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_der:
        st.markdown("""
            <div style="background:#FFFFFF; border-radius:12px; padding:20px 24px; border:1px solid #E6E9EF; box-shadow:0 2px 8px rgba(0,0,0,0.04); margin-bottom:16px;">
                <p style="color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:0 0 16px 0;">INGRESOS POR ESTADO</p>
        """, unsafe_allow_html=True)

        pagos_data = sb.table("pagos").select("estado, monto").execute().data
        if pagos_data:
            df_pagos = pd.DataFrame(pagos_data)
            df_group = df_pagos.groupby("estado")["monto"].sum().reset_index()
            colores = {"Pagado": "#00C875", "Pendiente": "#FFCB00", "Vencido": "#E2445C"}
            fig2 = go.Figure()
            for _, row in df_group.iterrows():
                fig2.add_trace(go.Bar(
                    name=row["estado"],
                    x=[row["estado"]],
                    y=[row["monto"]],
                    marker=dict(
                        color=colores.get(row["estado"], "#4353FF"),
                        line=dict(color="#FFFFFF", width=0)
                    ),
                    text=f"${row['monto']:,.0f}",
                    textposition="outside",
                    textfont=dict(color="#323338", size=11),
                ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#323338", family="Montserrat"),
                xaxis=dict(showgrid=False, title="", color="#676879"),
                yaxis=dict(showgrid=False, showticklabels=False),
                showlegend=False,
                bargap=0.5,
                margin=dict(t=30, b=10, l=10, r=10),
                height=260
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay pagos todavía.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>PROGRESO DE TAREAS</p>", unsafe_allow_html=True)

    total_tareas = tareas_pendientes + tareas_completadas
    if total_tareas > 0:
        porcentaje = int((tareas_completadas / total_tareas) * 100)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
                <div style="background:#F6F7FB; border-radius:100px; height:10px; overflow:hidden; margin-top:12px;">
                    <div style="background:linear-gradient(90deg, #4353FF, #6B5BFF); width:{porcentaje}%; height:100%; border-radius:100px;"></div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='color:#4353FF; font-weight:700; font-size:0.9rem; margin-top:6px;'>{porcentaje}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#676879; font-size:0.8rem; margin-top:8px;'>{tareas_completadas} de {total_tareas} tareas completadas</p>", unsafe_allow_html=True)
    else:
        st.info("No hay tareas registradas todavía.")