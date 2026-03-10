import streamlit as st
from config import get_supabase
from datetime import date

def mostrar_facturas():
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h1 style="color:#323338; font-size:1.6rem; font-weight:700; letter-spacing:-0.3px; margin:0 0 4px 0;">Facturas</h1>
            <p style="color:#676879; font-size:0.85rem; margin:0;">Sube y gestiona las facturas de tus clientes</p>
        </div>
        <hr style="border:none; border-top:1px solid #E6E9EF; margin:20px 0 28px 0;">
    """, unsafe_allow_html=True)

    sb = get_supabase()

    tab1, tab2 = st.tabs(["Lista de Facturas", "Subir Factura"])

    with tab1:
        facturas = sb.table("facturas").select("*, clientes(nombre, empresa), proyectos(nombre)").order("id", desc=True).execute().data

        if not facturas:
            st.markdown("""
                <div style="background:#FFFFFF; border-radius:12px; padding:48px; text-align:center; border:1px solid #E6E9EF;">
                    <div style="font-size:2.5rem; margin-bottom:12px;">🧾</div>
                    <p style="color:#323338; font-weight:600; margin:0 0 4px 0;">No hay facturas todavía</p>
                    <p style="color:#676879; font-size:0.85rem; margin:0;">Sube tu primera factura desde la pestaña de arriba</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for factura in facturas:
                empresa = factura["clientes"]["empresa"] if factura.get("clientes") else "Sin cliente"
                proyecto = factura["proyectos"]["nombre"] if factura.get("proyectos") else "Sin proyecto"

                with st.expander(f"🧾 {factura['concepto']} — {empresa}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<p style='margin:4px 0;'><b>Cliente:</b> {empresa}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Proyecto:</b> {proyecto}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Concepto:</b> {factura['concepto']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='margin:4px 0;'><b>Monto:</b> ${factura['monto']:,.2f}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Fecha:</b> {factura['fecha_emision']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='margin:4px 0;'><b>Archivo:</b> {factura['nombre_archivo']}</p>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_a, col_b, col_c = st.columns([2, 2, 4])
                    with col_a:
                        if factura.get("url_archivo"):
                            st.link_button("📥 Descargar PDF", factura["url_archivo"])
                    with col_b:
                        if st.button("🗑️ Eliminar", key=f"del_factura_{factura['id']}"):
                            try:
                                nombre_archivo = factura["nombre_archivo"]
                                sb.storage.from_("Facturas").remove([nombre_archivo])
                            except:
                                pass
                            sb.table("facturas").delete().eq("id", factura["id"]).execute()
                            st.success("Factura eliminada.")
                            st.rerun()

    with tab2:
        st.markdown("<p style='font-weight:700; color:#323338; font-size:1rem; margin-bottom:20px;'>Nueva Factura</p>", unsafe_allow_html=True)

        clientes = sb.table("clientes").select("id, nombre, empresa").execute().data
        proyectos = sb.table("proyectos").select("id, nombre").execute().data

        if not clientes:
            st.warning("⚠️ Primero debes agregar clientes.")
        else:
            cliente_opciones = {f"{c['nombre']} — {c['empresa']}": c['id'] for c in clientes}
            proyecto_opciones = {"Sin proyecto": None}
            proyecto_opciones.update({p['nombre']: p['id'] for p in proyectos})

            col1, col2 = st.columns(2)
            with col1:
                concepto = st.text_input("Concepto *", placeholder="Ej: Factura Marzo 2026")
                cliente_sel = st.selectbox("Cliente *", list(cliente_opciones.keys()))
                proyecto_sel = st.selectbox("Proyecto", list(proyecto_opciones.keys()))
            with col2:
                monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
                fecha_emision = st.date_input("Fecha emisión", value=date.today())
                archivo = st.file_uploader("Subir PDF *", type=["pdf"])

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Subir Factura", use_container_width=True):
                if concepto == "" or archivo is None:
                    st.error("⚠️ El concepto y el PDF son obligatorios.")
                else:
                    try:
                        nombre_archivo = f"{cliente_opciones[cliente_sel]}_{fecha_emision}_{archivo.name}"
                        contenido = archivo.read()

                        sb.storage.from_("facturas").upload(
                            path=nombre_archivo,
                            file=contenido,
                            file_options={"content-type": "application/pdf"}
                        )

                        url = sb.storage.from_("facturas").get_public_url(nombre_archivo)

                        sb.table("facturas").insert({
                            "cliente_id": cliente_opciones[cliente_sel],
                            "proyecto_id": proyecto_opciones[proyecto_sel],
                            "concepto": concepto,
                            "monto": monto,
                            "fecha_emision": str(fecha_emision),
                            "nombre_archivo": nombre_archivo,
                            "url_archivo": url
                        }).execute()

                        st.toast("✅ Factura subida correctamente")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error al subir: {e}")