# -*- coding: utf-8 -*-
# =============================================================================
# Module: Account Asset Extension
# Description: Extends account assets with asset type classification
#              (Assets, Deferred Expenses, Deferred Revenue)
# =============================================================================

{
    'name': 'Account Asset Extension',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Asset Type Classification for Assets, Deferred Expenses and Revenue',
    'description': """
Account Asset Extension
=======================
This module extends the account asset functionality with:

* Asset Type field (Assets, Deferred Expenses, Deferred Revenue)
* Separate menu items for each asset type
* Dynamic field labels based on asset type
* Filtered actions for each asset type

Menu Structure:
--------------
Accounting > Journal Entries > Assets
    - Assets
    - Deferred Expenses
    - Deferred Revenue
    """,
    'author': 'Aldalil',
    'depends': ['account_asset'],
    'data': [
        'views/account_asset_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
