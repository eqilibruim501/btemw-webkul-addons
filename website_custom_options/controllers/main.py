# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


import json

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleCustom(WebsiteSale):

    def _filter_custom_options(self, **kw):
        custom_options = {
            k.split('-')[2]: v for k,
            v in kw.items() if "custom_options" in k}
        custom_option_checkbox = {
            k: v for k, v in kw.items() if "custom_option_checkbox" in k}
        custom_option_multiple = {
            k: v for k, v in kw.items() if "custom_option_multiple" in k}
        for optionName in custom_option_multiple.keys():
            optionId = optionName.split('-')[2]
            selectedIds = request.httprequest.form.getlist(optionName)
            custom_options.update({optionId: selectedIds})
        for optionName, valueId in custom_option_checkbox.items():
            optionId = optionName.split('-')[2]
            inputData = custom_options.get(optionId, [])
            inputData += [valueId]
            custom_options.update({optionId: inputData})
        if kw.get("file_name"):
            custom_options.update({
            "file_name":kw.get("file_name")
            })
        return custom_options

    @http.route(
        ['/shop/cart/update'],
        type='http',
        auth="public",
        methods=['POST'],
        website=True,
        csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))
        request.env.context = dict(request.env.context, custom_options=self._filter_custom_options(**kw))
        return super(WebsiteSaleCustom, self).cart_update(product_id, add_qty, set_qty, **kw)
