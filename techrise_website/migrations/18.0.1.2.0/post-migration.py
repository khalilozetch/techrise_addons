"""Post-migration for 18.0.1.1.0.

`website_hr_recruitment` creates a public "Jobs" menu item on the navbar.
This release intentionally unpublishes all job records and removes their
pages from the sitemap, so the menu item must go too — otherwise visitors
still see "Jobs" in the header and it 200s to an empty listing page that
Google will try to index again.

`_post_init_hook` only fires on install, not on upgrade, so the cleanup is
repeated here for running deployments.
"""


def migrate(cr, version):
    cr.execute("""
        DELETE FROM website_menu
         WHERE url LIKE '/jobs%%'
    """)
