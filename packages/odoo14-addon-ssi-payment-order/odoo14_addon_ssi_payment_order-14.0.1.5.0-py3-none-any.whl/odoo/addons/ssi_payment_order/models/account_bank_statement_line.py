# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _name = "account.bank.statement.line"
    _inherit = ["account.bank.statement.line"]

    payment_request_id = fields.Many2one(
        string="# Payment Request",
        comodel_name="payment_request",
    )

    @api.onchange("payment_request_id")
    def onchange_partner_id(self):
        self.partner_id = False
        if self.payment_request_id:
            self.partner_id = self.payment_request_id.partner_id

    @api.onchange("payment_request_id")
    def onchange_amount(self):
        self.amount = 0.0
        if self.payment_request_id:
            self.amount = -1.0 * self.payment_request_id.amount_payment

    @api.onchange("payment_request_id")
    def onchange_payment_ref(self):
        self.payment_ref = False
        if self.payment_request_id:
            self.payment_ref = self.payment_request_id.move_line_id.name

    @api.onchange("payment_request_id")
    def onchange_ref(self):
        self.ref = False
        if self.payment_request_id:
            self.ref = self.payment_request_id.name
