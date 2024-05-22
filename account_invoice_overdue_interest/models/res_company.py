from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    overdue_interest = fields.Float(string="Overdue interest %", digits=(4, 2))
