# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################
{
    'name': 'Website Custom Options',
    'summary': """
        This module adds support of custom option for product in odoo website.
    """,
    'description': """
        This module adds support of custom option for product in odoo website.
    """,
    'author': 'Webkul Software Pvt. Ltd.',
    'website': 'https://store.webkul.com/Odoo-Website-Custom-Options.html',
    'license': 'Other proprietary',
    'category': 'Website',
    'sequence': '1',
    'version': '1.2.3',
    'live_test_url': 'http://odoodemo.webkul.com/?module=website_custom_options&version=12.0',
    'depends': ['website_sale', 'product_custom_options'],
    'data': [
        'views/templates.xml',
        'views/website_custom_options.xml',
    ],
    'images': ['static/description/Banner.png'],
    'application': True,
    'pre_init_hook': 'pre_init_check',
    'price': 80,
    'currency': 'EUR',
}
