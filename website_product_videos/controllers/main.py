# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product/iframe'], type='json', auth="public", website=True)
    def render_frame(self, pvid=None):
        product_video_id = request.env['product.video'].browse(int(pvid))
        if product_video_id:
            return request.env['ir.ui.view'].render_template( "website_product_videos.video_iframe",{
                'pvid': product_video_id
            })
        return {}

    # For demo purpose only
    @http.route(['/demo/videos'], type='http', auth="public", website=True)
    def render_product_page(self):
        video_product_id = request.env.ref('website_product_videos.video_product')
        if video_product_id:
            redirect = '/shop/product/' + '-'.join((video_product_id).name.split(' ')) + '-' + str(video_product_id.id)
            return request.redirect(redirect)
        return request.redirect('/shop')