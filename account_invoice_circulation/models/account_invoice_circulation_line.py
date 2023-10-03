from odoo import fields, models


class AccountInvoiceCirculationLine(models.Model):

    _name = "account.invoice.circulation.line"
    _order = "sequence, id"
    _description = "Invoice circulation rule line"

    circulation_id = fields.Many2one(
        comodel_name="account.invoice.circulation", required=True
    )

    sequence = fields.Integer(string="Sequence")

    user_id = fields.Many2one(
        comodel_name="res.users", string="Approver", required=True
    )
