import streamlit as st
from pages import clientes, proyectos, pagos, dashboard, facturas
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="HellYeah Agency", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
        [data-testid="stSidebarNav"],[data-testid="collapsedControl"] {display:none;}
        #MainMenu,footer,header {visibility:hidden;}
        * {font-family:'Montserrat',sans-serif;}
        .stApp {background:#F6F7FB;}
        section[data-testid="stSidebar"] {background:#FFFFFF !important;border-right:1px solid #E6E9EF !important;min-width:230px !important;max-width:230px !important;}
        section[data-testid="stSidebar"] * {color:#323338 !important;}
        section[data-testid="stSidebar"] > div {padding-top:0 !important;}
        .stRadio > div {gap:2px !important;}
        .stRadio > div > label {background:transparent !important;border:none !important;border-radius:8px !important;padding:9px 14px !important;color:#676879 !important;font-weight:500 !important;font-size:0.84rem !important;transition:all 0.15s !important;margin:1px 6px !important;}
        .stRadio > div > label:hover {background:#F0F0F5 !important;color:#323338 !important;}
        .stButton > button {background:#4353FF !important;color:#FFFFFF !important;font-weight:600 !important;border:none !important;border-radius:8px !important;padding:10px 20px !important;font-size:0.84rem !important;transition:all 0.2s !important;}
        .stButton > button:hover {background:#3342CC !important;box-shadow:0 4px 12px rgba(67,83,255,0.3) !important;transform:translateY(-1px) !important;}
        .stTextInput > div > div > input,.stTextArea > div > div > textarea,.stNumberInput > div > div > input {background:#FFFFFF !important;border:1px solid #C5C7D4 !important;border-radius:8px !important;color:#323338 !important;font-size:0.85rem !important;padding:9px 12px !important;}
        .stTextInput > div > div > input:focus,.stTextArea > div > div > textarea:focus {border-color:#4353FF !important;box-shadow:0 0 0 2px rgba(67,83,255,0.15) !important;}
        .stSelectbox > div > div {background:#FFFFFF !important;border:1px solid #C5C7D4 !important;border-radius:8px !important;color:#323338 !important;}
        .stTabs [data-baseweb="tab-list"] {background:transparent !important;border-bottom:2px solid #E6E9EF !important;padding:0 !important;gap:0 !important;}
        .stTabs [data-baseweb="tab"] {background:transparent !important;border-radius:0 !important;color:#676879 !important;font-weight:600 !important;font-size:0.85rem !important;padding:10px 20px !important;border-bottom:2px solid transparent !important;margin-bottom:-2px !important;}
        .stTabs [aria-selected="true"] {color:#4353FF !important;border-bottom:2px solid #4353FF !important;}
        .streamlit-expanderHeader {background:#FFFFFF !important;border:1px solid #E6E9EF !important;border-radius:10px !important;color:#323338 !important;font-weight:600 !important;}
        .streamlit-expanderContent {background:#FAFBFF !important;border:1px solid #E6E9EF !important;border-top:none !important;border-radius:0 0 10px 10px !important;}
        [data-testid="stExpander"] {border:1px solid #E6E9EF !important;border-radius:10px !important;}
        hr {border:none !important;border-top:1px solid #E6E9EF !important;}
        .block-container {padding-left:2.5rem !important;padding-right:2.5rem !important;padding-top:2rem !important;max-width:1400px !important;}
        h1,h2,h3,h4 {color:#323338 !important;font-weight:700 !important;letter-spacing:-0.3px !important;}
        p,span,div,label {color:#323338 !important;}
        .stMarkdown p {color:#676879 !important;font-size:0.88rem !important;}
    </style>
""", unsafe_allow_html=True)

cookies = EncryptedCookieManager(prefix="hellyeah_", password="hellyeah_super_secret_key_2026")
if not cookies.ready():
    st.stop()

USUARIOS = {"admin": {"password": "hellyeah2026", "nombre": "Administrador", "rol": "admin"}}

def mostrar_login():
    st.markdown("<style>.stApp{background:linear-gradient(135deg,#F6F7FB 0%,#EEF0FF 100%) !important;}</style>", unsafe_allow_html=True)
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 0.55, 1])
    with col2:
        st.markdown("""
            <div style="background:#FFFFFF;border-radius:16px;padding:40px;box-shadow:0 4px 32px rgba(0,0,0,0.08);border:1px solid #E6E9EF;text-align:center;margin-bottom:24px;">
                <img src="https://raw.githubusercontent.com/zeltbrajon01-dot/hellyeah-app/master/logo.jpeg" style="width:80px;height:80px;object-fit:cover;border-radius:16px;margin-bottom:16px;">
                <h2 style="color:#323338 !important;font-size:1.4rem;font-weight:700;margin:0 0 6px 0;">HellYeah Agency</h2>
                <p style="color:#676879 !important;font-size:0.85rem;margin:0;">Bienvenido de vuelta</p>
            </div>
        """, unsafe_allow_html=True)
        usuario = st.text_input("", placeholder="Usuario")
        password = st.text_input("", type="password", placeholder="Contraseña")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Iniciar sesión", use_container_width=True):
            if usuario in USUARIOS and USUARIOS[usuario]["password"] == password:
                for k, v in [("autenticado","true"),("usuario",usuario),("nombre",USUARIOS[usuario]["nombre"]),("rol",USUARIOS[usuario]["rol"])]:
                    cookies[k] = v
                cookies.save()
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

if cookies.get("autenticado") != "true":
    mostrar_login()
else:
    nombre = cookies.get('nombre', '')
    rol = cookies.get('rol', '').upper()

    st.sidebar.markdown(f"""
        <div style="padding:20px 16px 8px 16px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
                <img src="https://raw.githubusercontent.com/zeltbrajon01-dot/hellyeah-app/master/logo.jpeg" style="width:36px;height:36px;object-fit:cover;border-radius:8px;">
                <div>
                    <div style="font-weight:700;font-size:0.95rem;">HellYeah</div>
                    <div style="color:#676879 !important;font-size:0.65rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Agency CRM</div>
                </div>
            </div>
        </div>
        <hr style="border:none;border-top:1px solid #E6E9EF;margin:0 16px 12px 16px;">
        <div style="padding:0 16px 8px 16px;">
            <div style="font-weight:600;font-size:0.85rem;">👤 {nombre}</div>
            <div style="color:#4353FF !important;font-size:0.72rem;font-weight:600;">{rol}</div>
        </div>
        <hr style="border:none;border-top:1px solid #E6E9EF;margin:0 16px 12px 16px;">
        <p style="color:#C5C7D4 !important;font-size:0.65rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:0 22px;margin-bottom:8px;">MENÚ</p>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio("", ["📊  Panel de control","👥  Clientes","📁  Proyectos","💰  Pagos","🧾  Facturas"])

    st.sidebar.markdown("<br>" * 8, unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border:none;border-top:1px solid #E6E9EF;'>", unsafe_allow_html=True)

    if st.sidebar.button("🚪  Cerrar Sesión", use_container_width=True):
        for k in ["autenticado","usuario","nombre","rol"]:
            cookies[k] = ""
        cookies["autenticado"] = "false"
        cookies.save()
        st.rerun()

    if "Panel de control" in menu: dashboard.mostrar_dashboard()
    elif "Clientes" in menu: clientes.mostrar_clientes()
    elif "Proyectos" in menu: proyectos.mostrar_proyectos()
    elif "Pagos" in menu: pagos.mostrar_pagos()
    elif "Facturas" in menu: facturas.mostrar_facturas()