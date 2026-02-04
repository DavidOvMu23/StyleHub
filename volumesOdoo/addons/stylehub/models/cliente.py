from odoo import models, fields, api


class ResPartner(models.Model):
    #Extiende el modelo de contactos para incluir información de peluquería.

    #Se añade el historial de citas y un indicador VIP calculado, lo que permite
    #reconocer clientes recurrentes sin duplicar datos del contacto base.

    # _inherit dice: "No crees nada nuevo, busca el modelo 'res.partner' y añádele esto"
    _inherit = 'res.partner'

    # 1. Creamos un enlace inverso para ver las citas desde el cliente
    # (Esto no crea columna en base de datos, es una vista virtual)
    # Relación: un cliente puede tener muchas citas.
    cita_ids = fields.One2many('stylehub.cita', 'cliente_id', string='Historial de Citas')

    # 2. El campo VIP se calcula solo
    es_vip = fields.Boolean(string='Es VIP', compute='_compute_es_vip', store=True)

    # @api.depends indica qué campos disparan el recálculo automático.
    @api.depends('cita_ids', 'cita_ids.state')
    def _compute_es_vip(self):
        #Marca como VIP a clientes con más de 5 citas realizadas.

        for cliente in self:
            # Contamos cuántas citas tiene este cliente en estado 'realizada'
            citas_hechas = len(cliente.cita_ids.filtered(lambda c: c.state == 'realizada'))

            # Si tiene más de 5, es VIP
            if citas_hechas > 5:
                cliente.es_vip = True
            else:
                cliente.es_vip = False