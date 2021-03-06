# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging
import ast
import os

from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)


class wk_import_csv(models.Model):
    _inherit = "wk.import.csv"

    @api.model
    def _get_csv_import_model(self):
        csv_model = super(wk_import_csv, self)._get_csv_import_model()
        csv_model.append(['product.public.category', 'Website Category image'])
        return csv_model

    @api.model
    def get_attachment(self):
        if self.csv_model == "product.public.category":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference(
                    'csv_image_uploader', 'sample_product_category_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        else:
            return super(wk_import_csv, self).get_attachment()

    @api.model
    def get_attachment_id(self, vals):
        if vals.get('csv_model') and vals.get(
                'csv_model') == "product.public.category":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference(
                    'csv_image_uploader', 'sample_product_category_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        return super(wk_import_csv, self).get_attachment_id(vals)

    @api.model
    def product_public_category_validate_values(self, values):
        res = {'status': False, 'msg': 'Website Category Id Not Found'}
        if values.get('id'):
            if 'image_status' in values:
                res['msg'] = values.get('image_status')
                values.pop('image_status')
            else:
                record_obj = self.env['ir.model.data'].xmlid_to_object(
                    values.get('id'))
                try:
                    category_id = values.pop('id')
                    if not values.get('name'):
                        values.pop('name')
                    record_obj.write(values)
                    res['status'] = True
                    res['msg'] = category_id + ' updated successfully.'
                except Exception as e:
                    _logger.info('=======%r', e)
                    res['msg'] = e
        else:
            res['msg'] = "Website Category Id Not Found in CSV "
        return res

    def product_public_category_import_csv(self):
        for current_record in self:
            current_record.import_function()
        return True
