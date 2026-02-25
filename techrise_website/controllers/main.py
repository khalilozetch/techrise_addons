from odoo import http
from odoo.http import request


class TechriseWebsite(http.Controller):

    @http.route('/about', type='http', auth='public', website=True, sitemap=True)
    def about_page(self, **kwargs):
        return request.render('techrise_website.about_page')

    @http.route('/services', type='http', auth='public', website=True, sitemap=True)
    def services_page(self, **kwargs):
        return request.render('techrise_website.services_page')

    @http.route('/server', type='http', auth='public', website=True, sitemap=True)
    def server_page(self, **kwargs):
        return request.render('techrise_website.server_page')

    @http.route(['/contact', '/contactus'], type='http', auth='public', website=True, sitemap=True)
    def contact_page(self, **kwargs):
        return request.render('techrise_website.contact_page')
