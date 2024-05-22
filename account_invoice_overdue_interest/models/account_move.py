from odoo import api, fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    overdue_interest = fields.Float(
        string="Overdue interest %",
        digits=(4, 2),
        compute="_compute_overdue_interest",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("partner_id")
    def _compute_overdue_interest(self):
        for record in self:
            record.overdue_interest = (
                record.partner_id.overdue_interest or record.company_id.overdue_interest
            )
