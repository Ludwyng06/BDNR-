#!/usr/bin/env python3
"""
Script para mostrar el pipeline de agregación completo
"""
import json
from pymongo import MongoClient

def show_pipeline():
    """
    Muestra el pipeline de agregación completo con explicaciones
    """
    print("=" * 80)
    print("[PIPELINE] PIPELINE DE AGREGACION PARA REPORTE DE TAREAS")
    print("=" * 80)
    
   
    pipeline = [

        # {
        #     "$match": {
        #         "id_estado_tarea": {
        #             "$in": [ObjectId("estado_pendiente_id"), ObjectId("estado_terminada_id")]
        #         }
        #     }
        # },

        {
            "$lookup": {
                "from": "proyectos",
                "localField": "id_proyecto", 
                "foreignField": "_id",
                "as": "proyecto"
            }
        },
        {
            "$lookup": {
                "from": "responsables",
                "localField": "id_responsable",
                "foreignField": "_id", 
                "as": "responsable"
            }
        },
        {
            "$lookup": {
                "from": "estados_tarea",
                "localField": "id_estado_tarea",
                "foreignField": "_id",
                "as": "estado"
            }
        },
        {
            "$unwind": "$proyecto"
        },
        {
            "$unwind": "$responsable"
        },
        {
            "$unwind": "$estado"
        },
        {
            "$addFields": {
                "grupo_etareo": {
                    "$cond": {
                        "if": {
                            "$and": [
                                {"$gt": ["$responsable.edad", 17]},
                                {"$lte": ["$responsable.edad", 30]}
                            ]
                        },
                        "then": "adulto joven",
                        "else": {
                            "$cond": {
                                "if": {
                                    "$and": [
                                        {"$gt": ["$responsable.edad", 30]},
                                        {"$lte": ["$responsable.edad", 50]}
                                    ]
                                },
                                "then": "adulto medio",
                                "else": {
                                    "$cond": {
                                        "if": {"$gt": ["$responsable.edad", 50]},
                                        "then": "adulto mayor",
                                        "else": "sin clasificar"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "nombre_tarea": "$nombre_tarea",
                "estado_tarea": "$estado.estado_tarea",
                "nombre_proyecto": "$proyecto.nombre_proyecto",
                "nombre_responsable": "$responsable.nombre_responsable",
                "apellido_responsable": "$responsable.apellido_responsable",
                "edad": "$responsable.edad",
                "grupo_etareo": "$grupo_etareo"
            }
        },
        {
            "$sort": {"nombre_responsable": 1}
        }
    ]
    
    print("\n[STEPS] PASOS DEL PIPELINE:")
    print("-" * 50)
    
    steps = [
        ("0. $match (OPCIONAL)", "Filtra tareas por estado - COMENTADO para mostrar todas"),
        ("1. $lookup (proyectos)", "Une tareas con proyectos usando id_proyecto"),
        ("2. $lookup (responsables)", "Une tareas con responsables usando id_responsable"),
        ("3. $lookup (estados)", "Une tareas con estados usando id_estado_tarea"),
        ("4. $unwind (proyecto)", "Aplana el array de proyecto (1 documento por tarea)"),
        ("5. $unwind (responsable)", "Aplana el array de responsable (1 documento por tarea)"),
        ("6. $unwind (estado)", "Aplana el array de estado (1 documento por tarea)"),
        ("7. $addFields (grupo_etareo)", "Calcula grupo etáreo usando $cond con if/else anidados"),
        ("8. $project", "Selecciona solo los campos requeridos en el reporte"),
        ("9. $sort", "Ordena alfabéticamente por nombre del responsable")
    ]
    
    for step, description in steps:
        print(f"  {step:<25} - {description}")
    
    print("\n[FILTER] FILTRO POR ESTADO:")
    print("-" * 50)
    print("  • COMENTADO: Muestra TODAS las tareas (pendientes, terminadas, vencidas)")
    print("  • DESCOMENTADO: Muestra solo tareas PENDIENTES y TERMINADAS")
    print("  • Para activar: Descomenta la sección $match en el pipeline")
    print("  • Para desactivar: Comenta la sección $match en el pipeline")
    
    print("\n[CONDITIONS] CONDICIONES DEL GRUPO ETAREO:")
    print("-" * 50)
    print("  • 18-30 años: 'adulto joven'")
    print("  • 31-50 años: 'adulto medio'") 
    print("  • 51+ años: 'adulto mayor'")
    print("  • Otros: 'sin clasificar'")
    
    print("\n[FIELDS] CAMPOS DEL REPORTE FINAL:")
    print("-" * 50)
    fields = [
        "nombre_tarea",
        "estado_tarea", 
        "nombre_proyecto",
        "nombre_responsable",
        "apellido_responsable",
        "edad",
        "grupo_etareo"
    ]
    
    for field in fields:
        print(f"  • {field}")
    
    print("\n[JSON] PIPELINE COMPLETO (JSON):")
    print("-" * 50)
    print(json.dumps(pipeline, indent=2, ensure_ascii=False))
    
    print("\n[USAGE] COMO USAR:")
    print("-" * 50)
    print("  • API: GET http://localhost:5000/reportes/tareas")
    print("  • Pipeline: GET http://localhost:5000/pipeline")
    print("  • MongoDB: db.tareas.aggregate([...pipeline...])")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    show_pipeline()
