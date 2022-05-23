from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    salesperson_email = fields.Char()

    @api.onchange("user_id")
    def user_id_onchange_phone_and_email(self):
        email = self.user_id.partner_id.email or ""

        self.comment = self.comment or ""

        if self.salesperson_email:
            self.comment = self.comment.replace(
                "\n" + _("Handler: ") + self.salesperson_email, ""
            ).replace(_("Handler: ") + self.salesperson_email, "")

        email_line = "\n" if self.comment else ""

        if email:
            self.comment += "{}{}{}".format(email_line, _("Handler: "), email)

        self.salesperson_email = self.user_id.partner_id.email
