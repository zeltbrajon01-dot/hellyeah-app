import os
import streamlit as st

def get_database_url():
    try:
        return st.secrets["DATABASE_URL"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("DATABASE_URL")