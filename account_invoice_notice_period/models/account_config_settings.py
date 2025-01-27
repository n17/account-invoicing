# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountConfigSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    default_notice_period = fields.Integer(
        string='Notice period (days)',
        related='company_id.default_notice_period',
        help='Default notice period (days) for new customers and invoices',
    )
