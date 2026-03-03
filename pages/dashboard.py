import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

import streamlit as st
import os

def get_database_url():
    try:
        return st.secrets["DATABASE_URL"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("DATABASE_URL")

DATABASE_URL = get_database_url()

def crear_conexion():
    engine = create_engine(DATABASE_URL)
    return engine

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

    engine = crear_conexion()
    with engine.connect() as conn:
        total_clientes = conn.execute(text("SELECT COUNT(*) FROM clientes")).fetchone()[0]
        total_proyectos = conn.execute(text("SELECT COUNT(*) FROM proyectos")).fetchone()[0]
        proyectos_activos = conn.execute(text("SELECT COUNT(*) FROM proyectos WHERE estado = 'En Proceso'")).fetchone()[0]
        proyectos_completados = conn.execute(text("SELECT COUNT(*) FROM proyectos WHERE estado = 'Completado'")).fetchone()[0]
        proyectos_pendientes = conn.execute(text("SELECT COUNT(*) FROM proyectos WHERE estado = 'Pendiente'")).fetchone()[0]
        tareas_pendientes = conn.execute(text("SELECT COUNT(*) FROM tareas WHERE estado != 'Completada'")).fetchone()[0]
        tareas_completadas = conn.execute(text("SELECT COUNT(*) FROM tareas WHERE estado = 'Completada'")).fetchone()[0]
        total_cobrado = conn.execute(text("SELECT SUM(monto) FROM pagos WHERE estado = 'Pagado'")).fetchone()[0] or 0
        total_pendiente = conn.execute(text("SELECT SUM(monto) FROM pagos WHERE estado = 'Pendiente'")).fetchone()[0] or 0
        total_vencido = conn.execute(text("SELECT SUM(monto) FROM pagos WHERE estado = 'Vencido'")).fetchone()[0] or 0

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

    st.markdown("### 📊 Análisis Visual")
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown("#### 📁 Estado de Proyectos")
        engine = crear_conexion()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT estado, COUNT(*) as cantidad FROM proyectos GROUP BY estado"))
            df_proyectos = pd.DataFrame(result.fetchall(), columns=["estado", "cantidad"])

        if df_proyectos.empty:
            st.info("No hay proyectos registrados todavía.")
        else:
            fig1 = go.Figure(data=[go.Pie(
                labels=df_proyectos["estado"],
                values=df_proyectos["cantidad"],
                hole=0.0,
                pull=[0.05] * len(df_proyectos),
                marker=dict(colors=["#FFA500", "#4A90D9", "#2ECC71"], line=dict(color="#1a1a2e", width=3)),
                textinfo="label+percent+value",
                textfont=dict(size=13, color="white"),
            )])
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(color="white")),
                margin=dict(t=30, b=60)
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col_der:
        st.markdown("#### 💳 Estado de Pagos")
        engine = crear_conexion()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT estado, COUNT(*) as cantidad, SUM(monto) as total FROM pagos GROUP BY estado"))
            df_pagos = pd.DataFrame(result.fetchall(), columns=["estado", "cantidad", "total"])

        if df_pagos.empty:
            st.info("No hay pagos registrados todavía.")
        else:
            colores_pagos = {"Pagado": "#2ECC71", "Pendiente": "#F39C12", "Vencido": "#E74C3C"}
            fig2 = go.Figure()
            for _, row in df_pagos.iterrows():
                color = colores_pagos.get(row["estado"], "#4A90D9")
                fig2.add_trace(go.Bar(
                    name=row["estado"],
                    x=[row["estado"]],
                    y=[row["total"]],
                    marker=dict(color=color, opacity=0.9, line=dict(color="white", width=1.5)),
                    text=f"${row['total']:,.0f}",
                    textposition="outside",
                    textfont=dict(color="white", size=13),
                ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", showticklabels=False),
                showlegend=False,
                bargap=0.3,
                margin=dict(t=30, b=30)
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.markdown("### 📈 Ingresos por Mes")
    engine = crear_conexion()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT TO_CHAR(fecha_emision, 'YYYY-MM') as mes, SUM(monto) as total
            FROM pagos WHERE estado = 'Pagado'
            GROUP BY mes ORDER BY mes
        """))
        df_ingresos = pd.DataFrame(result.fetchall(), columns=["mes", "total"])

    if df_ingresos.empty:
        st.info("No hay ingresos registrados todavía.")
    else:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_ingresos["mes"],
            y=df_ingresos["total"],
            mode="lines+markers",
            line=dict(color="#C6FF00", width=4),
            marker=dict(size=12, color="#C6FF00", line=dict(color="white", width=2)),
            fill="tozeroy",
            fillcolor="rgba(198,255,0,0.15)",
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, title="Mes"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", title="Monto ($)"),
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    st.markdown("### 🏆 Top Clientes más Rentables")
    engine = crear_conexion()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT c.empresa, SUM(p.monto) as total
            FROM pagos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            WHERE p.estado = 'Pagado'
            GROUP BY c.empresa
            ORDER BY total DESC LIMIT 5
        """))
        df_rentables = pd.DataFrame(result.fetchall(), columns=["empresa", "total"])

    if df_rentables.empty:
        st.info("No hay pagos registrados todavía.")
    else:
        for i, row in df_rentables.iterrows():
            maximo = df_rentables["total"].max()
            porcentaje = int((row["total"] / maximo) * 100)
            medalla = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "⭐"
            st.markdown(f"""
                <div style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: white; font-weight: 600;">{medalla} {row['empresa']}</span>
                        <span style="color: #C6FF00; font-weight: bold;">${row['total']:,.2f}</span>
                    </div>
                    <div style="background: #333; border-radius: 20px; height: 14px;">
                        <div style="background: linear-gradient(90deg, #C6FF00, #4ECDC4);
                            width: {porcentaje}%; height: 100%; border-radius: 20px;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

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