#!/usr/bin/env python3
"""
Script para importar datos de Supermarket a MongoDB
"""
import csv
import json
from pymongo import MongoClient
from bson import ObjectId

def import_supermarket_data():
    """
    Importa todos los datos de Supermarket a MongoDB
    """
    # Conectar a MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["supermarket"]
    
    print("Iniciando importacion de datos de Supermarket...")
    
    # 1. Importar Categorías
    print("Importando categorias...")
    categorias_collection = db["categorias"]
    categorias_collection.drop()  # Limpiar colección existente
    
    with open("BD Supermarket/categorias.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            categoria = {
                "_id": int(row["_id"]),
                "nombre": row["nombre"],
                "descripcion": row["descripcion"]
            }
            categorias_collection.insert_one(categoria)
    
    print(f"Categorias importadas: {categorias_collection.count_documents({})}")
    
    # 2. Importar Proveedores
    print("Importando proveedores...")
    proveedores_collection = db["proveedores"]
    proveedores_collection.drop()
    
    with open("BD Supermarket/proveedores.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            proveedor = {
                "_id": int(row["_id"]),
                "nombre": row["nombre"],
                "telefono": row["telefono"],
                "direccion": row["direccion"]
            }
            proveedores_collection.insert_one(proveedor)
    
    print(f"Proveedores importados: {proveedores_collection.count_documents({})}")
    
    # 3. Importar Clientes
    print("Importando clientes...")
    clientes_collection = db["clientes"]
    clientes_collection.drop()
    
    with open("BD Supermarket/clientes.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cliente = {
                "_id": int(row["_id"]),
                "nombre": row["nombre"],
                "email": row["email"],
                "telefono": row["telefono"]
            }
            clientes_collection.insert_one(cliente)
    
    print(f"Clientes importados: {clientes_collection.count_documents({})}")
    
    # 4. Importar Productos
    print("Importando productos...")
    productos_collection = db["productos"]
    productos_collection.drop()
    
    with open("BD Supermarket/productos.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            producto = {
                "_id": int(row["_id"]),
                "nombre": row["nombre"],
                "categoria_id": int(row["categoria_id"]),
                "precio": float(row["precio"]),
                "stock": int(row["stock"]),
                "proveedor_id": int(row["proveedor_id"])
            }
            productos_collection.insert_one(producto)
    
    print(f"Productos importados: {productos_collection.count_documents({})}")
    
    # 5. Importar Ventas
    print("Importando ventas...")
    ventas_collection = db["ventas"]
    ventas_collection.drop()
    
    with open("BD Supermarket/ventas.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parsear items JSON
            items = json.loads(row["items"])
            
            venta = {
                "_id": int(row["_id"]),
                "cliente_id": int(row["cliente_id"]),
                "fecha": row["fecha"],
                "items": items,
                "total": float(row["total"])
            }
            ventas_collection.insert_one(venta)
    
    print(f"Ventas importadas: {ventas_collection.count_documents({})}")
    
    print("\nImportacion completada exitosamente!")
    print("Resumen:")
    print(f"   • Categorías: {categorias_collection.count_documents({})}")
    print(f"   • Proveedores: {proveedores_collection.count_documents({})}")
    print(f"   • Clientes: {clientes_collection.count_documents({})}")
    print(f"   • Productos: {productos_collection.count_documents({})}")
    print(f"   • Ventas: {ventas_collection.count_documents({})}")
    
    client.close()

if __name__ == "__main__":
    import_supermarket_data()
