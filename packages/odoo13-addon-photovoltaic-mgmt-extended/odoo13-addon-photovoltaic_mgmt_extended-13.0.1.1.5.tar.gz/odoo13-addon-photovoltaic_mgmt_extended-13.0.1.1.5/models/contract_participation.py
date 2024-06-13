from odoo import models, api, fields, tools

class ContractParticipation(models.Model):
    _inherit = "contract.participation"

    # When payment information is set and the sate payment pending, automatically set the contract state to active
    @api.onchange('payment_mode_id', 'payment_date')
    def _on_payment_set(self):
        stage_active  = self.env["contract.participation.stage"].search([('valid', '=', 'True')])
        stage_pending = self.env["contract.participation.stage"].search([('default', '=', 'True')])
        for record in self:
            if record.payment_mode_id.id and record.payment_date and record.stage_id.id == stage_pending.id:
                record.stage_id = stage_active

    crece_activation_date   = fields.Datetime(string='Crece Solar fecha activación')
    crece_deactivation_date = fields.Datetime(string='Crece Solar fecha desactivación')

    crece_active = fields.Boolean(string='Crece Solar activado', compute='_compute_crece_active')
    @api.depends('crece_activation_date', 'crece_deactivation_date')
    def _compute_crece_active(self):
        for record in self:
            record.crece_active = record.crece_activation_date and not record.crece_deactivation_date

    @tools.ormcache()
    def _compute_total_inversion(self):
        contracts = self.env['contract.participation'].sudo().search([('stage_id.valid', '=', True)])
        inversion = sum(contracts.mapped('inversion'))
        base_inversion = float(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_mgmt.accumulated_inversion'))
        return round(inversion + base_inversion, 2) if base_inversion else round(inversion, 2)

    @tools.ormcache()
    def _compute_total_investors(self):
        contracts = self.env['contract.participation'].sudo().search([('stage_id.valid', '=', True)])
        base_investors = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_mgmt.total_investors'))
        return len(contracts) + base_investors if base_investors else len(contracts)