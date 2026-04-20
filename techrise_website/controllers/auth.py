"""Harden /web/reset_password against email enumeration (OWASP WSTG-ATHN-03).

Stock Odoo responds differently for existing vs. non-existing logins on the
reset-password form ("Password reset instructions sent" vs. "No account found
for this login"). An attacker can use that signal to enumerate valid accounts.

We override the controller to always return the same generic message whenever
a login has been submitted, regardless of whether the account exists. The
exception raised by ``res.users.reset_password`` for unknown accounts is
absorbed so the public response is identical in both cases.

No template or rendered asset is changed, so PageSpeed scores are unaffected.
"""

import logging

import werkzeug

from odoo import _, http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request


_logger = logging.getLogger(__name__)

# Single, non-revealing response used for both success and "account not found".
_GENERIC_RESET_MESSAGE = "If an account exists for this email, password reset instructions have been sent."
_ACCOUNT_NOT_FOUND_FRAGMENT = "No account found"


class TechriseAuthSignup(AuthSignupHome):

    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if not request.env['ir.http']._verify_request_recaptcha_token('password_reset'):
                    raise UserError(_("Suspicious activity detected by Google reCaptcha."))
                if qcontext.get('token'):
                    # Token flow: user clicked the reset link — behave exactly like stock.
                    self.do_signup(qcontext)
                    return self.web_login(*args, **kw)

                login = qcontext.get('login')
                if not login:
                    qcontext['error'] = _("No login provided.")
                else:
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr,
                    )
                    try:
                        request.env['res.users'].sudo().reset_password(login)
                    except Exception as e:
                        # Swallow "account not found" so the response does not
                        # reveal whether the email is registered. Any other
                        # failure (mailer down, etc.) is still surfaced below.
                        if _ACCOUNT_NOT_FOUND_FRAGMENT not in str(e):
                            raise
                    qcontext['message'] = _(_GENERIC_RESET_MESSAGE)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:  # noqa: BLE001 — mirror stock behaviour
                qcontext['error'] = str(e)

        elif 'signup_email' in qcontext:
            # Identical fallback to stock: redirect known signup_email to /web/login.
            return super().web_auth_reset_password(*args, **kw)

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response