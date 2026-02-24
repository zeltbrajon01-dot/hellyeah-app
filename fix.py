import sqlite3
import os

conn = sqlite3.connect("hellyeah.db")
cursor = conn.cursor()

# Ver todas las tareas y sus prioridades
cursor.execute("SELECT id, nombre, prioridad FROM tareas")
tareas = cursor.fetchall()
print("TAREAS ACTUALES:")
for t in tareas:
    print(t)

# Corregir todas las que no sean Baja, Media o Alta
cursor.execute("""
    UPDATE tareas 
    SET prioridad = 'Media' 
    WHERE prioridad NOT IN ('Baja', 'Media', 'Alta') 
    OR prioridad IS NULL
""")
conn.commit()
print("\nFilas corregidas:", cursor.rowcount)

# Verificar resultado
cursor.execute("SELECT id, nombre, prioridad FROM tareas")
print("\nTAREAS DESPUÉS:")
for t in cursor.fetchall():
    print(t)

conn.close()