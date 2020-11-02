import hashlib
import os
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import string
import random
expires_in = "url_controller.access_token_expires_in"


def nonce(length=40, prefix=""):
    rbytes = os.urandom(length)
    return "{}_{}".format(prefix, str(hashlib.sha1(rbytes).hexdigest()))


def api_key(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


class Users(models.Model):
    _inherit = "res.users"

    token = fields.Char("Access Token")
    api_key = fields.Char("API Key")
    expires = fields.Datetime("Expires")

    def generate_api_key(self):
        key = api_key()
        self.write({
            'api_key': key,
        })
        return True

    def generate_token(self):
        token = nonce()
        expires = datetime.now() + timedelta(
            minutes=int(self.env.ref(expires_in).sudo().value)
        )
        self.write({
            'token': token,
            'expires': expires.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        })
        return True

    @api.multi
    def has_expired(self):
        self.ensure_one()
        return datetime.now() > fields.Datetime.from_string(self.expires)
