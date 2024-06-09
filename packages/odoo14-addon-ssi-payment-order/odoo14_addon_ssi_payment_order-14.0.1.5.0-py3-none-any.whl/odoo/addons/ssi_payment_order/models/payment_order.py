# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class PaymentOrder(models.Model):
    _name = "payment_order"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]
    _description = "Payment Order"

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

    type_id = fields.Many2one(
        string="Type",
        comodel_name="payment_order_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        ondelete="restrict",
        domain=[
            ("parent_id", "=", False),
        ],
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        compute="_compute_currency_id",
        related=False,
        store=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        required=False,
    )
    date_end = fields.Date(
        required=False,
    )
    payment_request_ids = fields.One2many(
        string="Payment Requests",
        comodel_name="payment_request",
        inverse_name="payment_order_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_request = fields.Monetary(
        string="Amount Request",
        currency_field="currency_id",
        compute="_compute_amount_request",
        store=True,
    )
    move_ids = fields.One2many(
        string="Journal Entries",
        comodel_name="account.move",
        inverse_name="payment_order_id",
    )
    move_id = fields.Many2one(
        string="Journal Entry",
        comodel_name="account.move",
        compute="_compute_move_id",
        store=True,
    )
    move_state = fields.Selection(
        string="Journal Entry Status",
        related="move_id.state",
        store=True,
    )
    realization_ok = fields.Boolean(
        string="Can Realized",
        compute="_compute_realization_ok",
        store=False,
        compute_sudo=True,
    )
    allowed_partner_bank_ids = fields.Many2many(
        string="Allowed Bank Accounts",
        comodel_name="res.partner.bank",
        compute="_compute_allowed_partner_bank_ids",
        store=False,
    )

    @api.depends(
        "type_id",
        "company_id",
    )
    def _compute_currency_id(self):
        for record in self:
            result = False
            if record.company_id:
                result = record.company_id.currency_id
            if record.type_id:
                if record.type_id.journal_id.currency_id:
                    result = record.type_id.journal_id.currency_id
            record.currency_id = result

    @api.depends(
        "state",
    )
    def _compute_realization_ok(self):
        for record in self:
            result = True

            if record.state != "open":
                result = False

            for field_name in self._get_realization_field():
                if getattr(self, field_name):
                    result = False

            record.realization_ok = result

    @api.model
    def _get_realization_field(self):
        return ["move_id"]

    @api.depends(
        "move_ids",
    )
    def _compute_move_id(self):
        for record in self:
            result = False
            if record.move_ids:
                result = record.move_ids[0]
            record.move_id = result

    @api.depends(
        "move_id",
        "move_id.state",
    )
    def _compute_move_state(self):
        for record in self:
            result = False
            if record.move_id:
                result = record.move_id.state
            record.move_state = result

    @api.depends(
        "payment_request_ids",
        "payment_request_ids.amount_payment",
    )
    def _compute_amount_request(self):
        for record in self:
            result = 0.0
            for payment_request in record.payment_request_ids:
                result += payment_request.amount_payment
            record.amount_request = result

    @api.depends("type_id")
    def _compute_allowed_partner_bank_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.partner.bank",
                    method_selection=record.type_id.partner_bank_selection_method,
                    manual_recordset=record.type_id.partner_bank_ids,
                    domain=record.type_id.partner_bank_domain,
                    python_code=record.type_id.partner_bank_python_code,
                )
            record.allowed_partner_bank_ids = result

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def action_create_realization(self):
        for record in self.sudo():
            record._create_realization()

    def action_populate_payment_request(self):
        for record in self.sudo():
            record._populate_payment_request()

    def _populate_payment_request(self):
        self.ensure_one()
        self.payment_request_ids.write(
            {
                "payment_order_id": False,
            }
        )
        criteria = [
            ("payment_order_id", "=", False),
            ("state", "=", "open"),
        ]

        if self.partner_id:
            criteria += [
                ("partner_id", "=", self.partner_id.id),
            ]

        if self.date_start:
            criteria += [
                ("date", ">=", self.date_start),
            ]

        if self.date_end:
            criteria += [
                ("date", "<=", self.date_end),
            ]

        if self.type_id.require_bank_account:
            criteria = [
                ("partner_bank_id", "in", self.allowed_partner_bank_ids.ids),
            ]
        else:
            criteria = [
                "|",
                ("partner_bank_id", "=", False),
                ("partner_bank_id", "in", self.allowed_partner_bank_ids.ids),
            ]

        PaymentRequest = self.env["payment_request"]
        payment_requests = PaymentRequest.search(criteria)
        payment_requests.write(
            {
                "payment_order_id": self.id,
            }
        )

    def _create_realization(self):
        self.ensure_one()

        if self.type_id.realization_method == "manual":
            error_message = """
                Context: Create payment order realization
                Database ID: %s
                Problem: Realization method is manual
                Solution: Create journal entry manually
                """ % (
                self.id
            )
            raise UserError(_(error_message))

        realization_method = self.type_id.realization_method
        method_name = "_create_realization_" + realization_method

        if not hasattr(self, method_name):
            error_message = """
                Context: Create payment order realization
                Database ID: %s
                Problem: No realization method for selected payment order type
                Solution: Change payment order type
                """ % (
                self.id
            )
            raise UserError(_(error_message))

        getattr(self, method_name)()

    @api.model
    def _get_policy_field(self):
        res = super(PaymentOrder, self)._get_policy_field()
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
