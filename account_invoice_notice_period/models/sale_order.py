from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _prepare_invoice(self):
        # Handling for when invoicing the invoiceable lines
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["notice_period"] = (
            self.partner_id.notice_period or self.company_id.notice_period
        )

        return invoice_vals
