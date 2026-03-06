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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&display=swap');

        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        html, body, * {
            font-family: 'Montserrat', sans-serif !important;
        }

        .stApp {
            background: #F6F7FB !important;
        }

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E6E9EF !important;
            min-width: 230px !important;
            max-width: 230px !important;
        }

        section[data-testid="stSidebar"] * {
            color: #323338 !important;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 0 !important;
        }

        .stRadio > div {
            gap: 2px !important;
        }

        .stRadio > div > label {
            background: transparent !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 9px 14px !important;
            color: #676879 !important;
            font-weight: 500 !important;
            font-size: 0.84rem !important;
            transition: all 0.15s ease !important;
            margin: 1px 6px !important;
            cursor: pointer !important;
        }

        .stRadio > div > label:hover {
            background: #F0F0F5 !important;
            color: #323338 !important;
        }

        div[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
            background: #EEF0FF !important;
            color: #4353FF !important;
            font-weight: 600 !important;
        }

        .stButton > button {
            background: #4353FF !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 0.84rem !important;
            transition: all 0.2s ease !important;
            font-family: 'Montserrat', sans-serif !important;
            letter-spacing: 0.2px !important;
        }

        .stButton > button:hover {
            background: #3342CC !important;
            box-shadow: 0 4px 12px rgba(67,83,255,0.3) !important;
            transform: translateY(-1px) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: #FFFFFF !important;
            border: 1px solid #C5C7D4 !important;
            border-radius: 8px !important;
            color: #323338 !important;
            font-family: 'Montserrat', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 9px 12px !important;
            transition: all 0.2s !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4353FF !important;
            box-shadow: 0 0 0 2px rgba(67,83,255,0.15) !important;
        }

        .stSelectbox > div > div {
            background: #FFFFFF !important;
            border: 1px solid #C5C7D4 !important;
            border-radius: 8px !important;
            color: #323338 !important;
            font-size: 0.85rem !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: transparent !important;
            border-bottom: 2px solid #E6E9EF !important;
            border-radius: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 0 !important;
            color: #676879 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            padding: 10px 20px !important;
            border-bottom: 2px solid transparent !important;
            margin-bottom: -2px !important;
        }

        .stTabs [aria-selected="true"] {
            background: transparent !important;
            color: #4353FF !important;
            border-bottom: 2px solid #4353FF !important;
        }

        .streamlit-expanderHeader {
            background: #FFFFFF !important;
            border: 1px solid #E6E9EF !important;
            border-radius: 10px !important;
            color: #323338 !important;
            font-weight: 600 !important;
            font-size: 0.87rem !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        }

        .streamlit-expanderContent {
            background: #FAFBFF !important;
            border: 1px solid #E6E9EF !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }
[title] {
            pointer-events: none !important;
        }

        [data-testid="stSidebar"] [title] {
            display: none !important;
        }

        tooltip, [role="tooltip"] {
            display: none !important;
        }
        hr {
            border: none !important;
            border-top: 1px solid #E6E9EF !important;
        }

        .block-container {
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-top: 2rem !important;
            max-width: 1400px !important;
        }

        h1, h2, h3, h4, h5 {
            font-family: 'Montserrat', sans-serif !important;
            color: #323338 !important;
            font-weight: 700 !important;
            letter-spacing: -0.3px !important;
        }

        p, span, div, label {
            color: #323338 !important;
            font-family: 'Montserrat', sans-serif !important;
        }

        .stMarkdown p {
            color: #676879 !important;
            font-size: 0.88rem !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid #E6E9EF !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
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
                background: linear-gradient(135deg, #F6F7FB 0%, #EEF0FF 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.55, 1])
    with col2:
        st.markdown("""
            <div style="
                background: #FFFFFF;
                border-radius: 16px;
                padding: 48px 40px 40px 40px;
                box-shadow: 0 4px 32px rgba(0,0,0,0.08);
                border: 1px solid #E6E9EF;
                text-align: center;
                margin-bottom: 24px;
            ">
                <div style="
                    width: 52px; height: 52px;
                    background: linear-gradient(135deg, #4353FF, #6B5BFF);
                    border-radius: 14px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.5rem;
                    margin: 0 auto 20px auto;
                ">🔥</div>
                <h2 style="
                    color: #323338 !important;
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin: 0 0 6px 0;
                    letter-spacing: -0.3px;
                ">HellYeah Agency</h2>
                <p style="color: #676879 !important; font-size: 0.85rem; margin: 0 0 28px 0;">
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

    st.sidebar.markdown(f"""
        <div style="padding: 24px 16px 16px 16px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom: 24px;">
                <div style="
                    width: 34px; height: 34px;
                    background: linear-gradient(135deg, #4353FF, #6B5BFF);
                    border-radius: 10px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    flex-shrink: 0;
                ">🔥</div>
                <div>
                    <div style="color:#323338 !important; font-weight:700; font-size:0.95rem; line-height:1.3;">HellYeah</div>
                    <div style="color:#676879 !important; font-size:0.65rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;">Agency CRM</div>
                </div>
            </div>

            <div style="
                background: #F6F7FB;
                border-radius: 10px;
                padding: 10px 12px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                border: 1px solid #E6E9EF;
            ">
                <div style="
                    width: 30px; height: 30px;
                    background: linear-gradient(135deg, #4353FF, #6B5BFF);
                    border-radius: 50%;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 0.8rem;
                    flex-shrink: 0;
                    color: white;
                    font-weight: 700;
                ">{nombre[0] if nombre else 'A'}</div>
                <div>
                    <div style="color:#323338 !important; font-weight:600; font-size:0.82rem;">{nombre}</div>
                    <div style="color:#676879 !important; font-size:0.68rem;">{rol}</div>
                </div>
            </div>

            <div style="color:#C5C7D4 !important; font-size:0.65rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom: 6px; padding: 0 8px;">MENÚ</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio("", [
        "📊  Panel de control",
        "👥  Clientes",
        "📁  Proyectos",
        "💰  Pagos"
    ])

    st.sidebar.markdown("<br>" * 12, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style="height:1px; background:#E6E9EF; margin: 0 16px 12px 16px;"></div>
    """, unsafe_allow_html=True)

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