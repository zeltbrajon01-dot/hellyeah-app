import streamlit as st
import sqlite3
from datetime import date, datetime
import os

def crear_conexion():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "hellyeah.db")
    conn = sqlite3.connect(db_path)
    return conn

def formatear_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return fecha.strftime("%d/%m/%Y")
    except:
        return fecha_str

def mostrar_proyectos():
    st.title("📁 Proyectos y Tareas")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Lista de Proyectos", "➕ Agregar Proyecto"])

    with tab1:
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, c.nombre, c.empresa, p.estado, 
                   p.fecha_inicio, p.fecha_entrega, p.presupuesto, p.descripcion
            FROM proyectos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
        """)
        proyectos = cursor.fetchall()
        conn.close()

        if len(proyectos) == 0:
            st.info("No hay proyectos registrados todavía.")
        else:
            for proyecto in proyectos:
                if proyecto[4] == "Completado":
                    icono = "✅"
                elif proyecto[4] == "En Proceso":
                    icono = "🔄"
                else:
                    icono = "⏳"

                with st.expander(f"{icono} {proyecto[1]} — Cliente: {proyecto[3]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Cliente:** {proyecto[2]} ({proyecto[3]})")
                        st.write(f"**Estado:** {proyecto[4]}")
                        st.write(f"**Descripción:** {proyecto[8]}")
                    with col2:
                        st.write(f"**Fecha inicio:** {formatear_fecha(proyecto[5])}")
                        st.write(f"**Fecha entrega:** {formatear_fecha(proyecto[6])}")
                        st.write(f"**Presupuesto:** ${proyecto[7]:,.2f}")

                    st.markdown("#### ✅ Tareas de este proyecto")
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM tareas WHERE proyecto_id = ?", (proyecto[0],))
                    tareas = cursor.fetchall()
                    conn.close()

                    if len(tareas) == 0:
                        st.info("Este proyecto no tiene tareas todavía.")
                    else:
                        for tarea in tareas:
                            if tarea[4] == "Completada":
                                icono_tarea = "✅"
                            elif tarea[4] == "En Proceso":
                                icono_tarea = "🔄"
                            else:
                                icono_tarea = "⏳"

                            prioridad_mostrar = tarea[5] if tarea[5] in ["Baja", "Media", "Alta"] else "Media"

                            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([3, 2, 2, 2, 1])
                            with col_t1:
                                st.write(f"{icono_tarea} **{tarea[2]}**")
                            with col_t2:
                                st.write(f"👤 {tarea[3]}")
                            with col_t3:
                                st.write(f"🚦 {prioridad_mostrar}")
                            with col_t4:
                                nuevo_estado = st.selectbox(
                                    "Estado",
                                    ["Pendiente", "En Proceso", "Completada"],
                                    index=["Pendiente", "En Proceso", "Completada"].index(tarea[4]) if tarea[4] in ["Pendiente", "En Proceso", "Completada"] else 0,
                                    key=f"estado_tarea_{tarea[0]}"
                                )
                                if nuevo_estado != tarea[4]:
                                    conn = crear_conexion()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", (nuevo_estado, tarea[0]))
                                    conn.commit()
                                    conn.close()
                                    st.rerun()
                            with col_t5:
                                if st.button("🗑️", key=f"del_tarea_{tarea[0]}"):
                                    conn = crear_conexion()
                                    cursor = conn.cursor()
                                    cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea[0],))
                                    conn.commit()
                                    conn.close()
                                    st.rerun()

                    st.markdown("---")
                    st.markdown(f"#### ➕ Agregar tarea a: **{proyecto[1]}**")

                    with st.form(key=f"form_tarea_{proyecto[0]}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            nombre_tarea = st.text_input("Nombre de la tarea *", placeholder="Ej: Diseñar publicaciones")
                            responsable = st.text_input("Responsable", placeholder="Ej: María López")
                        with col2:
                            estado_tarea = st.selectbox(
                                "Estado",
                                options=["Pendiente", "En Proceso", "Completada"],
                                index=0,
                                key=f"est_{proyecto[0]}"
                            )
                            prioridad = st.selectbox(
                                "Prioridad",
                                options=["Baja", "Media", "Alta"],
                                index=0,
                                key=f"pri_{proyecto[0]}"
                            )
                            fecha_limite = st.date_input(
                                "Fecha límite",
                                value=date.today(),
                                key=f"fec_{proyecto[0]}"
                            )

                        guardar_tarea = st.form_submit_button("💾 Guardar Tarea", use_container_width=True)

                        if guardar_tarea:
                            if nombre_tarea == "":
                                st.error("⚠️ El nombre de la tarea es obligatorio.")
                            else:
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("""
                                    INSERT INTO tareas (proyecto_id, nombre, responsable, estado, prioridad, fecha_limite)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (proyecto[0], nombre_tarea, responsable, estado_tarea, prioridad, str(fecha_limite)))
                                conn.commit()
                                conn.close()
                                st.success(f"✅ Tarea '{nombre_tarea}' agregada correctamente.")
                                st.rerun()

                    st.markdown("---")
                    col_edit, col_del = st.columns(2)

                    with col_edit:
                        if st.button("✏️ Editar Proyecto", key=f"edit_proy_{proyecto[0]}"):
                            st.session_state[f"editando_proy_{proyecto[0]}"] = True

                    with col_del:
                        if st.button("🗑️ Eliminar Proyecto", key=f"del_proy_{proyecto[0]}"):
                            conn = crear_conexion()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM proyectos WHERE id = ?", (proyecto[0],))
                            cursor.execute("DELETE FROM tareas WHERE proyecto_id = ?", (proyecto[0],))
                            conn.commit()
                            conn.close()
                            st.success("Proyecto eliminado correctamente.")
                            st.rerun()

                    if st.session_state.get(f"editando_proy_{proyecto[0]}", False):
                        with st.form(key=f"form_edit_proy_{proyecto[0]}"):
                            st.markdown("### ✏️ Editar Proyecto")
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_estado_proy = st.selectbox(
                                    "Estado del proyecto",
                                    options=["Pendiente", "En Proceso", "Completado"],
                                    index=["Pendiente", "En Proceso", "Completado"].index(proyecto[4]) if proyecto[4] in ["Pendiente", "En Proceso", "Completado"] else 0
                                )
                                nueva_descripcion = st.text_area("Descripción", value=proyecto[8] or "")
                            with col2:
                                nuevo_presupuesto = st.number_input("Presupuesto ($)", value=float(proyecto[7]), min_value=0.0)
                                nueva_fecha_inicio = st.date_input("Fecha de inicio", value=datetime.strptime(proyecto[5], "%Y-%m-%d").date() if proyecto[5] else date.today())
                                nueva_fecha_entrega = st.date_input("Fecha de entrega", value=datetime.strptime(proyecto[6], "%Y-%m-%d").date() if proyecto[6] else date.today())

                            col_g, col_c = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                conn = crear_conexion()
                                cursor = conn.cursor()
                                cursor.execute("""
                                    UPDATE proyectos 
                                    SET estado=?, presupuesto=?, descripcion=?, fecha_inicio=?, fecha_entrega=?
                                    WHERE id=?
                                """, (nuevo_estado_proy, nuevo_presupuesto, nueva_descripcion,
                                      str(nueva_fecha_inicio), str(nueva_fecha_entrega), proyecto[0]))
                                conn.commit()
                                conn.close()
                                st.success("✅ Proyecto actualizado correctamente.")
                                st.session_state[f"editando_proy_{proyecto[0]}"] = False
                                st.rerun()

                            if cancelar:
                                st.session_state[f"editando_proy_{proyecto[0]}"] = False
                                st.rerun()

    with tab2:
        st.subheader("➕ Agregar Nuevo Proyecto")

        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, empresa FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        if len(clientes) == 0:
            st.warning("⚠️ Primero debes agregar clientes antes de crear proyectos.")
        else:
            col1, col2 = st.columns(2)
            cliente_opciones = {f"{c[1]} — {c[2]}": c[0] for c in clientes}

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
                    conn = crear_conexion()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO proyectos (nombre, cliente_id, descripcion, estado, fecha_inicio, fecha_entrega, presupuesto)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (nombre_proy, cliente_opciones[cliente_sel], descripcion, estado,
                          str(fecha_inicio), str(fecha_entrega), presupuesto))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Proyecto '{nombre_proy}' creado correctamente.")
                    st.balloons()