use("supermarket");

db.ventas.aggregate([

    {
      $unwind: "$items"
    },
    {
      $lookup: {
        from: "productos",
        localField: "items.producto_id",
        foreignField: "_id",
        as: "producto"
      }
    },
    {
      $unwind: "$producto"
    },
    {
      $group: {
        _id: "$_id",  
        cliente_id: { $first: "$cliente_id" },
        fecha: { $first: "$fecha" },
        total: { $first: "$total" },
        productos: {
          $push: {
            nombre: "$producto.nombre",
            precio: "$producto.precio",
            cantidad: "$items.cantidad"
          }
        }
      }
    },
    {
      $project: {
        
        cliente_id: 1,
        fecha: 1,
        total: 1,
        productos: 1,
        
      }
    },
    
  ]);

  