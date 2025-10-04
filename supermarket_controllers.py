"""
Controladores para la base de datos Supermarket
"""
from flask import Blueprint, jsonify, request
from supermarket_models import (
    CategoriaModel, ProveedorModel, ClienteModel, 
    ProductoModel, VentaModel, SupermarketReporteModel
)

# Blueprint para Supermarket
supermarket_bp = Blueprint("supermarket", __name__)

# Endpoints para Categorías
@supermarket_bp.route("/supermarket/categorias", methods=["GET"])
def get_categorias():
    try:
        categorias = CategoriaModel.get_all_categorias()
        for c in categorias:
            c["_id"] = str(c["_id"])
        return jsonify({
            "success": True,
            "total": len(categorias),
            "data": categorias
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints para Proveedores
@supermarket_bp.route("/supermarket/proveedores", methods=["GET"])
def get_proveedores():
    try:
        proveedores = ProveedorModel.get_all_proveedores()
        for p in proveedores:
            p["_id"] = str(p["_id"])
        return jsonify({
            "success": True,
            "total": len(proveedores),
            "data": proveedores
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints para Clientes
@supermarket_bp.route("/supermarket/clientes", methods=["GET"])
def get_clientes():
    try:
        clientes = ClienteModel.get_all_clientes()
        for c in clientes:
            c["_id"] = str(c["_id"])
        return jsonify({
            "success": True,
            "total": len(clientes),
            "data": clientes
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints para Productos
@supermarket_bp.route("/supermarket/productos", methods=["GET"])
def get_productos():
    try:
        productos = ProductoModel.get_all_productos()
        for p in productos:
            p["_id"] = str(p["_id"])
        return jsonify({
            "success": True,
            "total": len(productos),
            "data": productos
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@supermarket_bp.route("/supermarket/productos/categoria/<int:categoria_id>", methods=["GET"])
def get_productos_por_categoria(categoria_id):
    try:
        productos = ProductoModel.get_productos_por_categoria(categoria_id)
        for p in productos:
            p["_id"] = str(p["_id"])
        return jsonify({
            "success": True,
            "categoria_id": categoria_id,
            "total": len(productos),
            "data": productos
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints para Ventas
@supermarket_bp.route("/supermarket/ventas", methods=["GET"])
def get_ventas():
    try:
        ventas = VentaModel.get_all_ventas()
        for v in ventas:
            v["_id"] = str(v["_id"])
        return jsonify({
            "success": True,
            "total": len(ventas),
            "data": ventas
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Endpoints para Reportes
@supermarket_bp.route("/supermarket/reportes/ventas-detallado", methods=["GET"])
def get_reporte_ventas_detallado():
    """
    Reporte detallado de ventas con información de clientes y productos
    """
    try:
        reporte = SupermarketReporteModel.generar_reporte_ventas_detallado()
        return jsonify({
            "success": True,
            "total_registros": len(reporte),
            "data": reporte
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@supermarket_bp.route("/supermarket/reportes/ventas-por-categoria", methods=["GET"])
def get_reporte_ventas_por_categoria():
    """
    Reporte de ventas agrupadas por categoría
    """
    try:
        reporte = SupermarketReporteModel.generar_reporte_ventas_por_categoria()
        return jsonify({
            "success": True,
            "total_categorias": len(reporte),
            "data": reporte
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@supermarket_bp.route("/supermarket/reportes/ventas-con-productos", methods=["GET"])
def get_ventas_con_productos():
    """
    Reporte de ventas con productos unidos (equivalente a joinColecciones.js)
    """
    try:
        reporte = SupermarketReporteModel.generar_ventas_con_productos_unidos()
        return jsonify({
            "success": True,
            "total_ventas": len(reporte),
            "data": reporte
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500