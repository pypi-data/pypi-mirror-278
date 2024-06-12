# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

from odoo.addons.queue_job.delay import chain
from odoo.addons.ssi_decorator import ssi_decorator


class StockBalance(models.Model):
    _name = "stock_balance"
    _description = "Stock Balance"
    _inherit = [
        "mixin.transaction_queue_cancel",
        "mixin.transaction_queue_done",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "action_queue_done"
    _approval_state = "confirm"
    _after_approved_method = "action_queue_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _queue_processing_create_page = True
    _automatically_insert_queue_done_button = False
    _automatically_insert_queue_cancel_button = False

    _queue_to_done_insert_form_element_ok = True
    _queue_to_done_form_xpath = "//group[@name='queue_processing']"

    _queue_to_cancel_insert_form_element_ok = True
    _queue_to_cancel_form_xpath = "//group[@name='queue_processing']"

    _method_to_run_from_wizard = "action_queue_cancel"

    _statusbar_visible_label = "draft,confirm,queue_done,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "queue_cancel_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "queue_done_ok",
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
        "dom_queue_done",
        "dom_done",
        "dom_terminate",
        "dom_queue_cancel",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    type_id = fields.Many2one(
        comodel_name="stock_balance_type",
        string="Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    product_ids = fields.Many2many(
        string="Products",
        comodel_name="product.product",
        relation="rel_stock_balance_2_product",
        column1="stock_balance_id",
        column2="product_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    product_stock_balance_ids = fields.One2many(
        string="Product Stock Balances",
        comodel_name="product.stock_balance",
        inverse_name="stock_balance_id",
        readonly=True,
    )
    product_stock_balance_warehouse_ids = fields.One2many(
        string="Product Stock Balances - Warehouse",
        comodel_name="product.stock_balance_warehouse",
        inverse_name="sb_id",
        readonly=True,
    )
    product_stock_balance_picking_ids = fields.One2many(
        string="Product Stock Balances - Picking",
        comodel_name="product.stock_balance_picking",
        inverse_name="sb_id",
        readonly=True,
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Product Category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.product_category_selection_method,
                    manual_recordset=record.type_id.product_category_ids,
                    domain=record.type_id.product_category_domain,
                    python_code=record.type_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    def action_create_product_stock_balance(self):
        for record in self.sudo():
            record._create_product_stock_balance()
            record.product_stock_balance_ids._compute_previous_product_stock_balance_id()

    @ssi_decorator.post_queue_done_action()
    def _01_generate_stock_balance_report(self):
        self.ensure_one()
        ProductSB = self.env["product.stock_balance"]
        sb_delayables = []
        for product in self.product_ids:
            criteria = [
                ("product_id", "=", product.id),
                ("stock_balance_id", "=", self.id),
            ]
            for sb in ProductSB.search(criteria):
                description = "Generate stock balance for product ID %s for %s" % (
                    product.id,
                    sb.date,
                )
                current_sb_delayable = (
                    sb.with_context(job_batch=self.done_queue_job_batch_id)
                    .delayable(description=_(description))
                    .action_create_stock_balance_warehouse()
                )
                sb_delayables.append(current_sb_delayable)
                description = "Compute beginning value/qty for product ID %s for %s" % (
                    sb.product_id.id,
                    sb.date,
                )
                current_sb1_delayable = (
                    sb.with_context(job_batch=self.done_queue_job_batch_id)
                    .delayable(description=_(description))
                    .action_compute_beginning()
                )
                sb_delayables.append(current_sb1_delayable)

            sb_delayables = sb_delayables
            chain(*sb_delayables).delay()

    @ssi_decorator.post_cancel_action()
    def _01_delete_product_stock_balance(self):
        self.ensure_one()
        self.product_stock_balance_ids.unlink()

    def _get_date_list(self):
        self.ensure_one()
        dates = []
        current_date = fields.Date.to_date(self.date_start)
        date_end = fields.Date.to_date(self.date_end)
        while current_date <= date_end:
            dates.append(current_date)
            current_date = fields.Date.add(current_date, days=1)
        return dates

    def _create_product_stock_balance(self):
        self.ensure_one()
        self.product_stock_balance_ids.unlink()
        ProductSB = self.env["product.stock_balance"]
        for product in self.product_ids:
            for stock_balance_date in self._get_date_list():
                ProductSB.create(
                    {
                        "stock_balance_id": self.id,
                        "product_id": product.id,
                        "date": fields.Date.to_string(stock_balance_date),
                    }
                )

    @api.model
    def _get_policy_field(self):
        res = super(StockBalance, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "queue_cancel_ok",
            "done_ok",
            "queue_done_ok",
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
