import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_clientes():
    st.title("👥 Gestión de Clientes")
    st.markdown("---")

    sb = get_supabase()

    tab1, tab2 = st.tabs(["📋 Lista de Clientes", "➕ Agregar Cliente"])

    with tab1:
        clientes = sb.table("clientes").select("*").order("id", desc=True).execute().data

        if not clientes:
            st.info("No hay clientes registrados todavía.")
        else:
            for cliente in clientes:
                with st.expander(f"👤 {cliente['nombre']} — {cliente['empresa']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nombre:** {cliente['nombre']}")
                        st.write(f"**Empresa:** {cliente['empresa']}")
                        st.write(f"**Email:** {cliente['email']}")
                    with col2:
                        st.write(f"**Teléfono:** {cliente['telefono']}")
                        st.write(f"**Tipo:** {cliente['tipo']}")
                        st.write(f"**Fecha registro:** {cliente['fecha_registro']}")

                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{cliente['id']}"):
                            st.session_state[f"editando_{cliente['id']}"] = True
                    with col_del:
                        if st.button("🗑️ Eliminar", key=f"del_{cliente['id']}"):
                            sb.table("clientes").delete().eq("id", cliente['id']).execute()
                            st.success("Cliente eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_{cliente['id']}", False):
                        with st.form(key=f"form_edit_{cliente['id']}"):
                            st.markdown("### ✏️ Editar Cliente")
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_nombre = st.text_input("Nombre", value=cliente['nombre'])
                                nueva_empresa = st.text_input("Empresa", value=cliente['empresa'])
                                nuevo_email = st.text_input("Email", value=cliente['email'])
                            with col2:
                                nuevo_telefono = st.text_input("Teléfono", value=cliente['telefono'])
                                nuevo_tipo = st.selectbox("Tipo", ["Pequeño", "Mediano", "Grande"],
                                    index=["Pequeño", "Mediano", "Grande"].index(cliente['tipo']) if cliente['tipo'] in ["Pequeño", "Mediano", "Grande"] else 0)

                            col_g, col_c = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                sb.table("clientes").update({
                                    "nombre": nuevo_nombre,
                                    "empresa": nueva_empresa,
                                    "email": nuevo_email,
                                    "telefono": nuevo_telefono,
                                    "tipo": nuevo_tipo
                                }).eq("id", cliente['id']).execute()
                                st.success("✅ Cliente actualizado.")
                                st.session_state[f"editando_{cliente['id']}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_{cliente['id']}"] = False
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
                sb.table("clientes").insert({
                    "nombre": nombre,
                    "empresa": empresa,
                    "email": email,
                    "telefono": telefono,
                    "tipo": tipo,
                    "fecha_registro": str(fecha_registro)
                }).execute()
                st.success(f"✅ Cliente '{nombre}' agregado correctamente.")
                st.balloons()