import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from datetime import date

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

def mostrar_pagos():
    st.title("💰 Gestión de Pagos")
    st.markdown("---")

    engine = crear_conexion()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT SUM(monto) FROM pagos WHERE estado = 'Pagado'
        """))
        total_cobrado = result.fetchone()[0] or 0

        result = conn.execute(text("""
            SELECT SUM(monto) FROM pagos WHERE estado = 'Pendiente'
        """))
        total_pendiente = result.fetchone()[0] or 0

        result = conn.execute(text("""
            SELECT SUM(monto) FROM pagos WHERE estado = 'Vencido'
        """))
        total_vencido = result.fetchone()[0] or 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2ECC7122, #2ECC7144);
                border-left: 4px solid #2ECC71; border-radius: 12px; padding: 20px;">
                <div style="color: #aaa; font-size: 0.85rem;">💵 Total Cobrado</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold;">${total_cobrado:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F39C1222, #F39C1244);
                border-left: 4px solid #F39C12; border-radius: 12px; padding: 20px;">
                <div style="color: #aaa; font-size: 0.85rem;">⏳ Por Cobrar</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold;">${total_pendiente:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #E74C3C22, #E74C3C44);
                border-left: 4px solid #E74C3C; border-radius: 12px; padding: 20px;">
                <div style="color: #aaa; font-size: 0.85rem;">🚨 Vencido</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold;">${total_vencido:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Lista de Pagos", "➕ Registrar Pago"])

    with tab1:
        filtro = st.selectbox("Filtrar por estado", ["Todos", "Pagado", "Pendiente", "Vencido"])

        engine = crear_conexion()
        with engine.connect() as conn:
            if filtro == "Todos":
                result = conn.execute(text("""
                    SELECT p.id, c.empresa, pr.nombre, p.concepto, p.monto, 
                           p.estado, p.fecha_emision, p.fecha_pago
                    FROM pagos p
                    LEFT JOIN clientes c ON p.cliente_id = c.id
                    LEFT JOIN proyectos pr ON p.proyecto_id = pr.id
                    ORDER BY p.id DESC
                """))
            else:
                result = conn.execute(text("""
                    SELECT p.id, c.empresa, pr.nombre, p.concepto, p.monto,
                           p.estado, p.fecha_emision, p.fecha_pago
                    FROM pagos p
                    LEFT JOIN clientes c ON p.cliente_id = c.id
                    LEFT JOIN proyectos pr ON p.proyecto_id = pr.id
                    WHERE p.estado = :estado
                    ORDER BY p.id DESC
                """), {"estado": filtro})
            pagos = result.fetchall()

        if len(pagos) == 0:
            st.info("No hay pagos registrados todavía.")
        else:
            for pago in pagos:
                if pago[5] == "Pagado":
                    icono = "✅"
                    color = "#2ECC71"
                elif pago[5] == "Vencido":
                    icono = "🚨"
                    color = "#E74C3C"
                else:
                    icono = "⏳"
                    color = "#F39C12"

                with st.expander(f"{icono} {pago[3]} — {pago[1]} — ${pago[4]:,.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Cliente:** {pago[1]}")
                        st.write(f"**Proyecto:** {pago[2] or 'Sin proyecto'}")
                        st.write(f"**Concepto:** {pago[3]}")
                    with col2:
                        st.write(f"**Monto:** ${pago[4]:,.2f}")
                        st.write(f"**Estado:** {pago[5]}")
                        st.write(f"**Fecha emisión:** {pago[6]}")
                        st.write(f"**Fecha pago:** {pago[7] or 'Pendiente'}")

                    col_a, col_b, col_c, col_d = st.columns(4)

                    with col_a:
                        if st.button("✅ Pagado", key=f"pagado_{pago[0]}"):
                            engine = crear_conexion()
                            with engine.connect() as conn:
                                conn.execute(text("""
                                    UPDATE pagos SET estado='Pagado', fecha_pago=:fecha 
                                    WHERE id=:id
                                """), {"fecha": str(date.today()), "id": pago[0]})
                                conn.commit()
                            st.rerun()

                    with col_b:
                        if st.button("🚨 Vencido", key=f"vencido_{pago[0]}"):
                            engine = crear_conexion()
                            with engine.connect() as conn:
                                conn.execute(text("""
                                    UPDATE pagos SET estado='Vencido' WHERE id=:id
                                """), {"id": pago[0]})
                                conn.commit()
                            st.rerun()

                    with col_c:
                        if st.button("✏️ Editar", key=f"edit_pago_{pago[0]}"):
                            st.session_state[f"editando_pago_{pago[0]}"] = True

                    with col_d:
                        if st.button("🗑️ Eliminar", key=f"del_pago_{pago[0]}"):
                            engine = crear_conexion()
                            with engine.connect() as conn:
                                conn.execute(text("DELETE FROM pagos WHERE id=:id"), {"id": pago[0]})
                                conn.commit()
                            st.success("Pago eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_pago_{pago[0]}", False):
                        with st.form(key=f"form_edit_pago_{pago[0]}"):
                            st.markdown("### ✏️ Editar Pago")
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_concepto = st.text_input("Concepto", value=pago[3])
                                nuevo_monto = st.number_input("Monto", value=float(pago[4]), min_value=0.0)
                            with col2:
                                nuevo_estado = st.selectbox("Estado", ["Pendiente", "Pagado", "Vencido"],
                                    index=["Pendiente", "Pagado", "Vencido"].index(pago[5]) if pago[5] in ["Pendiente", "Pagado", "Vencido"] else 0)
                                nueva_fecha_emision = st.date_input("Fecha emisión",
                                    value=pago[6] if pago[6] else date.today())
                                nueva_fecha_pago = st.date_input("Fecha pago",
                                    value=pago[7] if pago[7] else date.today())

                            col_g, col_c2 = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c2:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                engine = crear_conexion()
                                with engine.connect() as conn:
                                    conn.execute(text("""
                                        UPDATE pagos 
                                        SET concepto=:concepto, monto=:monto, estado=:estado,
                                            fecha_emision=:fecha_emision, fecha_pago=:fecha_pago
                                        WHERE id=:id
                                    """), {
                                        "concepto": nuevo_concepto,
                                        "monto": nuevo_monto,
                                        "estado": nuevo_estado,
                                        "fecha_emision": str(nueva_fecha_emision),
                                        "fecha_pago": str(nueva_fecha_pago),
                                        "id": pago[0]
                                    })
                                    conn.commit()
                                st.success("✅ Pago actualizado.")
                                st.session_state[f"editando_pago_{pago[0]}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_pago_{pago[0]}"] = False
                                st.rerun()

    with tab2:
        st.subheader("➕ Registrar Nuevo Pago")

        engine = crear_conexion()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nombre, empresa FROM clientes"))
            clientes = result.fetchall()
            result = conn.execute(text("SELECT id, nombre FROM proyectos"))
            proyectos = result.fetchall()

        if len(clientes) == 0:
            st.warning("⚠️ Primero debes agregar clientes.")
        else:
            col1, col2 = st.columns(2)
            cliente_opciones = {f"{c[1]} — {c[2]}": c[0] for c in clientes}
            proyecto_opciones = {"Sin proyecto": None}
            proyecto_opciones.update({p[1]: p[0] for p in proyectos})

            with col1:
                concepto = st.text_input("Concepto *", placeholder="Ej: Mensualidad Marzo")
                cliente_sel = st.selectbox("Cliente *", list(cliente_opciones.keys()))
                proyecto_sel = st.selectbox("Proyecto", list(proyecto_opciones.keys()))
            with col2:
                monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
                estado = st.selectbox("Estado", ["Pendiente", "Pagado", "Vencido"])
                fecha_emision = st.date_input("Fecha emisión", value=date.today())
                fecha_pago = st.date_input("Fecha pago", value=date.today())

            st.markdown("---")

            if st.button("💾 Guardar Pago", use_container_width=True):
                if concepto == "":
                    st.error("⚠️ El concepto es obligatorio.")
                else:
                    engine = crear_conexion()
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO pagos (cliente_id, proyecto_id, concepto, monto, estado, fecha_emision, fecha_pago)
                            VALUES (:cliente_id, :proyecto_id, :concepto, :monto, :estado, :fecha_emision, :fecha_pago)
                        """), {
                            "cliente_id": cliente_opciones[cliente_sel],
                            "proyecto_id": proyecto_opciones[proyecto_sel],
                            "concepto": concepto,
                            "monto": monto,
                            "estado": estado,
                            "fecha_emision": str(fecha_emision),
                            "fecha_pago": str(fecha_pago)
                        })
                        conn.commit()
                    st.success(f"✅ Pago registrado correctamente.")
                    st.balloons()