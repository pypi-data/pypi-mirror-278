# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = ["account.move.line"]

    payment_request_ids = fields.One2many(
        string="Payment Requests",
        comodel_name="payment_request",
        inverse_name="move_line_id",
    )

    def _create_payment_request(self, batch):
        self.ensure_one()
        PaymentRequest = self.env["payment_request"]
        PaymentRequest.create(self._prepare_create_payment_request(batch))

    def _prepare_create_payment_request(self, batch):
        self.ensure_one()
        return {
            "date": batch.date,
            "type_id": batch.type_id.id,
            "partner_id": self.partner_id.id,
            "move_line_id": self.id,
            "amount_payment": self.amount_residual_currency * -1.0,
            "batch_payment_request_id": batch.id,
            "partner_bank_id": self.partner_id.bank_ids
            and self.partner_id.bank_ids[0].id
            or False,
        }
