# Part of odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

import werkzeug.wrappers

from odoo import http
from odoo.addons.restful.common import invalid_response, valid_response
from odoo.http import request

expires_in = "url_controller.access_token_expires_in"


class AccessToken(http.Controller):
    """."""

    @http.route("/get_token", methods=["GET"], type="http", auth="none", csrf=False)
    def token(self, **kwargs):
        headers = request.httprequest.headers
        api_key = headers.get("api_key")
        if not api_key:
            return invalid_response(
                "missing error",
                "API Key is missing",
                403,
            )
        access_user = request.env["res.users"].sudo().search([('api_key', '=', api_key)], limit=1)
        if not access_user:
            error = "API Key Mismatch"
            return invalid_response("Authentication Failed", error, 403)

        access_user.sudo().generate_token()
        access_token = access_user.token
        # Successful response:
        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(
                {
                    "uid": access_user.id,
                    "company_id": access_user.company_id.id if access_user.id else None,
                    "access_token": access_token,
                    "expires_in(minutes)": str(request.env.ref(expires_in).sudo().value),
                }
            ),
        )
