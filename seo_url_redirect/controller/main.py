import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.seo_url_redirect.models.ir_http import slug
from odoo.http import route, request

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        
        result = super(WebsiteSale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        qcontext = result.qcontext
        url = "/shop"

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if category:
                url = "/shop/category/%s" % slug(category)

        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        if qcontext.get("search_count"):
            pager = request.website.pager(url=url, total=qcontext.get("search_count"), page=page, step=ppg, scope=7, url_args=post)
            result.qcontext.update(pager=pager)

        return result
