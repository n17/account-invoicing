from email_validator import EmailNotValidError, validate_email

from odoo import _, models
from odoo.exceptions import ValidationError


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    def send_and_print_action(self):
        for invoice in self.invoice_ids:
            partner = invoice.partner_id
            if not partner.invoice_email:
                raise ValidationError(
                    _("Partner '{}' has no invoice email address").format(partner.name)
                )

            try:
                validate_email(partner.invoice_email)
            except EmailNotValidError as err:
                raise ValidationError(
                    _("Partner '{}' invoice email address '{}' is not valid").format(
                        partner.name, partner.invoice_email
                    )
                ) from err

        return super(AccountInvoiceSend, self).send_and_print_action()
