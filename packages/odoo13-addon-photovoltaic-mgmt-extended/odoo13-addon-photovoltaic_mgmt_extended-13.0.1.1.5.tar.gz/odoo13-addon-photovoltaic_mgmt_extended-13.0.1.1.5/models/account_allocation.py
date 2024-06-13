from odoo import models, api, fields, tools

class AccountAllocation(models.Model):
    _inherit = 'account.allocation'

    state = fields.Selection(
        selection_add=[
            ('reinversion_iva', 'Reinversión IVA'),
            ('crece_acumulado', 'Crece Solar - acumulado'),
            ('crece_reinvertido', 'Crece Solar - reinvertido')
        ]
    )

    @tools.ormcache()
    def _compute_total_benefits(self):
        allocations = self.env['account.allocation'].sudo().search([])
        benefits = sum(allocations.mapped('total'))
        base_benefits = float(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_mgmt.million_benefits'))
        return round(benefits + base_benefits, 2) if base_benefits else round(benefits, 2)