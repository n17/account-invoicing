from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    invoice_ids = fields.Many2many(
        comodel_name="account.move",
        related="sale_id.invoice_ids",
    )

    invoice_count = fields.Integer(
        related="sale_id.invoice_count",
    )

    # @api.multi
    def action_view_invoice(self):
        action = self.env.ref("account.view_out_invoice_tree").read()[0]

        if len(self.invoice_ids) == 0:
            form_view_name = "account.view_move_form"
            action["views"] = [(self.env.ref(form_view_name).id, "form")]
        else:
            action["domain"] = [("id", "in", self.invoice_ids.ids)]

        return action

    # @api.multi
    def button_validate(self):
        if self.has_open_invoices():
            # Don't allow validating pickings if they have open invoices
            raise ValidationError(
                _(
                    "You cannot confirm the transfer because some of the invoices "
                    "are still pending!"
                )
            )
        else:
            return super().button_validate()

    def has_open_invoices(self):
        self.ensure_one()
        # Only check lines with policy "Invoice delivered"
        so_lines_to_deliver = self.sudo().sale_id.order_line.filtered(
            lambda r: r.product_id.invoice_policy == "delivery"
        )
        states = so_lines_to_deliver.mapped("order_id.invoice_ids.state")
        is_open = "to invoice" in states or "draft" in states or "in payment" in states

        return is_open