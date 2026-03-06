import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_pagos():
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h1 style="color:#323338; font-size:1.6rem; font-weight:700; letter-spacing:-0.3px; margin:0 0 4px 0;">Pagos</h1>
            <p style="color:#676879; font-size:0.85rem; margin:0;">Gestiona los pagos y finanzas de tu agencia</p>
        </div>
        <hr style="border:none; border-top:1px solid #E6E9EF; margin:20px 0 28px 0;">
    """, unsafe_allow_html=True)

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
            <div style="background:#FFFFFF; border-radius:12px; padding:20px 24px; border:1px solid #E6E9EF; border-top:3px solid #00C875; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="color:#676879; font-size:0.75rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:8px;">💵 Total Cobrado</div>
                <div style="color:#00C875; font-size:1.8rem; font-weight:700; letter-spacing:-1px;">${total_cobrado:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="background:#FFFFFF; border-radius:12px; padding:20px 24px; border:1px solid #E6E9EF; border-top:3px solid #FFCB00; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="color:#676879; font-size:0.75rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:8px;">⏳ Por Cobrar</div>
                <div style="color:#D97706; font-size:1.8rem; font-weight:700; letter-spacing:-1px;">${total_pendiente:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style="background:#FFFFFF; border-radius:12px; padding:20px 24px; border:1px solid #E6E9EF; border-top:3px solid #E2445C; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="color:#676879; font-size:0.75rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:8px;">🚨 Vencido</div>
                <div style="color:#E2445C; font-size:1.8rem; font-weight:700; letter-spacing:-1px;">${total_vencido:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Lista de Pagos", "Registrar Pago"])

    with tab1:
        filtro = st.selectbox("Filtrar por estado", ["Todos", "Pagado", "Pendiente", "Vencido"])

        if filtro == "Todos":
            pagos = sb.table("pagos").select("*, clientes(empresa), proyectos(nombre)").order("id", desc=True).execute().data
        else:
            pagos = sb.table("pagos").select("*, clientes(empresa), proyectos(nombre)").eq("estado", filtro).order("id", desc=True).execute().data

        if not pagos:
            st.markdown("""
                <div style="background:#FFFFFF; border-radius:12px; padding:48px; text-align:center; border:1px solid #E6E9EF;">
                    <div style="font-size:2.5rem; margin-bottom:12px;">💰</div>
                    <p style="color:#323338; font-weight:600; margin:0 0 4px 0;">No hay pagos todavía</p>
                    <p style="color:#676879; font-size:0.85rem; margin:0;">Registra tu primer pago desde la pestaña de arriba</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for pago in pagos:
                empresa = pago["clientes"]["empresa"] if pago.get("clientes") else "Sin cliente"
                proyecto = pago["proyectos"]["nombre"] if pago.get("proyectos") else "Sin proyecto"
                color_estado = "#00C875" if pago["estado"] == "Pagado" else "#E2445C" if pago["estado"] == "Vencido" else "#FFCB00"
                icono = "✅" if pago["estado"] == "Pagado" else "🚨" if pago["estado"] == "Vencido" else "⏳"

                with st.expander(f"{icono} {pago['concepto']} — {empresa} — ${pago['monto']:,.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<p style='margin:4px 0;'><b>Cliente:</b> {empresa}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Proyecto:</b> {proyecto}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Concepto:</b> {pago['concepto']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='margin:4px 0;'><b>Monto:</b> ${pago['monto']:,.2f}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Estado:</b> <span style='color:{color_estado}; font-weight:600;'>{pago['estado']}</span></p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Emisión:</b> {pago['fecha_emision']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Pago:</b> {pago['fecha_pago'] or 'Pendiente'}</p>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
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
                        st.markdown("<hr style='border:none; border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)
                        with st.form(key=f"form_edit_pago_{pago['id']}"):
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
        st.markdown("<p style='font-weight:700; color:#323338; font-size:1rem; margin-bottom:20px;'>Nuevo Pago</p>", unsafe_allow_html=True)

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

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Guardar Pago", use_container_width=True):
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
                    st.toast("✅ Cliente guardado correctamente")