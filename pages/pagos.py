import streamlit as st
import sqlite3
from datetime import date
import os

def crear_conexion():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "hellyeah.db")
    conn = sqlite3.connect(db_path)
    return conn

def mostrar_pagos():
    st.title("💰 Control de Pagos")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Lista de Pagos", "➕ Agregar Pago"])

    with tab1:
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.id, c.nombre, c.empresa, pr.nombre, pa.concepto, 
                   pa.monto, pa.estado, pa.fecha_emision, pa.fecha_pago
            FROM pagos pa
            LEFT JOIN clientes c ON pa.cliente_id = c.id
            LEFT JOIN proyectos pr ON pa.proyecto_id = pr.id
            ORDER BY pa.fecha_emision DESC
        """)
        pagos = cursor.fetchall()
        conn.close()

        if len(pagos) == 0:
            st.info("No hay pagos registrados todavía. Ve a la pestaña 'Agregar Pago'.")
        else:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Pagado'")
            total_cobrado = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Pendiente'")
            total_pendiente = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(monto) FROM pagos WHERE estado = 'Vencido'")
            total_vencido = cursor.fetchone()[0] or 0
            conn.close()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Total Cobrado", f"${total_cobrado:,.2f}")
            with col2:
                st.metric("⏳ Por Cobrar", f"${total_pendiente:,.2f}")
            with col3:
                st.metric("🚨 Vencido", f"${total_vencido:,.2f}")

            st.markdown("---")

            filtro = st.selectbox("Filtrar por estado", ["Todos", "Pendiente", "Pagado", "Vencido"])

            for pago in pagos:
                if filtro != "Todos" and pago[6] != filtro:
                    continue

                if pago[6] == "Pagado":
                    icono = "✅"
                elif pago[6] == "Vencido":
                    icono = "🚨"
                else:
                    icono = "⏳"

                with st.expander(f"{icono} {pago[2]} — {pago[4]} — ${pago[5]:,.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Cliente:** {pago[1]} ({pago[2]})")
                        st.write(f"**Proyecto:** {pago[3] or 'Sin proyecto'}")
                        st.write(f"**Concepto:** {pago[4]}")
                    with col2:
                        st.write(f"**Monto:** ${pago[5]:,.2f}")
                        st.write(f"**Estado:** {pago[6]}")
                        st.write(f"**Fecha emisión:** {pago[7]}")
                        st.write(f"**Fecha pago:** {pago[8] or 'Pendiente'}")

                    st.markdown("---")
                    col_pagar, col_vencer, col_editar, col_del = st.columns(4)

                    with col_pagar:
                        if pago[6] != "Pagado":
                            if st.button("✅ Pagado", key=f"pagar_{pago[0]}"):
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("""
                                    UPDATE pagos SET estado='Pagado', fecha_pago=? WHERE id=?
                                """, (str(date.today()), pago[0]))
                                conn.commit()
                                conn.close()
                                st.success("✅ Pago registrado.")
                                st.rerun()

                    with col_vencer:
                        if pago[6] == "Pendiente":
                            if st.button("🚨 Vencido", key=f"vencer_{pago[0]}"):
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("UPDATE pagos SET estado='Vencido' WHERE id=?", (pago[0],))
                                conn.commit()
                                conn.close()
                                st.warning("🚨 Marcado como vencido.")
                                st.rerun()

                    with col_editar:
                        if st.button("✏️ Editar", key=f"edit_pago_{pago[0]}"):
                            st.session_state[f"editando_pago_{pago[0]}"] = True

                    with col_del:
                        if st.button("🗑️ Eliminar", key=f"del_pago_{pago[0]}"):
                            conn = crear_conexion()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM pagos WHERE id=?", (pago[0],))
                            conn.commit()
                            conn.close()
                            st.success("Pago eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_pago_{pago[0]}", False):
                        with st.form(key=f"form_pago_{pago[0]}"):
                            st.markdown("### ✏️ Editar Pago")
                            col1, col2 = st.columns(2)

                            with col1:
                                nuevo_concepto = st.text_input("Concepto", value=pago[4])
                                nuevo_monto = st.number_input("Monto ($)", value=float(pago[5]), min_value=0.0)
                                nuevo_estado = st.selectbox("Estado", [
                                    "Pendiente", "Pagado", "Vencido"
                                ], index=["Pendiente", "Pagado", "Vencido"].index(pago[6]) if pago[6] in ["Pendiente", "Pagado", "Vencido"] else 0)

                            with col2:
                                nueva_fecha_emision = st.date_input("Fecha de emisión", value=date.today())
                                nueva_fecha_pago = st.date_input("Fecha de pago", value=date.today())

                            col_g, col_c = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("""
                                    UPDATE pagos SET concepto=?, monto=?, estado=?, 
                                    fecha_emision=?, fecha_pago=?
                                    WHERE id=?
                                """, (nuevo_concepto, nuevo_monto, nuevo_estado,
                                      str(nueva_fecha_emision), str(nueva_fecha_pago), pago[0]))
                                conn.commit()
                                conn.close()
                                st.success("✅ Pago actualizado correctamente.")
                                st.session_state[f"editando_pago_{pago[0]}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_pago_{pago[0]}"] = False
                                st.rerun()

    with tab2:
        st.subheader("Registrar Nuevo Pago")

        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, empresa FROM clientes")
        clientes = cursor.fetchall()
        cursor.execute("SELECT id, nombre FROM proyectos")
        proyectos = cursor.fetchall()
        conn.close()

        if len(clientes) == 0:
            st.warning("⚠️ Primero debes agregar clientes antes de registrar pagos.")
        else:
            col1, col2 = st.columns(2)

            cliente_opciones = {f"{c[1]} — {c[2]}": c[0] for c in clientes}
            proyecto_opciones = {"Sin proyecto": None}
            proyecto_opciones.update({p[1]: p[0] for p in proyectos})

            with col1:
                cliente_sel = st.selectbox("Cliente *", list(cliente_opciones.keys()))
                concepto = st.text_input("Concepto *", placeholder="Ej: Mensualidad Febrero 2026")
                monto = st.number_input("Monto ($) *", min_value=0.0, step=100.0)

            with col2:
                proyecto_sel = st.selectbox("Proyecto (opcional)", list(proyecto_opciones.keys()))
                estado = st.selectbox("Estado", ["Pendiente", "Pagado", "Vencido"])
                fecha_emision = st.date_input("Fecha de emisión", value=date.today())

            st.markdown("---")

            if st.button("💾 Guardar Pago", use_container_width=True):
                if concepto == "" or monto == 0:
                    st.error("⚠️ El concepto y el monto son obligatorios.")
                else:
                    fecha_pago_auto = str(date.today()) if estado == "Pagado" else None
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO pagos (cliente_id, proyecto_id, concepto, monto, estado, fecha_emision, fecha_pago)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        cliente_opciones[cliente_sel],
                        proyecto_opciones[proyecto_sel],
                        concepto, monto, estado,
                        str(fecha_emision),
                        fecha_pago_auto
                    ))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Pago de ${monto:,.2f} registrado correctamente.")
                    st.balloons()