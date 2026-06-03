# -*- coding: utf-8 -*-
"""Ed25519 signing for license responses and unlock tokens.

The PRIVATE key lives only on this central server (a 0600 PEM file, path from
``techrise_license.signing_key_path``). Clients embed the matching PUBLIC key
and verify; they can never forge an ``allowed`` verdict or an unlock token, even
pointed at a fake server.
"""
import base64
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

DEFAULT_KEY_PATH = '/etc/techrise/license_ed25519_private.pem'

# Canonical messages — MUST match the client verifier byte-for-byte.
GATE_PREFIX = 'techrise-gate:v1'
UNLOCK_PREFIX = 'techrise-unlock:v1'


def _gate_message(device_uid, allowed, expiry, issued_at):
    return '\n'.join([
        GATE_PREFIX,
        device_uid or '',
        '1' if allowed else '0',
        expiry or '',
        str(issued_at),
    ]).encode('utf-8')


def _unlock_message(device_uid, expires_at):
    return '\n'.join([
        UNLOCK_PREFIX, device_uid or '', str(expires_at),
    ]).encode('utf-8')


class TechriseLicenseSigner(models.AbstractModel):
    _name = 'techrise.license.signer'
    _description = 'Techrise License Signer (Ed25519)'

    @api.model
    def _key_path(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'techrise_license.signing_key_path', DEFAULT_KEY_PATH)

    @api.model
    def _private_key(self):
        from cryptography.hazmat.primitives import serialization
        with open(self._key_path(), 'rb') as fh:
            return serialization.load_pem_private_key(fh.read(), password=None)

    @api.model
    def _sign(self, message_bytes):
        key = self._private_key()
        return base64.b64encode(key.sign(message_bytes)).decode('ascii')

    @api.model
    def gate_signature(self, device_uid, allowed, expiry):
        """Return the signed envelope for a gate decision, or None if the key
        is missing (logged — the endpoint still answers, just unsigned)."""
        issued_at = int(fields.Datetime.now().timestamp())
        try:
            sig = self._sign(_gate_message(device_uid, allowed, expiry, issued_at))
        except Exception as exc:
            _logger.error('License signing unavailable: %s', exc)
            return None
        return {
            'v': 1,
            'device_uid': device_uid,
            'allowed': bool(allowed),
            'expiry': expiry or '',
            'issued_at': issued_at,
            'signature': sig,
        }

    @api.model
    def issue_unlock_token(self, device_uid, days=7):
        """Mint a signed emergency-unlock token bound to ``device_uid``.

        Returns ``"<expires_at_epoch>:<signature_b64>"``. Set it on the client
        as the ``techrise_license.unlock_token`` system parameter.
        """
        expires_at = int(fields.Datetime.now().timestamp()) + days * 86400
        sig = self._sign(_unlock_message(device_uid, expires_at))
        return '%d:%s' % (expires_at, sig)
