from odoo import models, fields, tools


class PhotovoltaicPowerEnergy(models.Model):
    _inherit = "photovoltaic.power.energy"

    @tools.ormcache()
    def _compute_total_tn_co2_avoided(self):
        energy = self.env['photovoltaic.power.energy'].sudo().search([('photovoltaic_power_station_id','!=','SDL')])
        return round(sum(energy.mapped('tn_co2_avoided')), 2)

    @tools.ormcache()
    def _compute_energy_generated(self):
        energy = self.env['photovoltaic.power.energy'].sudo().search([('photovoltaic_power_station_id','!=','SDL')])
        return round(sum(energy.mapped('energy_generated')) / 1000, 2)