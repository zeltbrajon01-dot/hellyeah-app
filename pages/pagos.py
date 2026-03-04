import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_pagos():
    st.title("💰 Gestión de Pagos")
    st.markdown("---")

    sb = get_supabase()

    pagos_cobrados = sb.table("pagos").select("monto").eq("estado", "Pagado").execute().data
    total_cobrado = sum([p["monto"] for p in pagos_cobrados]) if pagos_cobrados else 0

    pagos_pendientes = sb.table("pagos").select("monto").eq("estado", "Pendiente").execute().data
    total_pendiente = sum([p["monto"] for p in pagos_pendientes]) if pagos_pendientes else 0

    pagos_vencidos = sb.table("pagos").select("monto").eq("estado", "Vencido").execute().data
    total_vencido = sum([p["monto"] for p in pagos_vencidos]) if pagos_vencidos else 0

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

        if filtro == "Todos":
            pagos = sb.table("pagos").select("*, clientes(empresa), proyectos(nombre)").order("id", desc=True).execute().data
        else:
            pagos = sb.table("pagos").select("*, clientes(empresa), proyectos(nombre)").eq("estado", filtro).order("id", desc=True).execute().data

        if not pagos:
            st.info("No hay pagos registrados todavía.")
        else:
            for pago in pagos:
                empresa = pago["clientes"]["empresa"] if pago.get("clientes") else "Sin cliente"
                proyecto = pago["proyectos"]["nombre"] if pago.get("proyectos") else "Sin proyecto"
                icono = "✅" if pago["estado"] == "Pagado" else "🚨" if pago["estado"] == "Vencido" else "⏳"

                with st.expander(f"{icono} {pago['concepto']} — {empresa} — ${pago['monto']:,.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Cliente:** {empresa}")
                        st.write(f"**Proyecto:** {proyecto}")
                        st.write(f"**Concepto:** {pago['concepto']}")
                    with col2:
                        st.write(f"**Monto:** ${pago['monto']:,.2f}")
                        st.write(f"**Estado:** {pago['estado']}")
                        st.write(f"**Fecha emisión:** {pago['fecha_emision']}")
                        st.write(f"**Fecha pago:** {pago['fecha_pago'] or 'Pendiente'}")

                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        if st.button("✅ Pagado", key=f"pagado_{pago['id']}"):
                            sb.table("pagos").update({"estado": "Pagado", "fecha_pago": str(date.today())}).eq("id", pago['id']).execute()
                            st.rerun()
                    with col_b:
                        if st.button("🚨 Vencido", key=f"vencido_{pago['id']}"):
                            sb.table("pagos").update({"estado": "Vencido"}).eq("id", pago['id']).execute()
                            st.rerun()
                    with col_c:
                        if st.button("✏️ Editar", key=f"edit_pago_{pago['id']}"):
                            st.session_state[f"editando_pago_{pago['id']}"] = True
                    with col_d:
                        if st.button("🗑️ Eliminar", key=f"del_pago_{pago['id']}"):
                            sb.table("pagos").delete().eq("id", pago['id']).execute()
                            st.success("Pago eliminado.")
                            st.rerun()

                    if st.session_state.get(f"editando_pago_{pago['id']}", False):
                        with st.form(key=f"form_edit_pago_{pago['id']}"):
                            st.markdown("### ✏️ Editar Pago")
                            col1, col2 = st.columns(2)
                            with col1:
                                nuevo_concepto = st.text_input("Concepto", value=pago['concepto'])
                                nuevo_monto = st.number_input("Monto", value=float(pago['monto']), min_value=0.0)
                            with col2:
                                nuevo_estado = st.selectbox("Estado", ["Pendiente", "Pagado", "Vencido"],
                                    index=["Pendiente", "Pagado", "Vencido"].index(pago['estado']) if pago['estado'] in ["Pendiente", "Pagado", "Vencido"] else 0)

                            col_g, col_c2 = st.columns(2)
                            with col_g:
                                guardar = st.form_submit_button("💾 Guardar", use_container_width=True)
                            with col_c2:
                                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

                            if guardar:
                                sb.table("pagos").update({
                                    "concepto": nuevo_concepto,
                                    "monto": nuevo_monto,
                                    "estado": nuevo_estado
                                }).eq("id", pago['id']).execute()
                                st.success("✅ Pago actualizado.")
                                st.session_state[f"editando_pago_{pago['id']}"] = False
                                st.rerun()
                            if cancelar:
                                st.session_state[f"editando_pago_{pago['id']}"] = False
                                st.rerun()

    with tab2:
        st.subheader("➕ Registrar Nuevo Pago")

        clientes = sb.table("clientes").select("id, nombre, empresa").execute().data
        proyectos = sb.table("proyectos").select("id, nombre").execute().data

        if not clientes:
            st.warning("⚠️ Primero debes agregar clientes.")
        else:
            col1, col2 = st.columns(2)
            cliente_opciones = {f"{c['nombre']} — {c['empresa']}": c['id'] for c in clientes}
            proyecto_opciones = {"Sin proyecto": None}
            proyecto_opciones.update({p['nombre']: p['id'] for p in proyectos})

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
                    sb.table("pagos").insert({
                        "cliente_id": cliente_opciones[cliente_sel],
                        "proyecto_id": proyecto_opciones[proyecto_sel],
                        "concepto": concepto,
                        "monto": monto,
                        "estado": estado,
                        "fecha_emision": str(fecha_emision),
                        "fecha_pago": str(fecha_pago)
                    }).execute()
                    st.success("✅ Pago registrado correctamente.")
                    st.balloons()