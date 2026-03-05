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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        * { font-family: 'Montserrat', sans-serif; }

        .stApp {
            background: #FAFAFA;
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #F0F0F0 !important;
            width: 240px !important;
        }

        section[data-testid="stSidebar"] > div {
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #1A1A1A !important;
        }

        .stRadio > div {
            gap: 2px !important;
        }

        .stRadio > div > label {
            background: transparent !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 11px 16px !important;
            color: #888888 !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            transition: all 0.2s ease !important;
            margin: 1px 8px !important;
        }

        .stRadio > div > label:hover {
            background: #F5F5F7 !important;
            color: #1A1A1A !important;
        }

        .stButton > button {
            background: #1A1A1A !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-size: 0.85rem !important;
            transition: all 0.3s ease !important;
            font-family: 'Montserrat', sans-serif !important;
            letter-spacing: 0.3px !important;
        }

        .stButton > button:hover {
            background: #333333 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: #FFFFFF !important;
            border: 1px solid #E8E8E8 !important;
            border-radius: 10px !important;
            color: #1A1A1A !important;
            font-family: 'Montserrat', sans-serif !important;
            padding: 10px 14px !important;
            transition: all 0.2s !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #1A1A1A !important;
            box-shadow: 0 0 0 2px rgba(0,0,0,0.08) !important;
        }

        .stSelectbox > div > div {
            background: #FFFFFF !important;
            border: 1px solid #E8E8E8 !important;
            border-radius: 10px !important;
            color: #1A1A1A !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: #F5F5F7 !important;
            border-radius: 12px !important;
            padding: 4px !important;
            gap: 2px !important;
            border: none !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 10px !important;
            color: #888888 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            font-family: 'Montserrat', sans-serif !important;
        }

        .stTabs [aria-selected="true"] {
            background: #FFFFFF !important;
            color: #1A1A1A !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        }

        .streamlit-expanderHeader {
            background: #FFFFFF !important;
            border: 1px solid #F0F0F0 !important;
            border-radius: 12px !important;
            color: #1A1A1A !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        }

        .streamlit-expanderContent {
            background: #FAFAFA !important;
            border: 1px solid #F0F0F0 !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
        }

        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #F0F0F0 !important;
            border-radius: 14px !important;
            padding: 20px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }

        hr { border-color: #F0F0F0 !important; }

        .block-container {
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            padding-top: 2.5rem !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Montserrat', sans-serif !important;
            color: #1A1A1A !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }

        p, label, div {
            color: #444444 !important;
        }

        .stMarkdown p {
            color: #444444 !important;
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
            .stApp { background: #FFFFFF !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 40px;">
                <div style="
                    width: 56px; height: 56px;
                    background: #1A1A1A;
                    border-radius: 16px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.6rem;
                    margin: 0 auto 20px auto;
                ">🔥</div>
                <h1 style="
                    font-family: 'Montserrat', sans-serif;
                    color: #1A1A1A !important;
                    font-size: 1.6rem;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                    margin: 0 0 8px 0;
                ">HellYeah Agency</h1>
                <p style="color: #AAAAAA !important; font-size: 0.85rem; margin: 0; font-weight: 400;">
                    Inicia sesión para continuar
                </p>
            </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("", placeholder="Usuario")
        password = st.text_input("", type="password", placeholder="Contraseña")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Continuar →", use_container_width=True):
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
            <p style="text-align:center; color:#CCCCCC !important; font-size:0.75rem; margin-top:20px;">
                Acceso seguro y privado
            </p>
        """, unsafe_allow_html=True)

autenticado = cookies.get("autenticado") == "true"

if not autenticado:
    mostrar_login()
else:
    nombre = cookies.get('nombre', '')
    rol = cookies.get('rol', '').upper()

    st.sidebar.markdown(f"""
        <div style="padding: 32px 20px 24px 20px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom: 32px;">
                <div style="
                    width: 32px; height: 32px;
                    background: #1A1A1A;
                    border-radius: 8px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1rem;
                ">🔥</div>
                <div>
                    <div style="font-family:'Montserrat',sans-serif; color:#1A1A1A !important; font-weight:700; font-size:0.95rem; line-height:1.2;">HellYeah</div>
                    <div style="color:#AAAAAA !important; font-size:0.65rem; font-weight:600; letter-spacing:1.5px; text-transform:uppercase;">Agency CRM</div>
                </div>
            </div>

            <div style="
                background: #F5F5F7;
                border-radius: 12px;
                padding: 12px 14px;
                margin-bottom: 28px;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <div style="
                    width: 34px; height: 34px;
                    background: #1A1A1A;
                    border-radius: 50%;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 0.9rem;
                    flex-shrink: 0;
                ">👤</div>
                <div>
                    <div style="color:#1A1A1A !important; font-weight:600; font-size:0.82rem;">{nombre}</div>
                    <div style="color:#AAAAAA !important; font-size:0.68rem; font-weight:500;">{rol}</div>
                </div>
            </div>

            <div style="color:#BBBBBB !important; font-size:0.65rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom: 8px; padding: 0 4px;">NAVEGACIÓN</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio("", [
        "📊  Panel de control",
        "👥  Clientes",
        "📁  Proyectos",
        "💰  Pagos"
    ])

    st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style="height:1px; background:#F0F0F0; margin: 0 20px 16px 20px;"></div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("← Cerrar Sesión", use_container_width=True):
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