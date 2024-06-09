# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class BatchPaymentRequest(models.Model):
    _name = "batch_payment_request"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]
    _description = "Batch Payment Request"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
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
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

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
    max_overdue = fields.Integer(
        related="type_id.max_overdue",
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
        inverse_name="batch_payment_request_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

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

    def action_populate(self):
        for record in self.sudo():
            record._populate()

    def _populate(self):
        self.ensure_one()
        self.payment_request_ids.unlink()
        domain1 = self._prepare_aml_domain()
        AML = self.env["account.move.line"]
        if not self.date_start and not self.date_end:
            aml = AML.search(domain1)
        elif self.date_start and not self.date_end:
            domain2 = domain1 + [
                ("date_maturity", "!=", False),
                ("date_maturity", ">=", self.date_start),
            ]
            aml = AML.search(domain2)
            domain2 = domain1 + [
                ("date_maturity", "=", False),
                ("date", ">=", self.date_start),
            ]
            aml += AML.search(domain2)
        elif not self.date_start and self.date_end:
            domain2 = domain1 + [
                ("date_maturity", "!=", False),
                ("date_maturity", "<=", self.date_end),
            ]
            aml = AML.search(domain2)
            domain2 = domain1 + [
                ("date_maturity", "=", False),
                ("date", "<=", self.date_end),
            ]
            aml += AML.search(domain2)
        elif self.date_start and self.date_end:
            domain2 = domain1 + [
                ("date_maturity", "!=", False),
                ("date_maturity", ">=", self.date_start),
                ("date_maturity", "<=", self.date_end),
            ]
            aml = AML.search(domain2)
            domain2 = domain1 + [
                ("date_maturity", "=", False),
                ("date", ">=", self.date_start),
                ("date", "<=", self.date_end),
            ]
            aml += AML.search(domain2)
        for line in aml:
            line._create_payment_request(self)

    def _prepare_aml_domain(self):
        self.ensure_one()
        result = [
            ("account_id", "in", self.allowed_account_ids.ids),
            ("journal_id", "in", self.allowed_journal_ids.ids),
            ("currency_id", "in", self.allowed_currency_ids.ids),
            ("partner_id", "in", self.allowed_partner_ids.ids),
            ("credit", ">", 0.0),
            ("full_reconcile_id", "=", False),
            ("move_id.state", "=", "posted"),
        ]
        return result

    @ssi_decorator.post_cancel_action()
    def _10_delete_payment_request(self):
        self.ensure_one()
        self.payment_request_ids.unlink()

    @api.model
    def _get_policy_field(self):
        res = super(BatchPaymentRequest, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
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
