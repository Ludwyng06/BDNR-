# API de Reportes de Tareas - Flask + MongoDB

Este proyecto implementa una API REST con Flask y MongoDB para generar reportes complejos de tareas usando pipelines de agregación.

## 🚀 Características

- **Pipeline de agregación complejo** que combina datos de múltiples colecciones
- **Clasificación automática por grupos etáreos**:
  - Adulto joven: 18-30 años
  - Adulto medio: 31-50 años  
  - Adulto mayor: 51+ años
- **Ordenamiento alfabético** por nombre del responsable
- **Filtros por estado** de tarea (Pendiente, Terminada, Vencida)
- **Endpoints REST** para consumo con Postman, Insomnia, Thunder, etc.

## 📊 Estructura de Datos

El reporte incluye:
- Nombre de la tarea
- Estado de la tarea
- Nombre del proyecto asociado
- Nombre y apellido del responsable
- Edad del responsable
- Grupo etáreo calculado automáticamente

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install flask flask-pymongo pymongo requests
```

### 2. Importar datos a MongoDB
```bash
python import_data.py
```

### 3. Ejecutar la aplicación
```bash
python app.py
```

### 4. Probar la API
```bash
python test_api.py
```

## 🔗 Endpoints Disponibles

### Reportes
- `GET /reportes/tareas` - Reporte completo de todas las tareas
- `GET /reportes/tareas/filtro?estado=Pendiente` - Reporte filtrado por estado

### Colecciones
- `GET /proyectos` - Lista todos los proyectos
- `GET /responsables` - Lista todos los responsables
- `GET /estados-tarea` - Lista todos los estados de tarea

### Información
- `GET /api` - Información de la API y endpoints disponibles

## 📝 Ejemplo de Respuesta

```json
{
  "success": true,
  "total_registros": 30,
  "data": [
    {
      "nombre_tarea": "Tarea 19",
      "estado_tarea": "Vencida",
      "nombre_proyecto": "Estudio de suelos en Mocoa en pro de construcción de edificios de más de 20 pisos",
      "nombre_responsable": "Belinda",
      "apellido_responsable": "Aragón",
      "edad": 23,
      "grupo_etareo": "adulto joven"
    }
  ]
}
```

## 🧪 Pruebas con Herramientas Externas

### Postman
1. Crear nueva colección
2. Agregar request GET a `http://localhost:5000/reportes/tareas`
3. Enviar request

### Insomnia
1. Crear nuevo request
2. Método: GET
3. URL: `http://localhost:5000/reportes/tareas`
4. Enviar

### Thunder (VS Code)
1. Instalar extensión Thunder Client
2. Crear nuevo request
3. GET `http://localhost:5000/reportes/tareas`

## 🔍 Filtros Disponibles

- `?estado=Pendiente` - Solo tareas pendientes
- `?estado=Terminada` - Solo tareas terminadas  
- `?estado=Vencida` - Solo tareas vencidas
- `?estado=all` - Todas las tareas (por defecto)

## 📁 Estructura del Proyecto

```
proyecto/
├── app.py                 # Aplicación principal Flask
├── models.py             # Modelos de dominio y pipeline
├── controllers.py        # Controladores y endpoints
├── import_data.py        # Script para importar datos CSV
├── test_api.py          # Script de pruebas
├── collections/         # Archivos CSV con datos
│   ├── proyecto.csv
│   ├── tarea.csv
│   ├── responsable.csv
│   ├── estado_tarea.csv
│   └── tipo_documento.csv
└── README.md
```

## 🎯 Pipeline de Agregación

El pipeline implementa:
1. **$lookup** para unir tareas con proyectos, responsables y estados
2. **$unwind** para aplanar los arrays resultantes
3. **$addFields** con **$switch** para calcular grupos etáreos
4. **$project** para seleccionar campos específicos
5. **$sort** para ordenar alfabéticamente

## 🚨 Requisitos

- Python 3.7+
- MongoDB 4.0+
- Flask
- PyMongo
