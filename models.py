from bson.objectid import ObjectId

class UserModel:
    """
    Modelo de dominio para la colección 'usuarios' en MongoDB.
    Implementa operaciones CRUD usando métodos estáticos.
    """
    collection = None  # atributo de clase que guardará la referencia a la colección

    @staticmethod
    def init(mongo):
        UserModel.collection = mongo.db.usuarios

    @staticmethod
    def create_user(data):
        return UserModel.collection.insert_one(data).inserted_id

    @staticmethod
    def get_all_users():
        return list(UserModel.collection.find())

    @staticmethod
    def get_user(user_id):
        return UserModel.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update_user(user_id, data):
        return UserModel.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )

    @staticmethod
    def delete_user(user_id):
        return UserModel.collection.delete_one({"_id": ObjectId(user_id)})


class ProyectoModel:
    """
    Modelo de dominio para la colección 'proyectos' en MongoDB.
    """
    collection = None

    @staticmethod
    def init(mongo):
        ProyectoModel.collection = mongo.db.proyectos

    @staticmethod
    def get_all_proyectos():
        return list(ProyectoModel.collection.find())

    @staticmethod
    def get_proyecto(proyecto_id):
        return ProyectoModel.collection.find_one({"_id": ObjectId(proyecto_id)})


class TareaModel:
    """
    Modelo de dominio para la colección 'tareas' en MongoDB.
    """
    collection = None

    @staticmethod
    def init(mongo):
        TareaModel.collection = mongo.db.tareas

    @staticmethod
    def get_all_tareas():
        return list(TareaModel.collection.find())

    @staticmethod
    def get_tarea(tarea_id):
        return TareaModel.collection.find_one({"_id": ObjectId(tarea_id)})


class ResponsableModel:
    """
    Modelo de dominio para la colección 'responsables' en MongoDB.
    """
    collection = None

    @staticmethod
    def init(mongo):
        ResponsableModel.collection = mongo.db.responsables

    @staticmethod
    def get_all_responsables():
        return list(ResponsableModel.collection.find())

    @staticmethod
    def get_responsable(responsable_id):
        return ResponsableModel.collection.find_one({"_id": ObjectId(responsable_id)})


class EstadoTareaModel:
    """
    Modelo de dominio para la colección 'estados_tarea' en MongoDB.
    """
    collection = None

    @staticmethod
    def init(mongo):
        EstadoTareaModel.collection = mongo.db.estados_tarea

    @staticmethod
    def get_all_estados():
        return list(EstadoTareaModel.collection.find())

    @staticmethod
    def get_estado(estado_id):
        return EstadoTareaModel.collection.find_one({"_id": ObjectId(estado_id)})


class ReporteModel:
    """
    Modelo para generar reportes complejos usando pipelines de agregación.
    """
    collection = None

    @staticmethod
    def init(mongo):
        ReporteModel.collection = mongo.db

    @staticmethod
    def generar_reporte_tareas(filtrar_estados=None):
        """
        Pipeline de agregación para generar el reporte de tareas con todas las especificaciones.
        
        Args:
            filtrar_estados (list): Lista de estados a filtrar. Si es None, muestra todas las tareas.
        """
        pipeline = []
        
        # Agregar filtro por estado si se especifica
        if filtrar_estados:
            # Primero necesitamos obtener los ObjectIds de los estados
            estados_collection = ReporteModel.collection.estados_tarea
            estados_ids = []
            for estado_nombre in filtrar_estados:
                estado_doc = estados_collection.find_one({"estado_tarea": estado_nombre})
                if estado_doc:
                    estados_ids.append(estado_doc["_id"])
            
            if estados_ids:
                pipeline.append({
                    "$match": {
                        "id_estado_tarea": {"$in": estados_ids}
                    }
                })
        
        pipeline.extend([
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
        ])
        
        return list(ReporteModel.collection.tareas.aggregate(pipeline))