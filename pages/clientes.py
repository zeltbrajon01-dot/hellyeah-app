import streamlit as st
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def crear_conexion():
    engine = create_engine(DATABASE_URL)
    return engine

def mostrar_clientes():
    st.title("👥 Gestión de Clientes")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Lista de Clientes", "➕ Agregar Cliente"])

    with tab1:
        engine = crear_conexion()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM clientes ORDER BY id DESC"))
            clientes = result.fetchall()

        if len(clientes) == 0:
            st.info("No hay clientes registrados todavía.")
        else:
            for cliente in clientes:
                with st.expander(f"👤 {cliente[1]} — {cliente[2]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nombre:** {cliente[1]}")
                        st.write(f"**Empresa:** {cliente[2]}")
                        st.write(f"**Email:** {cliente[3]}")
                    with col2:
                        st.write(f"**Teléfono:** {cliente[4]}")
                        st.write(f"**Tipo:** {cliente[5]}")
                        st.write(f"**Fecha registro:** {cliente[6]}")

                    col_edit, col_del = st.columns(2)

                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{cliente[0]}"):
                            st.session_state[f"editando_{cliente[0]}"] = True

                    with col_del:
                        if st.button("🗑️ Eliminar", key=f"del_{cliente[0]}"):
                            engine = crear_conexion()
                            with engine.connect() as conn:
                                conn.execute(text("DELETE FROM clientes WHERE id = :id"), {"id": cliente[0]})
                                conn.commit()
                            st.success("Cliente eliminado correctamente.")
                            st.rerun()

                    if st.session_state.get(f"editando_{cliente[0]}", False):
                        with st.form(key=f"form_edit_{cliente[0]}"):
                            st.markdown("### ✏️ Editar Cliente")
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_nombre = st.text_input("Nombre", value=cliente[1])
                                nueva_empresa = st.text_input("Empresa", value=cliente[2])
                                nuevo_email = st.text_input("Email", value=cliente[3])
                            with col2:
                                nuevo_telefono = st.text_input("Teléfono", value=cliente[4])
                                nuevo_tipo = st.selectbox("Tipo", ["Pequeño", "Mediano", "Grande"],
                                    index=["Pequeño", "Mediano", "Grande"].index(cliente[5]) if cliente[5] in ["Pequeño", "Mediano", "Grande"] else 0)

                            col_g, col_c = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                engine = crear_conexion()
                                with engine.connect() as conn:
                                    conn.execute(text("""
                                        UPDATE clientes 
                                        SET nombre=:nombre, empresa=:empresa, email=:email,
                                            telefono=:telefono, tipo=:tipo
                                        WHERE id=:id
                                    """), {
                                        "nombre": nuevo_nombre,
                                        "empresa": nueva_empresa,
                                        "email": nuevo_email,
                                        "telefono": nuevo_telefono,
                                        "tipo": nuevo_tipo,
                                        "id": cliente[0]
                                    })
                                    conn.commit()
                                st.success("✅ Cliente actualizado correctamente.")
                                st.session_state[f"editando_{cliente[0]}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_{cliente[0]}"] = False
                                st.rerun()

    with tab2:
        st.subheader("➕ Agregar Nuevo Cliente")
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre *", placeholder="Ej: Juan Pérez")
            empresa = st.text_input("Empresa *", placeholder="Ej: Coca Cola")
            email = st.text_input("Email", placeholder="Ej: juan@empresa.com")
        with col2:
            telefono = st.text_input("Teléfono", placeholder="Ej: 449 123 4567")
            tipo = st.selectbox("Tipo de cliente", ["Pequeño", "Mediano", "Grande"])
            fecha_registro = st.date_input("Fecha de registro", value=date.today())

        st.markdown("---")

        if st.button("💾 Guardar Cliente", use_container_width=True):
            if nombre == "" or empresa == "":
                st.error("⚠️ Nombre y empresa son obligatorios.")
            else:
                engine = crear_conexion()
                with engine.connect() as conn:
                    conn.execute(text("""
                        INSERT INTO clientes (nombre, empresa, email, telefono, tipo, fecha_registro)
                        VALUES (:nombre, :empresa, :email, :telefono, :tipo, :fecha)
                    """), {
                        "nombre": nombre,
                        "empresa": empresa,
                        "email": email,
                        "telefono": telefono,
                        "tipo": tipo,
                        "fecha": str(fecha_registro)
                    })
                    conn.commit()
                st.success(f"✅ Cliente '{nombre}' agregado correctamente.")
                st.balloons()