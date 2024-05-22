from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    overdue_interest = fields.Float(
        string="Overdue interest %",
        related="company_id.overdue_interest",
        help="Default overdue interest % for new customers and invoices",
        readonly=False,
    )
