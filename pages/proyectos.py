import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_proyectos():
    st.title("📁 Proyectos y Tareas")
    st.markdown("---")

    sb = get_supabase()

    tab1, tab2 = st.tabs(["📋 Lista de Proyectos", "➕ Agregar Proyecto"])

    with tab1:
        proyectos = sb.table("proyectos").select("*, clientes(nombre, empresa)").order("id", desc=True).execute().data

        if not proyectos:
            st.info("No hay proyectos registrados todavía.")
        else:
            for proyecto in proyectos:
                cliente_nombre = proyecto["clientes"]["nombre"] if proyecto.get("clientes") else "Sin cliente"
                cliente_empresa = proyecto["clientes"]["empresa"] if proyecto.get("clientes") else ""
                icono = "✅" if proyecto["estado"] == "Completado" else "🔄" if proyecto["estado"] == "En Proceso" else "⏳"

                with st.expander(f"{icono} {proyecto['nombre']} — Cliente: {cliente_empresa}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Cliente:** {cliente_nombre} ({cliente_empresa})")
                        st.write(f"**Estado:** {proyecto['estado']}")
                        st.write(f"**Descripción:** {proyecto['descripcion']}")
                    with col2:
                        st.write(f"**Fecha inicio:** {proyecto['fecha_inicio']}")
                        st.write(f"**Fecha entrega:** {proyecto['fecha_entrega']}")
                        st.write(f"**Presupuesto:** ${proyecto['presupuesto']:,.2f}")

                    st.markdown("#### ✅ Tareas de este proyecto")
                    tareas = sb.table("tareas").select("*").eq("proyecto_id", proyecto["id"]).execute().data

                    if not tareas:
                        st.info("Este proyecto no tiene tareas todavía.")
                    else:
                        for tarea in tareas:
                            icono_tarea = "✅" if tarea["estado"] == "Completada" else "🔄" if tarea["estado"] == "En Proceso" else "⏳"
                            prioridad_mostrar = tarea["prioridad"] if tarea["prioridad"] in ["Baja", "Media", "Alta"] else "Media"

                            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([3, 2, 2, 2, 1])
                            with col_t1:
                                st.write(f"{icono_tarea} **{tarea['nombre']}**")
                            with col_t2:
                                st.write(f"👤 {tarea['responsable']}")
                            with col_t3:
                                st.write(f"🚦 {prioridad_mostrar}")
                            with col_t4:
                                nuevo_estado = st.selectbox(
                                    "Estado",
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

                    st.markdown("---")
                    st.markdown(f"#### ➕ Agregar tarea a: **{proyecto['nombre']}**")

                    with st.form(key=f"form_tarea_{proyecto['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            nombre_tarea = st.text_input("Nombre de la tarea *", placeholder="Ej: Diseñar publicaciones")
                            responsable = st.text_input("Responsable", placeholder="Ej: María López")
                        with col2:
                            estado_tarea = st.selectbox("Estado", options=["Pendiente", "En Proceso", "Completada"], index=0, key=f"est_{proyecto['id']}")
                            prioridad = st.selectbox("Prioridad", options=["Baja", "Media", "Alta"], index=0, key=f"pri_{proyecto['id']}")
                            fecha_limite = st.date_input("Fecha límite", value=date.today(), key=f"fec_{proyecto['id']}")

                        guardar_tarea = st.form_submit_button("💾 Guardar Tarea", use_container_width=True)

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

                    st.markdown("---")
                    col_edit, col_del = st.columns(2)

                    with col_edit:
                        if st.button("✏️ Editar Proyecto", key=f"edit_proy_{proyecto['id']}"):
                            st.session_state[f"editando_proy_{proyecto['id']}"] = True

                    with col_del:
                        if st.button("🗑️ Eliminar Proyecto", key=f"del_proy_{proyecto['id']}"):
                            sb.table("tareas").delete().eq("proyecto_id", proyecto["id"]).execute()
                            sb.table("proyectos").delete().eq("id", proyecto["id"]).execute()
                            st.success("Proyecto eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_proy_{proyecto['id']}", False):
                        with st.form(key=f"form_edit_proy_{proyecto['id']}"):
                            st.markdown("### ✏️ Editar Proyecto")
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
        st.subheader("➕ Agregar Nuevo Proyecto")

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

            st.markdown("---")

            if st.button("💾 Guardar Proyecto", use_container_width=True):
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
                    st.balloons()