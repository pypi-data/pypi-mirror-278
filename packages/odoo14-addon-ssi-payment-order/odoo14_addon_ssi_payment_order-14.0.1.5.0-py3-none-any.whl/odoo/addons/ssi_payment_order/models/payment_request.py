# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class PaymentRequest(models.Model):
    _name = "payment_request"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
    ]
    _description = "Payment Request"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        default=lambda r: r._default_date(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="payment_request_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    min_overdue = fields.Integer(
        related="type_id.min_overdue",
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        compute="_compute_allowed_account_ids",
        store=False,
    )
    allowed_partner_ids = fields.Many2many(
        string="Allowed Partners",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_ids",
        store=False,
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_ids",
        store=False,
    )
    allowed_currency_ids = fields.Many2many(
        string="Allowed Currencies",
        comodel_name="res.currency",
        compute="_compute_allowed_currency_ids",
        store=False,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_id = fields.Many2one(
        related="move_line_id.account_id",
        store=True,
    )
    analytic_account_id = fields.Many2one(
        related="move_line_id.analytic_account_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        related="move_line_id.currency_id",
        store=True,
    )
    amount_payment = fields.Monetary(
        string="Amount Payment",
        currency_field="currency_id",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_bank_id = fields.Many2one(
        string="Bank Account",
        comodel_name="res.partner.bank",
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    bank_id = fields.Many2one(
        string="Bank",
        related="partner_bank_id.bank_id",
        store=True,
    )
    payment_order_id = fields.Many2one(
        string="# Payment Order",
        comodel_name="payment_order",
        readonly=True,
    )
    payment_order_status = fields.Selection(
        string="Payment Order Status",
        related="payment_order_id.state",
        store=True,
    )
    batch_payment_request_id = fields.Many2one(
        string="# Batch Payment Request",
        comodel_name="batch_payment_request",
        readonly=True,
        ondelete="cascade",
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "type_id",
    )
    def onchange_partner_id(self):
        self.partner_id = False

    @api.onchange(
        "partner_id",
    )
    def onchange_move_line_id(self):
        self.move_line_id = False

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_bank_id(self):
        self.partner_bank_id = False

    @api.onchange(
        "move_line_id",
    )
    def onchange_amount_payment(self):
        self.amount_payment = 0.0
        if self.move_line_id:
            self.amount_payment = -1.0 * self.move_line_id.amount_residual_currency

    @api.depends("type_id")
    def _compute_allowed_account_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.account",
                    method_selection=record.type_id.account_selection_method,
                    manual_recordset=record.type_id.account_ids,
                    domain=record.type_id.account_domain,
                    python_code=record.type_id.account_python_code,
                )
            record.allowed_account_ids = result

    @api.depends("type_id")
    def _compute_allowed_partner_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.partner",
                    method_selection=record.type_id.partner_selection_method,
                    manual_recordset=record.type_id.partner_ids,
                    domain=record.type_id.partner_domain,
                    python_code=record.type_id.partner_python_code,
                )
            record.allowed_partner_ids = result

    @api.depends("type_id")
    def _compute_allowed_journal_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.journal",
                    method_selection=record.type_id.journal_selection_method,
                    manual_recordset=record.type_id.journal_ids,
                    domain=record.type_id.journal_domain,
                    python_code=record.type_id.journal_python_code,
                )
            record.allowed_journal_ids = result

    @api.depends("type_id")
    def _compute_allowed_currency_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.currency",
                    method_selection=record.type_id.currency_selection_method,
                    manual_recordset=record.type_id.currency_ids,
                    domain=record.type_id.currency_domain,
                    python_code=record.type_id.currency_python_code,
                )
            record.allowed_currency_ids = result

    @api.model
    def _get_policy_field(self):
        res = super(PaymentRequest, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
