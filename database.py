import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def crear_conexion():
    engine = create_engine(DATABASE_URL)
    return engine

def inicializar_db():
    engine = crear_conexion()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                empresa VARCHAR(255),
                email VARCHAR(255),
                telefono VARCHAR(50),
                tipo VARCHAR(50),
                fecha_registro DATE
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                cliente_id INTEGER REFERENCES clientes(id),
                descripcion TEXT,
                estado VARCHAR(50),
                fecha_inicio DATE,
                fecha_entrega DATE,
                presupuesto DECIMAL(10,2)
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tareas (
                id SERIAL PRIMARY KEY,
                proyecto_id INTEGER REFERENCES proyectos(id),
                nombre VARCHAR(255),
                responsable VARCHAR(255),
                estado VARCHAR(50),
                prioridad VARCHAR(50),
                fecha_limite DATE
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pagos (
                id SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES clientes(id),
                proyecto_id INTEGER REFERENCES proyectos(id),
                concepto VARCHAR(255),
                monto DECIMAL(10,2),
                estado VARCHAR(50),
                fecha_emision DATE,
                fecha_pago DATE
            )
        """))
        conn.commit()
    print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    inicializar_db()