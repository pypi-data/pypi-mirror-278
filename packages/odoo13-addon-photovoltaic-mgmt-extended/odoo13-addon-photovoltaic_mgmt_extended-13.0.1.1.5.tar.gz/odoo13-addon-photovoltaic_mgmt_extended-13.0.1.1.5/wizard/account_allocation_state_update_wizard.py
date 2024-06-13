from attr import s
from odoo import fields, models

class AccountAllocationStateUpdate(models.TransientModel):
    _name = 'account.allocation.state.update.wizard'
    _description = 'Wizard to update account allocation state in bulk'
    _inherit = 'account.allocation'

    def update_state(self):
        # Get IDs of all selected account_allocations
        allocations = self.env["account.allocation"].browse(self.env.context.get("active_ids"))

        for allocation in allocations:
            allocation.state = self.state
