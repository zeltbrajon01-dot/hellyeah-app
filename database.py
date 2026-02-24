import sqlite3

def crear_conexion():
    conn = sqlite3.connect("hellyeah.db")
    return conn

def crear_tablas():
    conn = crear_conexion()
    cursor = conn.cursor()

    # Tabla de Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT,
            email TEXT,
            telefono TEXT,
            tipo TEXT,
            fecha_registro TEXT
        )
    """)

    # Tabla de Proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cliente_id INTEGER,
            descripcion TEXT,
            estado TEXT,
            fecha_inicio TEXT,
            fecha_entrega TEXT,
            presupuesto REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # Tabla de Tareas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proyecto_id INTEGER,
            nombre TEXT NOT NULL,
            responsable TEXT,
            estado TEXT,
            prioridad TEXT,
            fecha_limite TEXT,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    # Tabla de Pagos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            proyecto_id INTEGER,
            concepto TEXT,
            monto REAL,
            estado TEXT,
            fecha_emision TEXT,
            fecha_pago TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    conn.commit()
    conn.close()

# Esto crea las tablas automaticamente cuando se ejecuta
crear_tablas()