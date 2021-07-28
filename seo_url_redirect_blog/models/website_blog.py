# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models, _

class Blog(models.Model):
    _inherit = 'blog.blog'

    url_key = fields.Char(
        string='SEO Url Key',
        default='', translate=True,
        help="SEO Url Key for Blog")


    def __check_url_key_uniq(self):
        for obj in self:
            if obj.url_key:
                urlKey = "/" + obj.url_key
                res = self.env['website.rewrite'].sudo().search([('url_to', '=', urlKey), ('rewrite_val', '!=', 'custom')], 0, 2, 'id desc')
                if res:
                    for resObj in res:
                        if resObj.record_id == obj.id:
                            if resObj.rewrite_val != "blog.blog":
                                return False
                        else:
                            return False
        return True

    _constraints = [(__check_url_key_uniq, 'SEO URL Key must be unique!', ['url_key'])]

    @api.model
    def create(self, vals):
        res = super(Blog, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_blog', res)
        return res


    def write(self, vals):
        for blogObj in self:
            vals = self.env['website.rewrite'].createRedirectForRewrite(vals, blogObj, 'blog.blog', 'pattern_blog')
        res = super(Blog, self).write(vals)
        return res

    def update_seo_url(self):
        blogIds = self._context.get('active_ids')
        blogObjs = self.search([('id', 'in', blogIds)])
        self.env['website.rewrite'].setSeoUrlKey('pattern_blog', blogObjs)
        text = "SEO Url key of {} blog(s) have been successfully updated.".format(len(blogObjs))
        return self.env['wk.wizard.message'].genrated_message(text)

class BlogPost(models.Model):
    _inherit = 'blog.post'

    url_key = fields.Char(
        string='SEO Url Key',
        default='', translate=True,
        help="SEO Url Key for Blog Post")

    def __check_url_key_uniq(self):
        for obj in self:
            if obj.url_key:
                urlKey = "/" + obj.url_key
                res = self.env['website.rewrite'].sudo().search([('url_to', '=', urlKey), ('rewrite_val', '!=', 'custom')], 0, 2, 'id desc')
                if res:
                    for resObj in res:
                        if resObj.record_id == obj.id:
                            if resObj.rewrite_val != "blog.post":
                                return False
                        else:
                            return False
        return True


    _constraints = [(__check_url_key_uniq, 'SEO URL Key must be unique!', ['url_key'])]

    @api.model
    def create(self, vals):
        res = super(BlogPost, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_post', res)
        return res

    def write(self, vals):
        for blogPostObj in self:
            vals = self.env['website.rewrite'].createRedirectForRewrite(vals, blogPostObj, 'blog.post', 'pattern_post')
        res = super(BlogPost, self).write(vals)
        return res

    def update_seo_url(self):
        blogPostIds = self._context.get('active_ids')
        blogPostObjs = self.search([('id', 'in', blogPostIds)])
        self.env['website.rewrite'].setSeoUrlKey('pattern_post', blogPostObjs)
        text = "SEO Url key of {} blog post(s) have been successfully updated.".format(len(blogPostObjs))
        return self.env['wk.wizard.message'].genrated_message(text)
