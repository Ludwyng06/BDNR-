"""
Modelos para la base de datos Supermarket
"""
from bson import ObjectId

class CategoriaModel:
    """Modelo para categorías de productos"""
    collection = None

    @staticmethod
    def init(mongo):
        CategoriaModel.collection = mongo.db.categorias

    @staticmethod
    def get_all_categorias():
        return list(CategoriaModel.collection.find())

    @staticmethod
    def get_categoria(categoria_id):
        return CategoriaModel.collection.find_one({"_id": categoria_id})


class ProveedorModel:
    """Modelo para proveedores"""
    collection = None

    @staticmethod
    def init(mongo):
        ProveedorModel.collection = mongo.db.proveedores

    @staticmethod
    def get_all_proveedores():
        return list(ProveedorModel.collection.find())

    @staticmethod
    def get_proveedor(proveedor_id):
        return ProveedorModel.collection.find_one({"_id": proveedor_id})


class ClienteModel:
    """Modelo para clientes"""
    collection = None

    @staticmethod
    def init(mongo):
        ClienteModel.collection = mongo.db.clientes

    @staticmethod
    def get_all_clientes():
        return list(ClienteModel.collection.find())

    @staticmethod
    def get_cliente(cliente_id):
        return ClienteModel.collection.find_one({"_id": cliente_id})


class ProductoModel:
    """Modelo para productos"""
    collection = None

    @staticmethod
    def init(mongo):
        ProductoModel.collection = mongo.db.productos

    @staticmethod
    def get_all_productos():
        return list(ProductoModel.collection.find())

    @staticmethod
    def get_producto(producto_id):
        return ProductoModel.collection.find_one({"_id": producto_id})

    @staticmethod
    def get_productos_por_categoria(categoria_id):
        return list(ProductoModel.collection.find({"categoria_id": categoria_id}))


class VentaModel:
    """Modelo para ventas"""
    collection = None

    @staticmethod
    def init(mongo):
        VentaModel.collection = mongo.db.ventas

    @staticmethod
    def get_all_ventas():
        return list(VentaModel.collection.find())

    @staticmethod
    def get_venta(venta_id):
        return VentaModel.collection.find_one({"_id": venta_id})

    @staticmethod
    def get_ventas_por_cliente(cliente_id):
        return list(VentaModel.collection.find({"cliente_id": cliente_id}))


class SupermarketReporteModel:
    """
    Modelo para generar reportes complejos de Supermarket usando pipelines de agregación.
    """
    collection = None

    @staticmethod
    def init(mongo):
        SupermarketReporteModel.collection = mongo.db

    @staticmethod
    def generar_reporte_ventas_detallado():
        """
        Pipeline de agregación para generar reporte detallado de ventas con información de clientes y productos.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "clientes",
                    "localField": "cliente_id",
                    "foreignField": "_id",
                    "as": "cliente"
                }
            },
            {
                "$unwind": "$cliente"
            },
            {
                "$unwind": "$items"
            },
            {
                "$lookup": {
                    "from": "productos",
                    "localField": "items.producto_id",
                    "foreignField": "_id",
                    "as": "producto"
                }
            },
            {
                "$unwind": "$producto"
            },
            {
                "$lookup": {
                    "from": "categorias",
                    "localField": "producto.categoria_id",
                    "foreignField": "_id",
                    "as": "categoria"
                }
            },
            {
                "$unwind": "$categoria"
            },
            {
                "$project": {
                    "_id": 0,
                    "venta_id": "$_id",
                    "fecha": "$fecha",
                    "cliente_nombre": "$cliente.nombre",
                    "cliente_email": "$cliente.email",
                    "producto_nombre": "$producto.nombre",
                    "categoria_nombre": "$categoria.nombre",
                    "cantidad": "$items.cantidad",
                    "precio_unitario": "$producto.precio",
                    "subtotal": {"$multiply": ["$items.cantidad", "$producto.precio"]},
                    "total_venta": "$total"
                }
            },
            {
                "$sort": {"fecha": -1, "cliente_nombre": 1}
            }
        ]
        
        return list(SupermarketReporteModel.collection.ventas.aggregate(pipeline))

    @staticmethod
    def generar_reporte_ventas_por_categoria():
        """
        Pipeline para generar reporte de ventas agrupadas por categoría.
        """
        pipeline = [
            {
                "$unwind": "$items"
            },
            {
                "$lookup": {
                    "from": "productos",
                    "localField": "items.producto_id",
                    "foreignField": "_id",
                    "as": "producto"
                }
            },
            {
                "$unwind": "$producto"
            },
            {
                "$lookup": {
                    "from": "categorias",
                    "localField": "producto.categoria_id",
                    "foreignField": "_id",
                    "as": "categoria"
                }
            },
            {
                "$unwind": "$categoria"
            },
            {
                "$group": {
                    "_id": "$categoria.nombre",
                    "total_ventas": {"$sum": 1},
                    "total_cantidad": {"$sum": "$items.cantidad"},
                    "total_ingresos": {"$sum": {"$multiply": ["$items.cantidad", "$producto.precio"]}}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "categoria": "$_id",
                    "total_ventas": 1,
                    "total_cantidad": 1,
                    "total_ingresos": 1
                }
            },
            {
                "$sort": {"total_ingresos": -1}
            }
        ]
        
        return list(SupermarketReporteModel.collection.ventas.aggregate(pipeline))
