from odoo import models, fields, api
from datetime import timedelta  # Herramienta de Python para sumar/restar horas a una fecha
from odoo.exceptions import ValidationError  # Para lanzar errores de validación


class StylehubCita(models.Model):
    #Gestiona las citas de peluquería y sus servicios asociados.

    _name = 'stylehub.cita'
    _description = 'Cita de Peluquería'
    _rec_name = 'cliente_id'

    # RELACIONES (Many2one)
    # Vinculamos con el modelo de Contactos de Odoo (res.partner)
    # Relación: una cita pertenece a un único cliente.
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)

    # Vinculamos con el modelo de Estilistas
    # Relación: una cita es atendida por un único estilista.
    estilista_id = fields.Many2one('stylehub.estilista', string='Estilista', required=True)

    # CAMPOS BÁSICOS
    fecha_inicio = fields.Datetime(string='Fecha y Hora Inicio', required=True)
    
    # CAMPOS CALCULADOS
    fecha_fin = fields.Datetime(
        string='Fecha Fin', 
        compute='_compute_totales', 
        store=True  # Significa que lo calcule y que lo guarde en la base de datos
    )

    importe_total = fields.Float(
        string='Total a Pagar', 
        compute='_compute_totales', 
        store=True
    )

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

    # Relación: una cita tiene varias líneas de servicio, cada línea apunta a la cita.
    lineas_ids = fields.One2many('stylehub.cita.linea', 'cita_id', string='Servicios')

    # CALCULOS DE LOS CAMPOS
    # @api.depends le dice a Odoo: "Vigila estos campos. Si cambian, recalcula la función".
    @api.depends('fecha_inicio', 'lineas_ids', 'lineas_ids.duracion', 'lineas_ids.precio')
    def _compute_totales(self):

        #Calcula fecha_fin y importe_total en función de los servicios.

        #Lógica:
        #1) Si no hay fecha_inicio, no se puede calcular el fin ni el importe.
        #2) Sumar la duración de cada línea de servicio para obtener horas totales.
        #3) Sumar el precio de cada línea para obtener el importe total.
        #4) Calcular fecha_fin sumando las horas totales a fecha_inicio.

        for cita in self:
            # Si no hay fecha de inicio, no podemos calcular el fin
            if not cita.fecha_inicio:
                cita.fecha_fin = False
                cita.importe_total = 0.0
                continue

            # Sumamos la duración de todas las líneas
            horas_totales = sum(linea.duracion for linea in cita.lineas_ids)
            
            # Sumamos el precio de todas las líneas
            cita.importe_total = sum(linea.precio for linea in cita.lineas_ids)
            
            # Calculamos la Fecha Fin
            # Usamos timedelta para sumar "horas" a una fecha
            cita.fecha_fin = cita.fecha_inicio + timedelta(hours=horas_totales)

    # VALIDACIONES
    # @api.constrains le dice a Odoo: "Cada vez que estos campos cambien, ejecuta esta función para validar".
    @api.constrains('estilista_id', 'fecha_inicio', 'fecha_fin')

    # Función para comprobar citas solapadas
    def _check_solapamiento(self):
        #Evita que un mismo estilista tenga citas solapadas.

        #Detalle del decorador:
        # - @api.constrains: se ejecuta automáticamente cuando cambian los campos
        #   indicados, y permite bloquear operaciones que violen reglas de negocio.
        
        for cita in self:
            # Si la cita está cancelada, no importa si se solapa
            if cita.state == 'cancelada':
                continue

            # Buscamos en la base de datos si existe otra cita
            citas_superpuestas = self.search([
                ('id', '!=', cita.id),             # que no sea esta misma
                ('estilista_id', '=', cita.estilista_id.id), # del mismo estilista
                ('state', '!=', 'cancelada'),      # que no esté cancelada
                # que coincida en el tiempo (Lógica de solapamiento)
                ('fecha_inicio', '<', cita.fecha_fin),
                ('fecha_fin', '>', cita.fecha_inicio)
            ])
            
            if citas_superpuestas:
                # Si encontramos alguna cita que se solapa, lanzamos un error
                raise ValidationError(f"¡El estilista {cita.estilista_id.name} ya tiene una cita en ese horario!")
    
    # ACCIONES PARA CAMBIAR ESTADO
    def action_confirmar(self):
        #Pasa la cita a estado confirmado.

        for rec in self:
            rec.state = 'confirmada'

    def action_realizar(self):
        #Marca la cita como realizada al finalizar el servicio.

        for rec in self:
            rec.state = 'realizada'

    def action_cancelar(self):
        for rec in self:
            rec.state = 'cancelada'

# Tabla intermedia para los servicios en una cita
class StylehubCitaLinea(models.Model):
    #Detalle de servicios asociados a una cita.

    #Esta tabla intermedia permite personalizar precio y duración por cita
    #sin alterar el catálogo global de servicios.

    _name = 'stylehub.cita.linea'
    _description = 'Línea de Servicio en Cita'

    # Relación: la línea pertenece a una cita específica.
    cita_id = fields.Many2one('stylehub.cita', string='Cita')
    # Relación: la línea referencia el servicio del catálogo.
    servicio_id = fields.Many2one('stylehub.servicio', string='Servicio', required=True)
    
    # Estos campos se copiarán del servicio, pero permitimos editarlos
    precio = fields.Float(string='Precio')
    duracion = fields.Float(string='Duración (Horas)')

    # Al cambiar el servicio, copiamos precio y duración
    # @api.onchange se ejecuta en el formulario cuando el usuario cambia el campo.
    # Su objetivo es mejorar la experiencia de usuario rellenando datos sugeridos. (me lo ha recomendado chatgpt)
    @api.onchange('servicio_id')
    def _onchange_servicio_id(self):
        #Rellena precio y duración según el servicio elegido.

        # Si el usuario elige un servicio...
        if self.servicio_id:
            # ...copiamos el precio y duración de ese servicio a esta línea
            self.precio = self.servicio_id.precio
            self.duracion = self.servicio_id.duracion