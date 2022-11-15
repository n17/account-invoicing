from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    payment_date = fields.Date(
        string="Payment date",
        copy=False,
        compute="_compute_payment_date",
        store=True,
    )

    def _get_invoice_in_payment_state(self):
        res = super()._get_invoice_in_payment_state()

        if res == "paid":
            self._compute_payment_date()

        return res

    def _compute_payment_date(self):
        for record in self:
            payments = record._get_reconciled_payments()
            if payments:
                record.payment_date = max(payments.mapped("date"))
            else:
                record.payment_date = False

    def _cron_compute_payment_date(self):
        records = self.search(
            [("payment_date", "=", False), ("payment_state", "=", "paid")]
        )
        records._compute_payment_date()
