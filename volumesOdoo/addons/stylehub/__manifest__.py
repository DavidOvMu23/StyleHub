{
    'name': 'StyleHub',

    'depends': ['base', 'contacts'],  # Dependemos del módulo base y de Contacts para clientes
    'data': [
        'security/ir.model.access.csv', # Permisos de acceso a los modelos
        'views/servicio_views.xml',
        'views/estilista_views.xml',
        'views/cita_views.xml',
    ],
    'installable': True,
    'application': True,
}