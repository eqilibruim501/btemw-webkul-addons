# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models, _
from odoo.http import request
import werkzeug
import logging

_log = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        if not hasattr(request, "jsonrequest") and not hasattr(request, 'rerouting'):
            req_page = request.httprequest.path
            if "/web/database/" in req_page:
                return super(IrHttp, cls)._dispatch()
            redirectObj = request.env['website.rewrite'].sudo()
            if '/web/image' not in req_page and '/web/content' not in req_page:
                try:
                    redirect = cls._serve_url_redirect(req_page, redirectObj)
                    if redirect:
                        suffix = redirectObj.getSuffix(redirect.rewrite_val)
                        url_to = redirect.url_to
                        if suffix:
                            url_to = "{}{}".format(url_to, suffix)
                        return werkzeug.utils.redirect(url_to, redirect.type)
                    else:
                        website_id = request.env['website'].get_current_website()
                        if '/blog/' not in req_page and '/post/' not in req_page and not '/tag/' in req_page:
                            useServerRewrites = website_id.use_server_rewrites
                            if useServerRewrites:
                                redirect = cls._serve_url_to_redirect(req_page, redirectObj)
                                page = ''
                                if 'page' in req_page:
                                    actualUrl = req_page
                                    page = "/".join(req_page.split('/')[-2:])
                                    req_page = "/".join(req_page.split("page")[:-1])[:-1]
                                if redirect:
                                    rewrite_val = redirect.rewrite_val
                                    frontEndLang = request.httprequest.cookies.get('frontend_lang')
                                    defaultLang = ""
                                    defaultLangObj = request.env['ir.http']._get_default_lang()
                                    if defaultLangObj:
                                        defaultLang = defaultLangObj.code
                                    if rewrite_val == 'blog.blog':
                                        urlKey = '/'.join(req_page.split('/')[-1:])
                                        if frontEndLang != defaultLang:
                                            redirectUrl = "/{}/blog/{}".format(frontEndLang, urlKey)
                                        else:
                                            redirectUrl = "/blog/" + urlKey
                                        return cls.reroute(redirectUrl)
                                    if rewrite_val == 'blog.post':
                                        record_id = redirect.record_id
                                        urlKey = '/'.join(req_page.split('/')[-1:])
                                        urlKey = request.env['website.rewrite'].unsetUrlSuffix(urlKey)
                                        postObj = request.env['blog.post'].sudo().search([('url_key', '=', urlKey)])
                                        if postObj:
                                            blogUrlKey = postObj.blog_id.url_key
                                            if frontEndLang != defaultLang:
                                                redirectUrl = "/{}/blog/{}/post/{}".format(frontEndLang, blogUrlKey, urlKey)
                                            else:
                                                redirectUrl = "/blog/{}/post/{}".format(blogUrlKey, urlKey)
                                            return cls.reroute(redirectUrl)
                        if '/tag/' in req_page and website_id.use_server_rewrites:
                            defaultLang = ""
                            defaultLangObj = request.env['ir.http']._get_default_lang()
                            frontEndLang = request.httprequest.cookies.get('frontend_lang')
                            if defaultLangObj:
                                defaultLang = defaultLangObj.code
                            url = req_page[req_page.find('/tag/'):]
                            if url:
                                if frontEndLang != defaultLang:
                                    url = "/{}/blog/{}".format(frontEndLang, url)
                                else:
                                    url = "/blog{}".format(url)
                                return cls.reroute(url)
                except Exception as e:
                    pass
        res = super(IrHttp, cls)._dispatch()
        try:
            if res:
                resData = res.get_data()
                if b"href='/blog/" in resData or b"href='/post/" in resData or b'href="/blog/' in resData or b'href="/post/' in resData:
                    currentPage = request.httprequest.environ.get('PATH_INFO')
                    currentPage = currentPage.replace("/blog/", "/").replace("/post/", "/")
                    redirectObj = request.env['website.rewrite'].sudo().get_parent_category(currentPage)
                    use_server_rewrites = redirectObj.get('use_server_rewrites')
                    lang = redirectObj.get('lang')
                    dataString = resData.decode("utf-8")
                    if lang:
                        replaceLangBlogUrl = "/{}/blog/".format(lang)
                        replaceLangCatUrl = "/{}/post/".format(lang)
                        dataString = dataString.replace(replaceLangBlogUrl, "/blog/").replace(replaceLangCatUrl, "/post/")
                    if use_server_rewrites:
                        dataString = dataString.replace("/blog/", "/").replace("/post/", "/")
                    res.set_data(dataString.encode("utf-8"))
        except Exception as e:
            pass
        return res
