from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from controllers import user_bp, reporte_bp
from models import UserModel, ProyectoModel, TareaModel, ResponsableModel, EstadoTareaModel, ReporteModel
from supermarket_controllers import supermarket_bp
from supermarket_models import CategoriaModel, ProveedorModel, ClienteModel, ProductoModel, VentaModel, SupermarketReporteModel

app = Flask(__name__)

# Configuración de la base de datos TAREAS
app.config["MONGO_URI"] = "mongodb://localhost:27017/mi_db"
mongo = PyMongo(app)

# Configuración de la base de datos SUPERMARKET
client = MongoClient("mongodb://localhost:27017/")
db_supermarket = client["supermarket"]

# Inicializar todos los modelos de TAREAS
UserModel.init(mongo)
ProyectoModel.init(mongo)
TareaModel.init(mongo)
ResponsableModel.init(mongo)
EstadoTareaModel.init(mongo)
ReporteModel.init(mongo)

# Inicializar todos los modelos de SUPERMARKET
# Crear una instancia de PyMongo para la base de datos supermarket
from flask_pymongo import PyMongo

app.config["SUPERMARKET_MONGO_URI"] = "mongodb://localhost:27017/supermarket"
mongo_supermarket = PyMongo(app, uri="mongodb://localhost:27017/supermarket")

CategoriaModel.init(mongo_supermarket)
ProveedorModel.init(mongo_supermarket)
ClienteModel.init(mongo_supermarket)
ProductoModel.init(mongo_supermarket)
VentaModel.init(mongo_supermarket)
SupermarketReporteModel.init(mongo_supermarket)

# Registrar los blueprints
app.register_blueprint(user_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(supermarket_bp)

@app.route("/")
def index():
    return "API Flask + MongoDB funcionando con todas las colecciones"

@app.route("/unified")
def unified_data():
    """
    Endpoint que une datos de ambas bases de datos como en el ejemplo
    """
    try:
        # Obtener datos de la base de datos TAREAS
        usuarios = list(mongo.db.users.find({}, {"_id": 0}))
        tareas = list(mongo.db.tareas.find({}, {"_id": 0}))
        proyectos = list(mongo.db.proyectos.find({}, {"_id": 0}))
        
        # Obtener datos de la base de datos SUPERMARKET
        clientes = list(mongo_supermarket.db.clientes.find({}, {"_id": 0}))
        productos = list(mongo_supermarket.db.productos.find({}, {"_id": 0}))
        ventas = list(mongo_supermarket.db.ventas.find({}, {"_id": 0}))
        
        return jsonify({
            "base_datos_tareas": {
                "usuarios": usuarios,
                "tareas": tareas,
                "proyectos": proyectos
            },
            "base_datos_supermarket": {
                "clientes": clientes,
                "productos": productos,
                "ventas": ventas
            },
            "resumen": {
                "total_usuarios": len(usuarios),
                "total_tareas": len(tareas),
                "total_proyectos": len(proyectos),
                "total_clientes": len(clientes),
                "total_productos": len(productos),
                "total_ventas": len(ventas)
            }
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error al obtener datos de las bases de datos"
        }), 500

@app.route("/api")
def api_info():
    return {
        "message": "API Unificada - Tareas + Supermarket",
        "endpoints": {
            "unified_data": "/unified",
            "tareas": {
                "reporte_tareas": "/reportes/tareas",
                "reporte_tareas_filtrado": "/reportes/tareas/filtro?estado=Pendiente|Terminada|Vencida|all",
                "reporte_pendientes_terminadas": "/reportes/tareas?filtrar=pendientes_terminadas",
                "pipeline_info": "/pipeline",
                "proyectos": "/proyectos",
                "responsables": "/responsables",
                "estados_tarea": "/estados-tarea"
            },
            "supermarket": {
                "categorias": "/supermarket/categorias",
                "proveedores": "/supermarket/proveedores",
                "clientes": "/supermarket/clientes",
                "productos": "/supermarket/productos",
                "productos_por_categoria": "/supermarket/productos/categoria/<id>",
                "ventas": "/supermarket/ventas",
                "reporte_ventas_detallado": "/supermarket/reportes/ventas-detallado",
                "reporte_ventas_por_categoria": "/supermarket/reportes/ventas-por-categoria"
            }
        },
        "filtros_disponibles": {
            "todas_las_tareas": "GET /reportes/tareas (sin parámetros)",
            "pendientes_terminadas": "GET /reportes/tareas?filtrar=pendientes_terminadas",
            "por_estado_especifico": "GET /reportes/tareas/filtro?estado=Pendiente|Terminada|Vencida"
        }
    }

if __name__ == "__main__":
    print("Iniciando servidor Flask en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)