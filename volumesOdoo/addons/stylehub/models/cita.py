from odoo import models, fields, api

class StylehubCita(models.Model):
    _name = 'stylehub.cita'
    _description = 'Cita de Peluquería'

    # RELACIONES (Many2one)
    # Vinculamos con el modelo de Contactos de Odoo (res.partner)
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    
    # Vinculamos con el modelo de Estilistas
    estilista_id = fields.Many2one('stylehub.estilista', string='Estilista', required=True)

    # CAMPOS BÁSICOS
    fecha_inicio = fields.Datetime(string='Fecha y Hora Inicio', required=True)
    
    # ESTADO (En el enunciado pide el estado de las citas: Borrador, Confirmada...)
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='borrador')
    
    # Si usamos Many2many a servicios, no deja editar el precio solo para esta cita
    # sin cambiar el precio del catálogo general.
    # Por eso he acabado haciendo un One2many a una tabla intermedia. Por que en el 
    # enunciado se pide que si el cliente tiene mucho pelo se deberá de cobrar un poco y si no se
    # hace así, lo que va a hacer es cambiar el precio del servicio en el catálogo general.
    
    lineas_ids = fields.One2many('stylehub.cita.linea', 'cita_id', string='Servicios')

# Tabla intermedia para los servicios en una cita
class StylehubCitaLinea(models.Model):
    _name = 'stylehub.cita.linea'
    _description = 'Línea de Servicio en Cita'

    cita_id = fields.Many2one('stylehub.cita', string='Cita')
    servicio_id = fields.Many2one('stylehub.servicio', string='Servicio', required=True)
    
    # Estos campos se copiarán del servicio, pero permitimos editarlos
    precio = fields.Float(string='Precio')
    duracion = fields.Float(string='Duración (Horas)')

    # Al cambiar el servicio, copiamos precio y duración
    @api.onchange('servicio_id') # el api on change es para cuando el usuario cambia el campo en la vista
    def _onchange_servicio_id(self):
        # Si el usuario elige un servicio...
        if self.servicio_id:
            # ...copiamos el precio y duración de ese servicio a esta línea
            self.precio = self.servicio_id.precio
            self.duracion = self.servicio_id.duracion