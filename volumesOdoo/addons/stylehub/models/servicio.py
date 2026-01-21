from odoo import models, fields

# Modelo para los servicios de peluquería

class StylehubServicio(models.Model):
    _name = 'stylehub.servicio'
    _description = 'Servicios de Peluquería'

    name = fields.Char(string='Nombre del Servicio', required=True)
    precio = fields.Float(string='Precio Base', required=True)
    duracion = fields.Float(string='Duración (Horas)', help="Ejemplo: 0.5 son 30 minutos")