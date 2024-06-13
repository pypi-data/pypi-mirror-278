from odoo import models, fields, tools


class PhotovoltaicPowerStation(models.Model):
    _inherit = "photovoltaic.power.station"

    tecnical_memory_link = fields.Char(string="Enlace memoria técnica")

    eq_family_consumption = fields.Float(
        string='Consumo equivalente en familia',
        compute='_compute_eq_family_consumption',
        tracking=True)

    short_term_investment = fields.Boolean(string='Plant available for sort term investment')
    long_term_investment = fields.Boolean(string='Plant available for long term investment')

    stock_location = fields.Many2one('stock.location', domain=[('usage', '=', 'internal')])
    stock_quants = fields.Many2many('stock.quant', compute='_compute_stock_quant')

    def _compute_eq_family_consumption(self):
        for record in self:
            record.eq_family_consumption = sum(record.photovoltaic_power_energy_ids.mapped('eq_family_consum'))

    def _compute_stock_quant(self):
        for record in self:
            if record.stock_location:
                record.stock_quants = self.env['stock.quant'].search([
                    ('location_id', '=', record.stock_location.id)
                ])
            else:
                record.stock_quants = []

    def toggle_short_term(self):
        self.short_term_investment = not self.short_term_investment

    def toggle_long_term(self):
        self.long_term_investment = not self.long_term_investment

    @tools.ormcache()
    def _compute_installed_power(self):
        plants = self.env['photovoltaic.power.station'].sudo().search([('name','!=','SDL')])
        return round(sum(plants.mapped('peak_power')) / 1000, 2)

    @tools.ormcache()
    def _compute_plants_with_reservation(self):
        plants_with_reservation = self.env['photovoltaic.power.station'].sudo().search(
            [('reservation', '>=', 0)])
        return len(plants_with_reservation)