import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_clientes():
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h1 style="color:#323338; font-size:1.6rem; font-weight:700; letter-spacing:-0.3px; margin:0 0 4px 0;">Clientes</h1>
            <p style="color:#676879; font-size:0.85rem; margin:0;">Gestiona tu cartera de clientes</p>
        </div>
        <hr style="border:none; border-top:1px solid #E6E9EF; margin:20px 0 28px 0;">
    """, unsafe_allow_html=True)

    sb = get_supabase()

    tab1, tab2 = st.tabs(["Lista de Clientes", "Agregar Cliente"])

    with tab1:
        clientes = sb.table("clientes").select("*").order("id", desc=True).execute().data

        if not clientes:
            st.markdown("""
                <div style="background:#FFFFFF; border-radius:12px; padding:48px; text-align:center; border:1px solid #E6E9EF;">
                    <div style="font-size:2.5rem; margin-bottom:12px;">👥</div>
                    <p style="color:#323338; font-weight:600; margin:0 0 4px 0;">No hay clientes todavía</p>
                    <p style="color:#676879; font-size:0.85rem; margin:0;">Agrega tu primer cliente desde la pestaña de arriba</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for cliente in clientes:
                with st.expander(f"👤 {cliente['nombre']} — {cliente['empresa']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<p style='margin:4px 0;'><b>Nombre:</b> {cliente['nombre']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Empresa:</b> {cliente['empresa']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Email:</b> {cliente['email']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='margin:4px 0;'><b>Teléfono:</b> {cliente['telefono']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Tipo:</b> {cliente['tipo']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Registro:</b> {cliente['fecha_registro']}</p>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_edit, col_del, col_empty = st.columns([1, 1, 4])
                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_{cliente['id']}"):
                            st.session_state[f"editando_{cliente['id']}"] = True
                    with col_del:
                        if st.button("🗑️ Eliminar", key=f"del_{cliente['id']}"):
                            sb.table("clientes").delete().eq("id", cliente['id']).execute()
                            st.success("Cliente eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_{cliente['id']}", False):
                        st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)
                        with st.form(key=f"form_edit_{cliente['id']}"):
                            st.markdown("<p style='font-weight:700; color:#323338; margin-bottom:12px;'>Editar Cliente</p>", unsafe_allow_html=True)
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
        st.markdown("<p style='font-weight:700; color:#323338; font-size:1rem; margin-bottom:20px;'>Nuevo Cliente</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre *", placeholder="Ej: Juan Pérez")
            empresa = st.text_input("Empresa *", placeholder="Ej: Coca Cola")
            email = st.text_input("Email", placeholder="Ej: juan@empresa.com")
        with col2:
            telefono = st.text_input("Teléfono", placeholder="Ej: 449 123 4567")
            tipo = st.selectbox("Tipo de cliente", ["Pequeño", "Mediano", "Grande"])
            fecha_registro = st.date_input("Fecha de registro", value=date.today())

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Guardar Cliente", use_container_width=True):
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