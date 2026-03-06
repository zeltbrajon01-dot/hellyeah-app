import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_proyectos():
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h1 style="color:#323338; font-size:1.6rem; font-weight:700; letter-spacing:-0.3px; margin:0 0 4px 0;">Proyectos</h1>
            <p style="color:#676879; font-size:0.85rem; margin:0;">Gestiona los proyectos y tareas de tu agencia</p>
        </div>
        <hr style="border:none; border-top:1px solid #E6E9EF; margin:20px 0 28px 0;">
    """, unsafe_allow_html=True)

    sb = get_supabase()

    tab1, tab2 = st.tabs(["Lista de Proyectos", "Agregar Proyecto"])

    with tab1:
        proyectos = sb.table("proyectos").select("*, clientes(nombre, empresa)").order("id", desc=True).execute().data

        if not proyectos:
            st.markdown("""
                <div style="background:#FFFFFF; border-radius:12px; padding:48px; text-align:center; border:1px solid #E6E9EF;">
                    <div style="font-size:2.5rem; margin-bottom:12px;">📁</div>
                    <p style="color:#323338; font-weight:600; margin:0 0 4px 0;">No hay proyectos todavía</p>
                    <p style="color:#676879; font-size:0.85rem; margin:0;">Agrega tu primer proyecto desde la pestaña de arriba</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for proyecto in proyectos:
                cliente_nombre = proyecto["clientes"]["nombre"] if proyecto.get("clientes") else "Sin cliente"
                cliente_empresa = proyecto["clientes"]["empresa"] if proyecto.get("clientes") else ""
                color_estado = "#00C875" if proyecto["estado"] == "Completado" else "#4353FF" if proyecto["estado"] == "En Proceso" else "#FFCB00"
                icono = "✅" if proyecto["estado"] == "Completado" else "🔄" if proyecto["estado"] == "En Proceso" else "⏳"

                with st.expander(f"{icono} {proyecto['nombre']} — {cliente_empresa}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<p style='margin:4px 0;'><b>Cliente:</b> {cliente_nombre} ({cliente_empresa})</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Estado:</b> <span style='color:{color_estado}; font-weight:600;'>{proyecto['estado']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Descripción:</b> {proyecto['descripcion']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='margin:4px 0;'><b>Inicio:</b> {proyecto['fecha_inicio']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Entrega:</b> {proyecto['fecha_entrega']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Presupuesto:</b> ${proyecto['presupuesto']:,.2f}</p>", unsafe_allow_html=True)

                    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF; margin:16px 0;'>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>TAREAS</p>", unsafe_allow_html=True)

                    tareas = sb.table("tareas").select("*").eq("proyecto_id", proyecto["id"]).execute().data

                    if not tareas:
                        st.markdown("<p style='color:#676879; font-size:0.85rem;'>No hay tareas en este proyecto todavía.</p>", unsafe_allow_html=True)
                    else:
                        for tarea in tareas:
                            icono_tarea = "✅" if tarea["estado"] == "Completada" else "🔄" if tarea["estado"] == "En Proceso" else "⏳"
                            prioridad_color = "#E2445C" if tarea["prioridad"] == "Alta" else "#FFCB00" if tarea["prioridad"] == "Media" else "#00C875"
                            prioridad = tarea["prioridad"] if tarea["prioridad"] in ["Baja", "Media", "Alta"] else "Media"

                            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([3, 2, 2, 2, 1])
                            with col_t1:
                                st.markdown(f"<p style='margin:8px 0; font-weight:500;'>{icono_tarea} {tarea['nombre']}</p>", unsafe_allow_html=True)
                            with col_t2:
                                st.markdown(f"<p style='margin:8px 0; color:#676879; font-size:0.85rem;'>👤 {tarea['responsable']}</p>", unsafe_allow_html=True)
                            with col_t3:
                                st.markdown(f"<p style='margin:8px 0;'><span style='background:{prioridad_color}22; color:{prioridad_color}; padding:2px 8px; border-radius:20px; font-size:0.75rem; font-weight:600;'>{prioridad}</span></p>", unsafe_allow_html=True)
                            with col_t4:
                                nuevo_estado = st.selectbox(
                                    "",
                                    ["Pendiente", "En Proceso", "Completada"],
                                    index=["Pendiente", "En Proceso", "Completada"].index(tarea["estado"]) if tarea["estado"] in ["Pendiente", "En Proceso", "Completada"] else 0,
                                    key=f"estado_tarea_{tarea['id']}"
                                )
                                if nuevo_estado != tarea["estado"]:
                                    sb.table("tareas").update({"estado": nuevo_estado}).eq("id", tarea["id"]).execute()
                                    st.rerun()
                            with col_t5:
                                if st.button("🗑️", key=f"del_tarea_{tarea['id']}"):
                                    sb.table("tareas").delete().eq("id", tarea["id"]).execute()
                                    st.rerun()

                    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF; margin:16px 0;'>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#323338; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>AGREGAR TAREA</p>", unsafe_allow_html=True)

                    with st.form(key=f"form_tarea_{proyecto['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            nombre_tarea = st.text_input("Nombre de la tarea *", placeholder="Ej: Diseñar publicaciones")
                            responsable = st.text_input("Responsable", placeholder="Ej: María López")
                        with col2:
                            estado_tarea = st.selectbox("Estado", options=["Pendiente", "En Proceso", "Completada"], index=0, key=f"est_{proyecto['id']}")
                            prioridad = st.selectbox("Prioridad", options=["Baja", "Media", "Alta"], index=0, key=f"pri_{proyecto['id']}")
                            fecha_limite = st.date_input("Fecha límite", value=date.today(), key=f"fec_{proyecto['id']}")

                        guardar_tarea = st.form_submit_button("Guardar Tarea", use_container_width=True)

                        if guardar_tarea:
                            if nombre_tarea == "":
                                st.error("⚠️ El nombre de la tarea es obligatorio.")
                            else:
                                sb.table("tareas").insert({
                                    "proyecto_id": proyecto["id"],
                                    "nombre": nombre_tarea,
                                    "responsable": responsable,
                                    "estado": estado_tarea,
                                    "prioridad": prioridad,
                                    "fecha_limite": str(fecha_limite)
                                }).execute()
                                st.success(f"✅ Tarea '{nombre_tarea}' agregada.")
                                st.rerun()

                    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF; margin:16px 0;'>", unsafe_allow_html=True)
                    col_edit, col_del, col_empty = st.columns([1, 1, 4])

                    with col_edit:
                        if st.button("✏️ Editar", key=f"edit_proy_{proyecto['id']}"):
                            st.session_state[f"editando_proy_{proyecto['id']}"] = True
                    with col_del:
                        if st.button("🗑️ Eliminar", key=f"del_proy_{proyecto['id']}"):
                            sb.table("tareas").delete().eq("proyecto_id", proyecto["id"]).execute()
                            sb.table("proyectos").delete().eq("id", proyecto["id"]).execute()
                            st.success("Proyecto eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_proy_{proyecto['id']}", False):
                        st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)
                        with st.form(key=f"form_edit_proy_{proyecto['id']}"):
                            st.markdown("<p style='font-weight:700; color:#323338; margin-bottom:12px;'>Editar Proyecto</p>", unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_estado_proy = st.selectbox("Estado", options=["Pendiente", "En Proceso", "Completado"],
                                    index=["Pendiente", "En Proceso", "Completado"].index(proyecto["estado"]) if proyecto["estado"] in ["Pendiente", "En Proceso", "Completado"] else 0)
                                nueva_descripcion = st.text_area("Descripción", value=proyecto["descripcion"] or "")
                            with col2:
                                nuevo_presupuesto = st.number_input("Presupuesto ($)", value=float(proyecto["presupuesto"]), min_value=0.0)
                                nueva_fecha_inicio = st.date_input("Fecha de inicio")
                                nueva_fecha_entrega = st.date_input("Fecha de entrega")

                            col_g, col_c = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                sb.table("proyectos").update({
                                    "estado": nuevo_estado_proy,
                                    "presupuesto": nuevo_presupuesto,
                                    "descripcion": nueva_descripcion,
                                    "fecha_inicio": str(nueva_fecha_inicio),
                                    "fecha_entrega": str(nueva_fecha_entrega)
                                }).eq("id", proyecto["id"]).execute()
                                st.success("✅ Proyecto actualizado.")
                                st.session_state[f"editando_proy_{proyecto['id']}"] = False
                                st.rerun()
                            if cancelar:
                                st.session_state[f"editando_proy_{proyecto['id']}"] = False
                                st.rerun()

    with tab2:
        st.markdown("<p style='font-weight:700; color:#323338; font-size:1rem; margin-bottom:20px;'>Nuevo Proyecto</p>", unsafe_allow_html=True)

        clientes = sb.table("clientes").select("id, nombre, empresa").execute().data

        if not clientes:
            st.warning("⚠️ Primero debes agregar clientes antes de crear proyectos.")
        else:
            col1, col2 = st.columns(2)
            cliente_opciones = {f"{c['nombre']} — {c['empresa']}": c['id'] for c in clientes}

            with col1:
                nombre_proy = st.text_input("Nombre del proyecto *", placeholder="Ej: Campaña Redes Sociales")
                descripcion = st.text_area("Descripción", placeholder="Ej: Manejo de Instagram y Facebook")
                cliente_sel = st.selectbox("Cliente *", list(cliente_opciones.keys()))
            with col2:
                estado = st.selectbox("Estado inicial", ["Pendiente", "En Proceso", "Completado"])
                fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
                fecha_entrega = st.date_input("Fecha de entrega")
                presupuesto = st.number_input("Presupuesto ($)", min_value=0.0, step=100.0)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Guardar Proyecto", use_container_width=True):
                if nombre_proy == "":
                    st.error("⚠️ El nombre del proyecto es obligatorio.")
                else:
                    sb.table("proyectos").insert({
                        "nombre": nombre_proy,
                        "cliente_id": cliente_opciones[cliente_sel],
                        "descripcion": descripcion,
                        "estado": estado,
                        "fecha_inicio": str(fecha_inicio),
                        "fecha_entrega": str(fecha_entrega),
                        "presupuesto": presupuesto
                    }).execute()
                    st.success(f"✅ Proyecto '{nombre_proy}' creado correctamente.")
                    st.toast("✅ Proyecto creado correctamente")