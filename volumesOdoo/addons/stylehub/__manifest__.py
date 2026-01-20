# -*- coding: utf-8 -*-
{
    'name': "StyleHub",

    # 'base' es necesario porque vamos a usar los Clientes de Odoo (res.partner)
    'depends': ['base'],

    # Aquí iremos añadiendo los archivos XML y CSV conforme los creemos
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
    ],
    
    'application': True, # Esto hace que aparezca en el menú de Aplicaciones principal
    'installable': True,
}