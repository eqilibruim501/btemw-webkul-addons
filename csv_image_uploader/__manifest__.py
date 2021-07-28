# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################
{
  "name"                 :  "CSV Image Uploader",
  "summary"              :  "The module helps to import images for Product Variants, Product Extra Images, and Website Product Categories through a CSV file",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-CSV-Image-Uploader.html",
  "description"          :  """import product image
CSV file import
import image with CSV file
import product image with CSV file
Add product image
add product extra image
import product extra images
import variants image with CSV
use product image from CSV
allow CSV import
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=csv_image_uploader",
  "depends"              :  [
                             'sale_management',
                             'website_sale',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/import_csv_view.xml',
                             'views/csv_sequence.xml',
                             'data/demo_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}