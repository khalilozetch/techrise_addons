# -*- coding: utf-8 -*-
# =============================================================================
# Model: Account Asset Extension
# Description: Extends account assets with asset type classification
# =============================================================================

from odoo import fields, models


class AccountAsset(models.Model):
    """
    Extension of Account Asset for asset type classification.

    Adds field for categorizing assets as:
    - Assets (Fixed Assets)
    - Deferred Expenses
    - Deferred Revenue
    """
    _inherit = 'account.asset'

    # =========================================================================
    # FIELDS - Asset Classification
    # =========================================================================
    asset_type = fields.Selection(
        selection=[
            ('assets', 'Assets'),
            ('deferred_expenses', 'Deferred Expenses'),
            ('deferred_revenue', 'Deferred Revenue'),
            ('prepayments', 'Prepayments'),
        ],
        string="Type",
        default='assets',
        help="Classification of the asset for accounting purposes:\n"
             "- Assets: Fixed assets with depreciation\n"
             "- Deferred Expenses: Prepaid expenses to be amortized\n"
             "- Deferred Revenue: Unearned revenue to be recognized\n"
             "- Prepayments: Prepaid expenses",
    )


class AccountAccount(models.Model):
    _inherit = 'account.account'

    account_type = fields.Selection(
        selection_add=[
            ("prepayments", "Prepayments"),
        ], ondelete={'prepayments': 'cascade'}
    )
