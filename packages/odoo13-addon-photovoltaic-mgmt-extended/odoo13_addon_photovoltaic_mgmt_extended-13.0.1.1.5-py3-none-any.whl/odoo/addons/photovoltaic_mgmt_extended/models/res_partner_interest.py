from odoo import models, api, fields

class ResPartnerInterest(models.Model):
    
    _description = 'Partner Interest'
    _name = 'res.partner.interest'
    _order = 'name'
    _inherit='res.partner.category'
    _parent_store = True