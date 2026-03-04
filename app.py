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
            background-color: #0a0a0a;
        }
        section[data-testid="stSidebar"] {
            background: #1a1a1a !important;
            border-right: 2px solid #C6FF00 !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #C6FF00, #a8d900);
            color: #000000;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #d4ff33, #C6FF00);
            transform: translateY(-1px);
            box-shadow: 0 4px 15px #C6FF0044;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #1a1a1a;
            border: 1px solid #C6FF0033;
            border-radius: 8px;
            color: white;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #C6FF00;
            box-shadow: 0 0 0 1px #C6FF00;
        }
        .stSelectbox > div > div {
            background-color: #1a1a1a;
            border: 1px solid #C6FF0033;
            border-radius: 8px;
            color: white;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #111111;
            border-radius: 10px;
            padding: 4px;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: #aaa;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #C6FF00, #a8d900) !important;
            color: #000000 !important;
        }
        .streamlit-expanderHeader {
            background-color: #1a1a1a;
            border: 1px solid #C6FF0022;
            border-radius: 10px;
            color: white;
        }
        .streamlit-expanderContent {
            background-color: #111111;
            border: 1px solid #C6FF0011;
            border-radius: 0 0 10px 10px;
        }
        .stRadio > div {
            gap: 8px;
        }
        .stRadio > div > label {
            background-color: #1a1a1a;
            border: 1px solid #C6FF0022;
            border-radius: 8px;
            padding: 8px 12px;
            color: white;
            transition: all 0.2s;
        }
        .stRadio > div > label:hover {
            border-color: #C6FF00;
            color: #C6FF00;
        }
        [data-testid="stMetric"] {
            background-color: #1a1a1a;
            border: 1px solid #C6FF0022;
            border-radius: 12px;
            padding: 15px;
        }
        hr {
            border-color: #C6FF0022;
        }
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1.5rem;
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

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        try:
            from PIL import Image
            import os
            logo_paths = ["logo.jpeg", "/mount/src/hellyeah-app/logo.jpeg"]
            for path in logo_paths:
                if os.path.exists(path):
                    logo = Image.open(path)
                    st.image(logo, use_container_width=True)
                    break
            else:
                st.markdown("<h2 style='text-align:center; color:#C6FF00;'>🔥 HellYeah</h2>", unsafe_allow_html=True)
        except:
            st.markdown("<h2 style='text-align:center; color:#C6FF00;'>🔥 HellYeah</h2>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
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
            <p style="text-align:center; color:#555; font-size:0.75rem; margin-top:15px;">
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
            st.sidebar.markdown("<h2 style='color:#C6FF00;'>🔥 HellYeah Agency</h2>", unsafe_allow_html=True)
    except:
        st.sidebar.markdown("<h2 style='color:#C6FF00;'>🔥 HellYeah Agency</h2>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #C6FF0011, #C6FF0022);
            border-left: 3px solid #C6FF00;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
        ">
            <div style="color: #aaa; font-size: 0.75rem;">Conectado como</div>
            <div style="color: white; font-weight: bold;">👤 {cookies.get('nombre')}</div>
            <div style="color: #C6FF00; font-size: 0.8rem;">🛡️ {cookies.get('rol', '').upper()}</div>
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