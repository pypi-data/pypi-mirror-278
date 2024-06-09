# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentRequestType(models.Model):
    _name = "payment_request_type"
    _inherit = [
        "mixin.master_data",
        "mixin.account_account_m2o_configurator",
        "mixin.account_journal_m2o_configurator",
        "mixin.res_partner_m2o_configurator",
        "mixin.res_currency_m2o_configurator",
    ]
    _description = "Payment Request Type"
    _account_account_m2o_configurator_insert_form_element_ok = True
    _account_account_m2o_configurator_form_xpath = "//page[@name='account']"
    _account_journal_m2o_configurator_insert_form_element_ok = True
    _account_journal_m2o_configurator_form_xpath = "//page[@name='account']"
    _res_partner_m2o_configurator_insert_form_element_ok = True
    _res_partner_m2o_configurator_form_xpath = "//page[@name='partner']"
    _res_currency_m2o_configurator_insert_form_element_ok = True
    _res_currency_m2o_configurator_form_xpath = "//page[@name='account']"

    min_overdue = fields.Integer(
        string="Min. Overdue",
        required=True,
        default=0,
    )
    max_overdue = fields.Integer(
        string="Max. Overdue",
        required=True,
        default=0,
    )
