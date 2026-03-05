import streamlit as st
from pages import clientes
from pages import proyectos
from pages import pagos
from pages import dashboard
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(
    page_title="HellYeah Agency",
    page_icon="🔥",
    layout="wide"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background-color: #f4f6f9;
        }

        section[data-testid="stSidebar"] {
            background: #1a2332 !important;
            border-right: none !important;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stRadio > div > label {
            background-color: transparent !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            color: #adb5bd !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:hover {
            background-color: #2d3f55 !important;
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
            background-color: #2d3f55 !important;
            color: #ffffff !important;
            border-left: 3px solid #4A90D9 !important;
        }

        .stButton > button {
            background: #4A90D9;
            color: #ffffff;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: #357abd;
            box-shadow: 0 2px 8px rgba(74,144,217,0.4);
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            color: #333333;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4A90D9;
            box-shadow: 0 0 0 2px rgba(74,144,217,0.2);
        }

        .stSelectbox > div > div {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            color: #333333;
        }

        .stTabs [data-baseweb="tab-list"] {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 4px;
            gap: 4px;
            border: 1px solid #dee2e6;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 6px;
            color: #666;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background: #4A90D9 !important;
            color: #ffffff !important;
        }

        .streamlit-expanderHeader {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            color: #333333;
        }

        .streamlit-expanderContent {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0 0 8px 8px;
        }

        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }

        hr {
            border-color: #dee2e6;
        }

        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1.5rem;
        }

        h1, h2, h3, h4 {
            color: #1a2332 !important;
        }

        p, label, div {
            color: #333333;
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
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        st.markdown("""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
            ">
                <h2 style="color:#1a2332; margin-bottom:5px;">🔥 HellYeah Agency</h2>
                <p style="color:#888; margin-bottom:25px;">Inicia sesión para continuar</p>
            </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuario", placeholder="Tu usuario")
        password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Ingresar →", use_container_width=True):
            if usuario in USUARIOS and USUARIOS[usuario]["password"] == password:
                cookies["autenticado"] = "true"
                cookies["usuario"] = usuario
                cookies["nombre"] = USUARIOS[usuario]["nombre"]
                cookies["rol"] = USUARIOS[usuario]["rol"]
                cookies.save()
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

        st.markdown("""
            <p style="text-align:center; color:#aaa; font-size:0.75rem; margin-top:15px;">
                🔒 Acceso seguro y privado
            </p>
        """, unsafe_allow_html=True)

autenticado = cookies.get("autenticado") == "true"

if not autenticado:
    mostrar_login()
else:
    try:
        from PIL import Image
        import os
        logo_paths = ["logo.jpeg", "/mount/src/hellyeah-app/logo.jpeg"]
        for path in logo_paths:
            if os.path.exists(path):
                logo = Image.open(path)
                st.sidebar.image(logo, use_container_width=True)
                break
        else:
            st.sidebar.markdown("<h2 style='color:#ffffff; text-align:center;'>🔥 HellYeah</h2>", unsafe_allow_html=True)
    except:
        st.sidebar.markdown("<h2 style='color:#ffffff; text-align:center;'>🔥 HellYeah</h2>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    st.sidebar.markdown(f"""
        <div style="
            background: #2d3f55;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
        ">
            <div style="color: #adb5bd; font-size: 0.75rem;">Conectado como</div>
            <div style="color: white; font-weight: bold;">👤 {cookies.get('nombre')}</div>
            <div style="color: #4A90D9; font-size: 0.8rem;">🛡️ {cookies.get('rol', '').upper()}</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    menu = st.sidebar.radio("Navegación", [
        "📊 Panel de control",
        "👥 Clientes",
        "📁 Proyectos",
        "💰 Pagos"
    ])

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        cookies["autenticado"] = "false"
        cookies["usuario"] = ""
        cookies["nombre"] = ""
        cookies["rol"] = ""
        cookies.save()
        st.rerun()

    if menu == "📊 Panel de control":
        dashboard.mostrar_dashboard()
    elif menu == "👥 Clientes":
        clientes.mostrar_clientes()
    elif menu == "📁 Proyectos":
        proyectos.mostrar_proyectos()
    elif menu == "💰 Pagos":
        pagos.mostrar_pagos()