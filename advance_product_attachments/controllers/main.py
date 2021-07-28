# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import http
import base64
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
# from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/download/attachment'], type='json', auth="public", methods=['POST'], website=True)
    def download_attachment(self, pro_attachment_id):
        if pro_attachment_id:
            pro_attachment_id = int(pro_attachment_id)
            irAttachObj = request.env['product.attachment'].sudo().browse(pro_attachment_id)
            irAttachObj.downloads = irAttachObj.downloads + 1
        return True

class Binary(http.Controller):

    @http.route(['/web/content',
    '/web/content/<string:xmlid>',
    '/web/content/<string:xmlid>/<string:filename>',
    '/web/content/<int:id>',
    '/web/content/<int:id>/<string:filename>',
    '/web/content/<int:id>-<string:unique>',
    '/web/content/<int:id>-<string:unique>/<string:filename>',
    '/web/content/<int:id>-<string:unique>/<path:extra>/<string:filename>',
    '/web/content/<string:model>/<int:id>/<string:field>',
    '/web/content/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename=None, filename_field='name', unique=None, mimetype=None,
                       download=None, data=None, token=None, access_token=None, **kw):

        status, headers, content = request.env['ir.http'].sudo().binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype, access_token=access_token)

        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        if token:
            response.set_cookie('fileToken', token)
        return response
