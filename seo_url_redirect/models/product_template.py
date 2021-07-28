# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    url_key = fields.Char(
        string='SEO Url Key',
        default='', translate=True,
        help="SEO Url Key for Product")

    def __check_url_key_uniq(self):
        for obj in self:
            if obj.url_key:
                urlKey = "/" + obj.url_key
                res = self.env['website.rewrite'].sudo().search([('url_to', '=', urlKey), ('rewrite_val', '!=', 'custom')], 0, 2, 'id desc')
                if res:
                    for resObj in res:
                        if resObj.record_id == obj.id:
                            if resObj.rewrite_val != "product.template":
                                return False
                        else:
                            return False
        return True

    _constraints = [(__check_url_key_uniq, 'SEO URL Key must be unique!', ['url_key'])]

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_product', res)
        return res

    def write(self, vals):
        for proObj in self:
            if vals.get('url_key'):
                vals = self.env['website.rewrite'].createRedirectForRewrite(vals, proObj, 'product.template', 'pattern_category')
        res = super(ProductTemplate, self).write(vals)
        return res

    def update_seo_url(self):
        productIds = self._context.get('active_ids')
        productObjs = self.search([('id', 'in', productIds)])
        resp = self.env['website.rewrite'].setSeoUrlKey('pattern_product', productObjs)
        text = "SEO Url key of {} product(s) have been successfully updated.".format(len(productObjs))
        if resp:
            failedIds = ", ".join(resp)
            updatedProducts = len(productObjs) - len(resp)
            text = "Products with internal reference [{}] are failed to update. Reason : SEO URL Key must be unique!".format(failedIds)
            if updatedProducts:
                text = "SEO Url key of {} product(s) have been successfully updated and products with internal reference [{}] are failed to update. Reason : SEO URL Key must be unique!".format(updatedProducts, failedIds)
        return self.env['wk.wizard.message'].genrated_message(text)


    def open_website_url(self):
        res = super(ProductTemplate, self).open_website_url()
        website_id = self.env["website"].get_current_website()

        if website_id.use_server_rewrites and res.get("url"):
            url = self.url_key
            if website_id.use_suffix:
                url += website_id.suffix_product
            res.update({"url": url})
        return res
