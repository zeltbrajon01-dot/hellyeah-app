import streamlit as st
import sqlite3
from datetime import date
import os

def crear_conexion():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "hellyeah.db")
    conn = sqlite3.connect(db_path)
    return conn

def mostrar_clientes():
    st.title("👥 Gestión de Clientes")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Lista de Clientes", "➕ Agregar Cliente"])

    # ---- TAB 1: LISTA DE CLIENTES ----
    with tab1:
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        if len(clientes) == 0:
            st.info("No hay clientes registrados todavía. Ve a la pestaña 'Agregar Cliente'.")
        else:
            for cliente in clientes:
                with st.expander(f"🏢 {cliente[1]} — {cliente[2]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Empresa:** {cliente[2]}")
                        st.write(f"**Email:** {cliente[3]}")
                        st.write(f"**Teléfono:** {cliente[4]}")
                    with col2:
                        st.write(f"**Tipo:** {cliente[5]}")
                        st.write(f"**Fecha de registro:** {cliente[6]}")

                    st.markdown("---")
                    col_edit, col_del = st.columns(2)

                    # Botón Editar
                    with col_edit:
                        if st.button(f"✏️ Editar", key=f"edit_btn_{cliente[0]}"):
                            st.session_state[f"editando_{cliente[0]}"] = True

                    # Botón Eliminar
                    with col_del:
                        if st.button(f"🗑️ Eliminar", key=f"del_{cliente[0]}"):
                            conn = crear_conexion()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente[0],))
                            conn.commit()
                            conn.close()
                            st.success(f"Cliente eliminado correctamente.")
                            st.rerun()

                    # Formulario de edición
                    if st.session_state.get(f"editando_{cliente[0]}", False):
                        st.markdown("### ✏️ Editar Cliente")
                        with st.form(key=f"form_edit_{cliente[0]}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_nombre = st.text_input("Nombre", value=cliente[1])
                                nueva_empresa = st.text_input("Empresa", value=cliente[2])
                                nuevo_email = st.text_input("Email", value=cliente[3])
                            with col2:
                                nuevo_telefono = st.text_input("Teléfono", value=cliente[4])
                                nuevo_tipo = st.selectbox("Tipo de cliente", [
                                    "Cliente Pequeño",
                                    "Cliente Mediano",
                                    "Cliente Grande"
                                ], index=["Cliente Pequeño", "Cliente Mediano", "Cliente Grande"].index(cliente[5]) if cliente[5] in ["Cliente Pequeño", "Cliente Mediano", "Cliente Grande"] else 0)

                            col_guardar, col_cancelar = st.columns(2)
                            with col_guardar:
                                guardar = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)
                            with col_cancelar:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("""
                                    UPDATE clientes
                                    SET nombre=?, empresa=?, email=?, telefono=?, tipo=?
                                    WHERE id=?
                                """, (nuevo_nombre, nueva_empresa, nuevo_email, nuevo_telefono, nuevo_tipo, cliente[0]))
                                conn.commit()
                                conn.close()
                                st.success("✅ Cliente actualizado correctamente.")
                                st.session_state[f"editando_{cliente[0]}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_{cliente[0]}"] = False
                                st.rerun()

    # ---- TAB 2: AGREGAR CLIENTE ----
    with tab2:
        st.subheader("Agregar Nuevo Cliente")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del contacto *", placeholder="Ej: Juan Pérez")
            empresa = st.text_input("Empresa *", placeholder="Ej: Bopisa")
            email = st.text_input("Email", placeholder="Ej: juan@bopisa.com")

        with col2:
            telefono = st.text_input("Teléfono", placeholder="Ej: 667-123-4567")
            tipo = st.selectbox("Tipo de cliente", [
                "Cliente Pequeño",
                "Cliente Mediano",
                "Cliente Grande"
            ])
            fecha = st.date_input("Fecha de registro", value=date.today())

        st.markdown("---")

        if st.button("💾 Guardar Cliente", use_container_width=True):
            if nombre == "" or empresa == "":
                st.error("⚠️ El nombre y la empresa son obligatorios.")
            else:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO clientes (nombre, empresa, email, telefono, tipo, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombre, empresa, email, telefono, tipo, str(fecha)))
                conn.commit()
                conn.close()
                st.success(f"✅ Cliente {nombre} de {empresa} agregado correctamente.")
                st.balloons()