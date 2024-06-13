from odoo import models, api, fields, tools

class Partner(models.Model):
    _inherit = "res.partner"

    interest_ids = fields.Many2many('res.partner.interest', column1='partner_id',
                                    column2='category_id', string='Interests')

    @tools.ormcache()
    def _compute_plant_participants(self):
        participants = self.env['res.partner'].sudo().search([('participant', '=', True)])
        return len(participants)