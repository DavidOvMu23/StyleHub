from odoo import models, fields

# Modelo para los estilistas de peluquería


class StylehubEstilista(models.Model):
    #Registro de profesionales que atienden las citas.

    #Se usa un campo `active` para poder archivar estilistas sin perder el
    #historial de citas asociadas, una práctica habitual en Odoo.
    
    # IDENTIFICADORES DEL MODELO
    _name = 'stylehub.estilista'
    _description = 'Estilistas de Stylehub'

    # CAMPOS
    name = fields.Char(string='Nombre del Estilista', required=True)
    active = fields.Boolean(string='Activo', default=True)