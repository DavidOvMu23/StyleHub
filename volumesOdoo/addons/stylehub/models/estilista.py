from odoo import models, fields

# Modelo para los estilistas de peluquería

class StylehubEstilista(models.Model):
    # IDENTIFICADORES DEL MODELO
    _name = 'stylehub.estilista'
    _description = 'Estilistas de Stylehub'

    # CAMPOS
    name = fields.Char(string='Nombre del Estilista', required=True)
    active = fields.Boolean(string='Activo', default=True)