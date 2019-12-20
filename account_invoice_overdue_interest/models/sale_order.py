from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def _prepare_invoice(self):
        # Handling for when invoicing the invoiceable lines
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['overdue_interest'] \
            = self.partner_id.overdue_interest \
            or self.company_id.default_overdue_interest

        return invoice_vals
