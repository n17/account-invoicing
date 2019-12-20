from odoo import fields, models


class AccountConfigSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    default_overdue_interest = fields.Float(
        related='company_id.default_overdue_interest',
        help='''Default overdue interest % for new customers and invoices ''')
