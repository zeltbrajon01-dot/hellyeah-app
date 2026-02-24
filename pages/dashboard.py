import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def crear_conexion():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "hellyeah.db")
    conn = sqlite3.connect(db_path)
    return conn

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

def card_estado(titulo, valor, icono, color, descripcion=""):
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}44);
            border: 1px solid {color}66;
            border-radius: 12px;
            padding: 25px;
            margin: 5px 0;
            text-align: center;
        ">
            <div style="font-size: 2.5rem;">{icono}</div>
            <div style="color: white; font-size: 2.2rem; font-weight: bold; margin: 8px 0;">{valor}</div>
            <div style="color: {color}; font-size: 0.95rem; font-weight: 600;">{titulo}</div>
            <div style="color: #aaa; font-size: 0.8rem; margin-top: 4px;">{descripcion}</div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_dashboard():
    st.markdown("""
        <h1 style="
            background: linear-gradient(90deg, #FF6B6B, #FFE66D, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: bold;
        ">🔥 HellYeah Agency — Panel de Control</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proyectos")
    total_proyectos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proyectos WHERE estado = 'En Proceso'")
    proyectos_activos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proyectos WHERE estado = 'Completado'")
    proyectos_completados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM proyectos WHERE estado = 'Pendiente'")
    proyectos_pendientes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado != 'Completada'")
    tareas_pendientes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado = 'Completada'")
    tareas_completadas = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Pagado'")
    total_cobrado = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Pendiente'")
    total_pendiente = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Vencido'")
    total_vencido = cursor.fetchone()[0] or 0

    conn.close()

    # ---- FILA 1: TARJETAS PRINCIPALES ----
    st.markdown("### 📌 Resumen General")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metrica("Total Clientes", total_clientes, "👥", "#4ECDC4")
    with col2:
        card_metrica("Total Proyectos", total_proyectos, "📁", "#4A90D9")
    with col3:
        card_metrica("Proyectos Activos", proyectos_activos, "🔄", "#FFE66D")
    with col4:
        card_metrica("Tareas Pendientes", tareas_pendientes, "⚡", "#FF6B6B")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- FILA 2: TARJETAS FINANCIERAS ----
    st.markdown("### 💰 Resumen Financiero")
    col1, col2, col3 = st.columns(3)
    with col1:
        card_metrica("Total Cobrado", f"${total_cobrado:,.2f}", "💵", "#2ECC71")
    with col2:
        card_metrica("Por Cobrar", f"${total_pendiente:,.2f}", "⏳", "#F39C12")
    with col3:
        card_metrica("Vencido", f"${total_vencido:,.2f}", "🚨", "#E74C3C")

    st.markdown("---")

    # ---- FILA 3: GRÁFICAS 3D ----
    st.markdown("### 📊 Análisis Visual")
    col_izq, col_der = st.columns(2)

    # Gráfica 3D — Estado de Proyectos
    with col_izq:
        st.markdown("#### 📁 Estado de Proyectos")
        conn = crear_conexion()
        df_proyectos = pd.read_sql_query("""
            SELECT estado, COUNT(*) as cantidad 
            FROM proyectos GROUP BY estado
        """, conn)
        conn.close()

        if df_proyectos.empty:
            st.info("No hay proyectos registrados todavía.")
        else:
            fig1 = go.Figure(data=[go.Pie(
                labels=df_proyectos["estado"],
                values=df_proyectos["cantidad"],
                hole=0.0,
                pull=[0.05] * len(df_proyectos),
                marker=dict(
                    colors=["#FFA500", "#4A90D9", "#2ECC71"],
                    line=dict(color="#1a1a2e", width=3)
                ),
                textinfo="label+percent+value",
                textfont=dict(size=13, color="white"),
                hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>"
            )])
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", size=13),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    font=dict(color="white")
                ),
                margin=dict(t=30, b=60)
            )
            st.plotly_chart(fig1, use_container_width=True)

    # Gráfica 3D — Estado de Pagos
    with col_der:
        st.markdown("#### 💳 Estado de Pagos")
        conn = crear_conexion()
        df_pagos = pd.read_sql_query("""
            SELECT estado, COUNT(*) as cantidad, SUM(monto) as total
            FROM pagos GROUP BY estado
        """, conn)
        conn.close()

        if df_pagos.empty:
            st.info("No hay pagos registrados todavía.")
        else:
            colores_pagos = {
                "Pagado": "#2ECC71",
                "Pendiente": "#F39C12",
                "Vencido": "#E74C3C"
            }
            fig2 = go.Figure()
            for _, row in df_pagos.iterrows():
                color = colores_pagos.get(row["estado"], "#4A90D9")
                fig2.add_trace(go.Bar(
                    name=row["estado"],
                    x=[row["estado"]],
                    y=[row["total"]],
                    marker=dict(
                        color=color,
                        opacity=0.9,
                        line=dict(color="white", width=1.5)
                    ),
                    text=f"${row['total']:,.0f}",
                    textposition="outside",
                    textfont=dict(color="white", size=13),
                    hovertemplate=f"<b>{row['estado']}</b><br>Total: ${row['total']:,.2f}<br>Cantidad: {row['cantidad']}<extra></extra>"
                ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white", size=13),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    showticklabels=False
                ),
                showlegend=False,
                bargap=0.3,
                margin=dict(t=30, b=30)
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ---- FILA 4: INGRESOS POR MES ----
    st.markdown("### 📈 Ingresos por Mes")
    conn = crear_conexion()
    df_ingresos = pd.read_sql_query("""
        SELECT strftime('%Y-%m', fecha_emision) as mes, 
               SUM(monto) as total
        FROM pagos WHERE estado = 'Pagado'
        GROUP BY mes ORDER BY mes
    """, conn)
    conn.close()

    if df_ingresos.empty:
        st.info("No hay ingresos registrados todavía.")
    else:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_ingresos["mes"],
            y=df_ingresos["total"],
            mode="lines+markers",
            line=dict(color="#2ECC71", width=4),
            marker=dict(
                size=12,
                color="#2ECC71",
                line=dict(color="white", width=2),
                symbol="circle"
            ),
            fill="tozeroy",
            fillcolor="rgba(46,204,113,0.15)",
            hovertemplate="<b>%{x}</b><br>Ingresos: $%{y:,.2f}<extra></extra>"
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=13),
            xaxis=dict(showgrid=False, title="Mes"),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                title="Monto ($)"
            ),
            margin=dict(t=20, b=20),
            hovermode="x unified"
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ---- FILA 5: TOP CLIENTES ----
    st.markdown("### 🏆 Top Clientes más Rentables")
    conn = crear_conexion()
    df_rentables = pd.read_sql_query("""
        SELECT c.empresa, SUM(p.monto) as total
        FROM pagos p
        LEFT JOIN clientes c ON p.cliente_id = c.id
        WHERE p.estado = 'Pagado'
        GROUP BY c.empresa
        ORDER BY total DESC LIMIT 5
    """, conn)
    conn.close()

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
                        <span style="color: white; font-weight: 600; font-size: 1rem;">{medalla} {row['empresa']}</span>
                        <span style="color: #2ECC71; font-weight: bold; font-size: 1rem;">${row['total']:,.2f}</span>
                    </div>
                    <div style="background: #333; border-radius: 20px; height: 14px;">
                        <div style="
                            background: linear-gradient(90deg, #2ECC71, #4ECDC4);
                            width: {porcentaje}%;
                            height: 100%;
                            border-radius: 20px;
                        "></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- FILA 6: PROGRESO DE TAREAS ----
    st.markdown("### ✅ Progreso General de Tareas")
    total_tareas = tareas_pendientes + tareas_completadas

    if total_tareas > 0:
        porcentaje = int((tareas_completadas / total_tareas) * 100)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div style="background: #333; border-radius: 20px; height: 35px; overflow: hidden;">
                    <div style="
                        background: linear-gradient(90deg, #2ECC71, #4ECDC4);
                        width: {porcentaje}%;
                        height: 100%;
                        border-radius: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        font-size: 1rem;
                    ">{porcentaje}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <p style='color:white; margin-top: 8px; font-size: 0.9rem;'>
                    {tareas_completadas} de {total_tareas} completadas
                </p>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay tareas registradas todavía.")