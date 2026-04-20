from odoo import models


# URLs intentionally excluded from the public sitemap.
# - /contact     : 301 alias of canonical /contactus
# - /jobs*       : career pages are intentionally unpublished
# - /website/info: Odoo introspection page, not meant for public SEO
_SITEMAP_EXCLUDED_PREFIXES = ('/contact', '/jobs', '/website/info')
_SITEMAP_EXCLUDED_EXACT = {'/contact'}


class Website(models.Model):
    _inherit = 'website'

    def _enumerate_pages(self, query_string=None, force=False):
        """Filter out duplicate/unwanted URLs from the sitemap."""
        seen = set()
        for page in super()._enumerate_pages(query_string=query_string, force=force):
            url = (page.get('loc') or '').rstrip('/') or '/'
            if url in _SITEMAP_EXCLUDED_EXACT:
                continue
            if any(url == p or url.startswith(p + '/') for p in _SITEMAP_EXCLUDED_PREFIXES):
                continue
            if url in seen:
                continue
            seen.add(url)
            yield page