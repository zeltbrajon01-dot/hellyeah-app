import streamlit as st
from pages import clientes
from pages import proyectos
from pages import pagos
from pages import dashboard
from pages import facturas
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(
    page_title="HellYeah Agency",
    page_icon="🔥",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        * { font-family: 'Montserrat', sans-serif; }

        .stApp {
            background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%) !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f1623 0%, #0a0f1a 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.06) !important;
            min-width: 220px !important;
            max-width: 220px !important;
        }

        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 0 !important;
        }

        .stRadio > div { gap: 2px !important; }

        .stRadio > div > label {
            background: transparent !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            color: rgba(255,255,255,0.6) !important;
            font-weight: 500 !important;
            font-size: 0.84rem !important;
            transition: all 0.15s ease !important;
            margin: 1px 6px !important;
        }

        .stRadio > div > label:hover {
            background: rgba(255,255,255,0.07) !important;
            color: #FFFFFF !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #2563EB, #1d4ed8) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 0.84rem !important;
            transition: all 0.2s ease !important;
            font-family: 'Montserrat', sans-serif !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
            box-shadow: 0 4px 15px rgba(37,99,235,0.4) !important;
            transform: translateY(-1px) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
            font-family: 'Montserrat', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 9px 12px !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 2px rgba(37,99,235,0.25) !important;
        }

        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: rgba(255,255,255,0.3) !important;
        }

        .stSelectbox > div > div {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 0 !important;
            color: rgba(255,255,255,0.5) !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            padding: 10px 20px !important;
            border-bottom: 2px solid transparent !important;
            margin-bottom: -1px !important;
        }

        .stTabs [aria-selected="true"] {
            background: transparent !important;
            color: #FFFFFF !important;
            border-bottom: 2px solid #2563EB !important;
        }

        .streamlit-expanderHeader {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        .streamlit-expanderContent {
            background: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important;
        }

        hr {
            border: none !important;
            border-top: 1px solid rgba(255,255,255,0.08) !important;
        }

        .block-container {
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-top: 2rem !important;
            max-width: 1400px !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Montserrat', sans-serif !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            letter-spacing: -0.3px !important;
        }

        p, span, div, label {
            color: rgba(255,255,255,0.85) !important;
            font-family: 'Montserrat', sans-serif !important;
        }

        .stMarkdown p {
            color: rgba(255,255,255,0.6) !important;
        }

        div[data-testid="stDateInput"] input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
        }

        .stAlert {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

cookies = EncryptedCookieManager(
    prefix="hellyeah_",
    password="hellyeah_super_secret_key_2026"
)

if not cookies.ready():
    st.stop()

USUARIOS = {
    "admin": {
        "password": "hellyeah2026",
        "nombre": "Administrador",
        "rol": "admin"
    }
}

def mostrar_login():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f1623 0%, #1a2744 50%, #0f1623 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.55, 1])
    with col2:
        st.markdown("""
            <div style="
                background: rgba(255,255,255,0.04);
                border-radius: 16px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
                border: 1px solid rgba(255,255,255,0.08);
                text-align: center;
                margin-bottom: 24px;
                backdrop-filter: blur(20px);
            ">
                <img src="https://raw.githubusercontent.com/zeltbrajon01-dot/hellyeah-app/master/logo.jpeg"
                    style="width:80px; height:80px; object-fit:cover; border-radius:16px; margin-bottom:16px;">
                <h2 style="color:#FFFFFF !important; font-size:1.4rem; font-weight:700; margin:0 0 6px 0;">
                    HellYeah Agency
                </h2>
                <p style="color:rgba(255,255,255,0.5) !important; font-size:0.85rem; margin:0;">
                    Bienvenido de vuelta
                </p>
            </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("", placeholder="Usuario")
        password = st.text_input("", type="password", placeholder="Contraseña")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Iniciar sesión", use_container_width=True):
            if usuario in USUARIOS and USUARIOS[usuario]["password"] == password:
                cookies["autenticado"] = "true"
                cookies["usuario"] = usuario
                cookies["nombre"] = USUARIOS[usuario]["nombre"]
                cookies["rol"] = USUARIOS[usuario]["rol"]
                cookies.save()
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

autenticado = cookies.get("autenticado") == "true"

if not autenticado:
    mostrar_login()
else:
    nombre = cookies.get('nombre', '')
    rol = cookies.get('rol', '').upper()

    st.sidebar.markdown("""
        <div style="padding:20px 16px 8px 16px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <img src="https://raw.githubusercontent.com/zeltbrajon01-dot/hellyeah-app/master/logo.jpeg"
                    style="width:36px; height:36px; object-fit:cover; border-radius:8px; flex-shrink:0;">
                <div>
                    <div style="color:#FFFFFF !important; font-weight:700; font-size:0.95rem;">HellYeah</div>
                    <div style="color:rgba(255,255,255,0.4) !important; font-size:0.65rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;">Agency CRM</div>
                </div>
            </div>
        </div>
        <hr style="border:none; border-top:1px solid rgba(255,255,255,0.08); margin:0 16px 12px 16px;">
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"👤 **{nombre}**")
    st.sidebar.markdown(f"<span style='color:#2563EB; font-size:0.75rem; font-weight:600;'>{rol}</span>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:rgba(255,255,255,0.3); font-size:0.65rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:0 8px;'>MENÚ</p>", unsafe_allow_html=True)

    menu = st.sidebar.radio("", [
        "📊  Panel de control",
        "👥  Clientes",
        "📁  Proyectos",
        "💰  Pagos",
        "🧾  Facturas"
    ])

    st.sidebar.markdown("<br>" * 8, unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    if st.sidebar.button("🚪  Cerrar Sesión", use_container_width=True):
        cookies["autenticado"] = "false"
        cookies["usuario"] = ""
        cookies["nombre"] = ""
        cookies["rol"] = ""
        cookies.save()
        st.rerun()

    if "Panel de control" in menu:
        dashboard.mostrar_dashboard()
    elif "Clientes" in menu:
        clientes.mostrar_clientes()
    elif "Proyectos" in menu:
        proyectos.mostrar_proyectos()
    elif "Pagos" in menu:
        pagos.mostrar_pagos()
    elif "Facturas" in menu:
        facturas.mostrar_facturas()