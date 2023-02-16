# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

emails_split = re.compile(r"[;,\n\r]+")


class AccountPaymentEmail(models.TransientModel):
    _name = "account.payment.email"
    _description = "Account payment email"

    # composer content
    subject = fields.Char(
        "Subject", compute="_compute_subject", readonly=False, store=True
    )
    body = fields.Html(
        "Contents",
        sanitize_style=True,
        compute="_compute_body",
        readonly=False,
        store=True,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Attachments",
        compute="_compute_attachment_ids",
        readonly=False,
    )
    template_id = fields.Many2one(
        "mail.template",
        "Use template",
        domain="[('model', '=', 'account.payment')]",
        readonly=True,
    )
    # recipients
    partner_ids = fields.Many2many(
        "res.partner",
        string="Recipients",
        compute="_compute_partner_ids",
        readonly=False,
        store=True,
    )

    account_payment_id = fields.Many2one(
        "account.payment", string="Account payment", required=True
    )

    @api.depends("template_id")
    def _compute_subject(self):
        for record in self:
            if record.template_id:
                record.subject = record.template_id.subject
            elif not record.subject:
                record.subject = False

    @api.depends("template_id")
    def _compute_attachment_ids(self):
        for record in self:
            if record.template_id:
                pdf = (
                    self.env.ref(
                        "account_invoice_commission_payment.action_report_payment_commissions"
                    )
                    .sudo()
                    ._render_qweb_pdf(record.account_payment_id.id)
                )
                name = "payment_settlements"
                filename = name + ".pdf"
                create_attachment = (
                    self.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": filename,
                            "type": "binary",
                            "datas": base64.b64encode(pdf[0]),
                            "store_fname": filename,
                            "res_model": "account.payment",
                            "mimetype": "application/pdf",
                        }
                    )
                )

                record.attachment_ids = create_attachment
            elif not record.subject:
                record.subject = False

    @api.depends("template_id")
    def _compute_body(self):
        for record in self:
            if record.template_id:
                record.body = record.template_id.body_html
            elif not record.body:
                record.body = False

    @api.depends("template_id")
    def _compute_partner_ids(self):
        for record in self:
            if record.template_id:
                record.partner_ids = record.account_payment_id.partner_id.ids
            elif not record.partner_ids:
                record.partner_ids = False

    def action_send(self):
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(
                _(
                    "Unable to post message, please configure the sender's email address."
                )
            )

        payment_id = self.account_payment_id
        mail_values = []
        for partner in self.partner_ids:
            mail_values.append(self._add_mail_values(payment_id, partner))

        for mail_value in mail_values:
            new_mail = self.env["mail.mail"].sudo().create(mail_value)
            if new_mail:
                new_mail.send()

        return {"type": "ir.actions.act_window_close"}

    def _add_mail_values(self, payment_id, partner):
        subject = self.env["mail.render.mixin"]._render_template(
            self.subject, "account.payment", payment_id.ids, post_process=True
        )[payment_id.id]
        body = self.env["mail.render.mixin"]._render_template(
            self.body, "account.payment", payment_id.ids, post_process=True
        )[payment_id.id]

        mail_values = {
            "email_from": self.env.user.email_formatted,
            "author_id": self.env.user.partner_id.id,
            "model": "account.payment",
            "res_id": payment_id.id,
            "subject": subject,
            "body_html": body,
            "attachment_ids": [(4, att.id) for att in self.attachment_ids],
            "auto_delete": True,
            "recipient_ids": [(4, partner.id)],
        }
        mail_values["body_html"] = self.env["mail.render.mixin"]._replace_local_links(
            body
        )

        payment_id.sudo().message_post(
            message_type="comment",
            subtype_xmlid="mail.mt_note",
            subject=subject,
            body=body,
            notify_by_email=False,
            attachment_ids=self.attachment_ids.ids,
        )

        return mail_values