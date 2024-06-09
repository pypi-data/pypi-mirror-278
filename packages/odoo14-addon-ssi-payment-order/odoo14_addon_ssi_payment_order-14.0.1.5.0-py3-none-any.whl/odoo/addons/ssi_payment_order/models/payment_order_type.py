# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentOrderType(models.Model):
    _name = "payment_order_type"
    _inherit = [
        "mixin.master_data",
        "mixin.res_partner_bank_m2o_configurator",
    ]
    _description = "Payment Order Type"

    _res_partner_bank_m2o_configurator_insert_form_element_ok = True
    _res_partner_bank_m2o_configurator_form_xpath = "//page[@name='partner']"

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )
    realization_method = fields.Selection(
        string="Realization Method",
        selection=[
            ("manual", "Manual Realization"),
        ],
        required=True,
        default="manual",
    )
    require_bank_account = fields.Boolean(
        string="Require Bank Account",
        default=False,
    )
