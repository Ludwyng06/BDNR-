from flask import Blueprint, request, jsonify
from models import UserModel, ProyectoModel, TareaModel, ResponsableModel, EstadoTareaModel, ReporteModel

user_bp = Blueprint("users", __name__)
reporte_bp = Blueprint("reportes", __name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user_id = UserModel.create_user(data)
    return jsonify({"message": "Usuario creado", "id": str(user_id)}), 201

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = UserModel.get_all_users()
    for u in users:
        u["_id"] = str(u["_id"])
    return jsonify(users)

@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = UserModel.get_user(user_id)
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    result = UserModel.update_user(user_id, data)
    if result.modified_count > 0:
        return jsonify({"message": "Usuario actualizado"})
    return jsonify({"error": "No se actualizó ningún usuario"}), 404

@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = UserModel.delete_user(user_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Usuario eliminado"})
    return jsonify({"error": "No se eliminó ningún usuario"}), 404


# Endpoints para reportes
@reporte_bp.route("/reportes/tareas", methods=["GET"])
def get_reporte_tareas():
    """
    Endpoint para obtener el reporte de tareas con todas las especificaciones:
    - Nombre de la tarea
    - Estado de la tarea
    - Nombre del proyecto asociado
    - Nombre y apellido del responsable
    - Edad del responsable
    - Grupo etáreo (adulto joven, adulto medio, adulto mayor)
    - Ordenado alfabéticamente por nombre del responsable
    
    Parámetros opcionales:
    - filtrar: "pendientes_terminadas" para filtrar solo pendientes y terminadas
    """
    try:
        filtrar = request.args.get('filtrar', None)
        
        # Determinar qué estados filtrar
        if filtrar == "pendientes_terminadas":
            estados_filtro = ["Pendiente", "Terminada"]
        else:
            estados_filtro = None  # Mostrar todas las tareas
        
        reporte = ReporteModel.generar_reporte_tareas(estados_filtro)
        return jsonify({
            "success": True,
            "filtro_aplicado": "pendientes_terminadas" if estados_filtro else "todas_las_tareas",
            "total_registros": len(reporte),
            "data": reporte
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@reporte_bp.route("/reportes/tareas/filtro", methods=["GET"])
def get_reporte_tareas_filtrado():
    """
    Endpoint para obtener el reporte de tareas con filtro por estado.
    Parámetros de query:
    - estado: "Pendiente", "Terminada", "Vencida" o "all" para todos
    """
    try:
        estado_filtro = request.args.get('estado', 'all')
        
        # Obtener todos los datos del reporte
        reporte_completo = ReporteModel.generar_reporte_tareas()
        
        # Aplicar filtro si se especifica
        if estado_filtro != 'all':
            reporte_filtrado = [tarea for tarea in reporte_completo if tarea['estado_tarea'] == estado_filtro]
        else:
            reporte_filtrado = reporte_completo
        
        return jsonify({
            "success": True,
            "filtro_aplicado": estado_filtro,
            "total_registros": len(reporte_filtrado),
            "data": reporte_filtrado
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Endpoints adicionales para las otras colecciones
@reporte_bp.route("/proyectos", methods=["GET"])
def get_proyectos():
    try:
        proyectos = ProyectoModel.get_all_proyectos()
        for p in proyectos:
            p["_id"] = str(p["_id"])
        return jsonify(proyectos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reporte_bp.route("/responsables", methods=["GET"])
def get_responsables():
    try:
        responsables = ResponsableModel.get_all_responsables()
        for r in responsables:
            r["_id"] = str(r["_id"])
        return jsonify(responsables), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reporte_bp.route("/estados-tarea", methods=["GET"])
def get_estados_tarea():
    try:
        estados = EstadoTareaModel.get_all_estados()
        for e in estados:
            e["_id"] = str(e["_id"])
        return jsonify(estados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reporte_bp.route("/pipeline", methods=["GET"])
def get_pipeline_info():
    """
    Endpoint para mostrar el pipeline de agregación completo
    """
    pipeline = [
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
    
    return jsonify({
        "message": "Pipeline de agregación para el reporte de tareas",
        "description": "Este pipeline combina datos de múltiples colecciones y calcula grupos etáreos",
        "steps": [
            "0. $match (OPCIONAL): Filtra por estado - solo si se especifica filtrar_estados",
            "1. $lookup: Une tareas con proyectos",
            "2. $lookup: Une tareas con responsables", 
            "3. $lookup: Une tareas con estados",
            "4. $unwind: Aplana los arrays de join",
            "5. $addFields: Calcula grupo etáreo con $cond (if/else)",
            "6. $project: Selecciona campos específicos",
            "7. $sort: Ordena alfabéticamente por responsable"
        ],
        "pipeline": pipeline,
        "usage": "GET /reportes/tareas para ejecutar este pipeline"
    }), 200