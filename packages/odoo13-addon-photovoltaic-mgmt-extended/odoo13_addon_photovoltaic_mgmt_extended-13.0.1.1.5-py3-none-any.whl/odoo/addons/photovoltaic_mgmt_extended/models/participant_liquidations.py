from odoo import models, fields

class ParticipantLiquidations(models.Model):
    _inherit = 'participant.liquidations'

    state = fields.Selection(
        selection_add=[
            ('reinversion_iva', 'Reinversión IVA'),
            ('crece_acumulado', 'Crece Solar - acumulado'),
            ('crece_reinvertido', 'Crece Solar - reinvertido'),
            ('donacion', 'Donación'),
        ]
    )

