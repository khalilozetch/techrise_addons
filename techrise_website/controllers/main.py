from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


SERVICE_LABELS = {
    'erp': 'ERP System Design (Odoo)',
    'website': 'Website Design & Development',
    'mobile': 'Mobile App Development',
    'integration': 'System Integration',
    'accounting': 'Accounting & Tax Services',
    'branding': 'Branding & Marketing',
    'hosting': 'Server & Hosting',
    'support': 'Technical Support',
    'other': 'Other',
}


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

    @http.route('/contactus', type='http', auth='public', website=True, sitemap=True)
    def contact_page(self, **kwargs):
        return request.render('techrise_website.contact_page')

    @http.route('/contact', type='http', auth='public', website=True, sitemap=False)
    def contact_alias(self, **kwargs):
        # Canonical URL is /contactus; 301 kills the duplicate-content signal in GSC.
        return redirect('/contactus', code=301)

    @http.route('/contact/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def contact_submit(self, **kwargs):
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email_from', '').strip()
        phone = kwargs.get('phone', '').strip()
        company = kwargs.get('company', '').strip()
        service_key = kwargs.get('service', '').strip()
        message = kwargs.get('body', '').strip()

        service_label = SERVICE_LABELS.get(service_key, service_key)

        lead_name = f"Website Contact: {name}"
        if service_label:
            lead_name = f"{service_label} - {name}"

        description = message
        if service_label:
            description = f"Service Interested In: {service_label}\n\n{message}"

        vals = {
            'name': lead_name,
            'contact_name': name,
            'email_from': email,
            'phone': phone,
            'partner_name': company or False,
            'description': description,
            'type': 'lead',
        }

        request.env['crm.lead'].sudo().create(vals)

        return request.render('techrise_website.contact_thankyou')

    @http.route('/privacy-policy', type='http', auth='public', website=True, sitemap=True)
    def privacy_policy_page(self, **kwargs):
        return request.render('techrise_website.privacy_policy_page')

    @http.route('/terms-and-conditions', type='http', auth='public', website=True, sitemap=True)
    def terms_and_conditions_page(self, **kwargs):
        return request.render('techrise_website.terms_and_conditions_page')

    # ================================================================
    # Industry landing pages (Google Ads + SEO targeted)
    # ================================================================
    @http.route('/erp-for-construction-uae', type='http', auth='public', website=True, sitemap=True)
    def erp_construction_page(self, **kwargs):
        return request.render('techrise_website.erp_construction_page')

    @http.route('/erp-for-healthcare-uae', type='http', auth='public', website=True, sitemap=True)
    def erp_healthcare_page(self, **kwargs):
        return request.render('techrise_website.erp_healthcare_page')

    @http.route('/erp-for-retail-uae', type='http', auth='public', website=True, sitemap=True)
    def erp_retail_page(self, **kwargs):
        return request.render('techrise_website.erp_retail_page')
