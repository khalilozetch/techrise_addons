from . import controllers


def _post_init_hook(env):
    """Fix menu parent IDs to point to the website-specific top menu."""
    website = env.ref('website.default_website', raise_if_not_found=False)
    if not website:
        return
    top_menu = env['website.menu'].search([
        ('website_id', '=', website.id),
        ('parent_id', '=', False),
    ], limit=1)
    if not top_menu:
        return
    menu_xmlids = [
        'techrise_website.menu_home',
        'techrise_website.menu_about',
        'techrise_website.menu_services',
        'techrise_website.menu_server',
        'techrise_website.menu_contact',
    ]
    for xmlid in menu_xmlids:
        menu = env.ref(xmlid, raise_if_not_found=False)
        if menu and menu.parent_id != top_menu:
            menu.parent_id = top_menu
    # Remove duplicate default menus
    default_home = env['website.menu'].search([
        ('url', '=', '/'),
        ('parent_id', '=', top_menu.id),
        ('id', 'not in', [env.ref(x, raise_if_not_found=False).id for x in menu_xmlids if env.ref(x, raise_if_not_found=False)]),
    ])
    default_contact = env['website.menu'].search([
        ('url', '=', '/contactus'),
        ('parent_id', '=', top_menu.id),
        ('id', 'not in', [env.ref(x, raise_if_not_found=False).id for x in menu_xmlids if env.ref(x, raise_if_not_found=False)]),
    ])
    (default_home | default_contact).unlink()
