#!/usr/bin/env python3
"""
Script para importar datos CSV a MongoDB
"""
import csv
import os
from pymongo import MongoClient
from bson import ObjectId

def import_csv_to_mongodb():
    """
    Importa los datos de los archivos CSV a MongoDB
    """
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mi_db']
    
    # Limpiar colecciones existentes
    db.proyectos.drop()
    db.tareas.drop()
    db.responsables.drop()
    db.estados_tarea.drop()
    db.tipo_documento.drop()
    
    print("Importando datos a MongoDB...")
    
    # Importar proyectos
    print("Importando proyectos...")
    with open('collections/proyecto.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        proyectos = []
        for row in reader:
            proyecto = {
                '_id': int(row['_id']),
                'nombre_proyecto': row['nombre_proyecto'],
                'fecha_inicio': row['fecha_inicio'],
                'fecha_fin': row['fecha_fin'],
                'descripcion_proyecto': row['descripcion_proyecto'],
                'costo': int(row['costo'])
            }
            proyectos.append(proyecto)
        db.proyectos.insert_many(proyectos)
        print(f"[OK] {len(proyectos)} proyectos importados")
    
    # Importar responsables
    print("Importando responsables...")
    with open('collections/responsable.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        responsables = []
        for row in reader:
            responsable = {
                '_id': int(row['_id']),
                'documento': row['documento'],
                'tipo_documento': int(row['tipo_documento']),
                'nombre_responsable': row['nombre_responsable'],
                'apellido_responsable': row['apellido_responsable'],
                'edad': int(row['edad']),
                'celular': row['celular'],
                'correo': row['correo'],
                'profesion': row['profesion'],
                'cargo': row['cargo']
            }
            responsables.append(responsable)
        db.responsables.insert_many(responsables)
        print(f"[OK] {len(responsables)} responsables importados")
    
    # Importar estados de tarea
    print("Importando estados de tarea...")
    with open('collections/estado_tarea.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        estados = []
        for row in reader:
            estado = {
                '_id': int(row['_id']),
                'estado_tarea': row['estado_tarea']
            }
            estados.append(estado)
        db.estados_tarea.insert_many(estados)
        print(f"[OK] {len(estados)} estados importados")
    
    # Importar tipos de documento
    print("Importando tipos de documento...")
    with open('collections/tipo_documento.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tipos = []
        for row in reader:
            tipo = {
                '_id': int(row['_id']),
                'tipo_documento': row['tipo_documento']
            }
            tipos.append(tipo)
        db.tipo_documento.insert_many(tipos)
        print(f"[OK] {len(tipos)} tipos de documento importados")
    
    # Importar tareas
    print("Importando tareas...")
    with open('collections/tarea.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tareas = []
        for row in reader:
            tarea = {
                '_id': int(row['_id']),
                'nombre_tarea': row['nombre_tarea'],
                'fecha_inicio': row['fecha_inicio'],
                'fecha_fin': row['fecha_fin'],
                'id_proyecto': int(row['id_proyecto']),
                'id_responsable': int(row['id_responsable']),
                'id_estado_tarea': int(row['id_estado_tarea']),
                'tiempo_ejecucion': float(row['tiempo_ejecucion']) if row['tiempo_ejecucion'] else None
            }
            tareas.append(tarea)
        db.tareas.insert_many(tareas)
        print(f"[OK] {len(tareas)} tareas importadas")
    
    print("\n[SUCCESS] Importacion completada exitosamente!")
    print("\nDatos importados:")
    print(f"- Proyectos: {db.proyectos.count_documents({})}")
    print(f"- Responsables: {db.responsables.count_documents({})}")
    print(f"- Estados de tarea: {db.estados_tarea.count_documents({})}")
    print(f"- Tipos de documento: {db.tipo_documento.count_documents({})}")
    print(f"- Tareas: {db.tareas.count_documents({})}")
    
    client.close()

if __name__ == "__main__":
    import_csv_to_mongodb()
