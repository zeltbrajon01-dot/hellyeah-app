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
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

        [data-testid="stSidebarNav"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        * { font-family: 'DM Sans', sans-serif; }

        .stApp {
            background: #F7F8FC;
        }

        section[data-testid="stSidebar"] {
            background: #0F1117 !important;
            border-right: 1px solid #1E2130 !important;
            width: 260px !important;
        }

        section[data-testid="stSidebar"] > div {
            padding: 0 !important;
        }

        .stRadio > div {
            gap: 4px !important;
        }

        .stRadio > div > label {
            background: transparent !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            color: #8B8FA8 !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            transition: all 0.2s ease !important;
            margin: 2px 8px !important;
            display: flex !important;
            align-items: center !important;
        }

        .stRadio > div > label:hover {
            background: #1E2130 !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stSidebar"] .stRadio label[data-checked="true"],
        div[data-testid="stSidebar"] .stRadio input:checked + div {
            background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
            color: #FFFFFF !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-size: 0.9rem !important;
            transition: all 0.3s ease !important;
            font-family: 'DM Sans', sans-serif !important;
            letter-spacing: 0.3px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: #FFFFFF !important;
            border: 1.5px solid #E5E7EB !important;
            border-radius: 10px !important;
            color: #111827 !important;
            font-family: 'DM Sans', sans-serif !important;
            padding: 10px 14px !important;
            transition: all 0.2s !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        }

        .stSelectbox > div > div {
            background: #FFFFFF !important;
            border: 1.5px solid #E5E7EB !important;
            border-radius: 10px !important;
            color: #111827 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background: #FFFFFF !important;
            border-radius: 12px !important;
            padding: 6px !important;
            gap: 4px !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border-radius: 8px !important;
            color: #6B7280 !important;
            font-weight: 600 !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
            color: #ffffff !important;
        }

        .streamlit-expanderHeader {
            background: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            color: #111827 !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        }

        .streamlit-expanderContent {
            background: #FAFAFA !important;
            border: 1px solid #E5E7EB !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
        }

        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 14px !important;
            padding: 20px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        }

        hr { border-color: #1E2130 !important; }

        .block-container {
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-top: 2rem !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Syne', sans-serif !important;
            color: #111827 !important;
            font-weight: 700 !important;
        }

        p, label, div {
            color: #374151 !important;
        }

        .stMarkdown p {
            color: #374151 !important;
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
            .stApp { background: linear-gradient(135deg, #0F1117 0%, #1a1f35 50%, #0F1117 100%) !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.55, 1])
    with col2:
        st.markdown("""
            <div style="
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                padding: 48px 40px;
                backdrop-filter: blur(20px);
                text-align: center;
                margin-bottom: 24px;
            ">
                <div style="font-size: 3rem; margin-bottom: 8px;">🔥</div>
                <h1 style="
                    font-family: 'Syne', sans-serif;
                    color: #FFFFFF !important;
                    font-size: 1.8rem;
                    font-weight: 800;
                    margin: 0 0 6px 0;
                ">HellYeah Agency</h1>
                <p style="color: #6B7280 !important; font-size: 0.9rem; margin: 0 0 32px 0;">
                    Panel de administración
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <style>
                .login-input .stTextInput > div > div > input {
                    background: rgba(255,255,255,0.05) !important;
                    border: 1px solid rgba(255,255,255,0.1) !important;
                    color: white !important;
                    border-radius: 10px !important;
                }
            </style>
        """, unsafe_allow_html=True)

        usuario = st.text_input("", placeholder="👤 Usuario")
        password = st.text_input("", type="password", placeholder="🔒 Contraseña")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Iniciar sesión →", use_container_width=True):
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
    st.sidebar.markdown("""
        <div style="padding: 28px 20px 16px 20px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.8rem;">🔥</span>
                <div>
                    <div style="font-family:'Syne',sans-serif; color:#FFFFFF; font-weight:800; font-size:1.1rem; line-height:1.2;">HellYeah</div>
                    <div style="color:#6366F1; font-size:0.75rem; font-weight:600; letter-spacing:1px;">AGENCY CRM</div>
                </div>
            </div>
        </div>
        <div style="height:1px; background:linear-gradient(90deg, #6366F1, transparent); margin: 0 20px 20px 20px;"></div>
    """, unsafe_allow_html=True)

    nombre = cookies.get('nombre', '')
    rol = cookies.get('rol', '').upper()

    st.sidebar.markdown(f"""
        <div style="
            margin: 0 12px 20px 12px;
            background: #1E2130;
            border-radius: 12px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <div style="
                width: 38px; height: 38px;
                background: linear-gradient(135deg, #6366F1, #8B5CF6);
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 1rem;
                flex-shrink: 0;
            ">👤</div>
            <div>
                <div style="color:#FFFFFF; font-weight:600; font-size:0.85rem;">{nombre}</div>
                <div style="color:#6366F1; font-size:0.7rem; font-weight:600;">{rol}</div>
            </div>
        </div>

        <div style="padding: 0 12px; margin-bottom: 8px;">
            <div style="color:#4B5563; font-size:0.7rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding: 0 8px; margin-bottom: 8px;">MENÚ PRINCIPAL</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio("", [
        "📊  Panel de control",
        "👥  Clientes",
        "📁  Proyectos",
        "💰  Pagos"
    ])

    st.sidebar.markdown("<br>" * 8, unsafe_allow_html=True)
    st.sidebar.markdown("<div style='height:1px; background:#1E2130; margin: 0 12px 16px 12px;'></div>", unsafe_allow_html=True)

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