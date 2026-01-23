{
    'name': 'StyleHub',

    'depends': ['base'],  # Dependemos del módulo base porque usaremos Clientes (res.partner)
    'data': [
        'security/ir.model.access.csv', # Permisos de acceso a los modelos
        'views/servicio_views.xml',     # Vistas para el modelo Servicio
    ],
    'installable': True,
    'application': True,
}