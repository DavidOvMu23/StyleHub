from odoo import models, fields


class PeluqueriaServicio(models.Model):
    #Catálogo de servicios disponibles en la peluquería.

    #Este modelo actúa como base para definir los servicios que luego se
    #seleccionan en las citas. Centralizar aquí precio y duración permite
    #mantener consistencia y reutilizar la información en múltiples citas.

    # IDENTIFICADORES DEL MODELO
    # _name es el nombre técnico del modelo. Es para referenciarlo y poder usarlo en el codigo.
    _name = 'stylehub.servicio'
    # _description es el nombre legible del modelo
    _description = 'Servicios de Peluquería'

    # CAMPOS
    # campo de texto para guardar el nombre
    name = fields.Char(string='Nombre del Servicio', required=True)

    # float para el precio del sevicio
    precio = fields.Float(string='Precio Base', required=True)

    # float para la diración del servicio en horas
    duracion = fields.Float(string='Duración (Horas)', help="Ejemplo: 0.5 son 30 minutos")