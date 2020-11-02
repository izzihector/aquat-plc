from odoo import fields, http, tools, _
from odoo.http import request
import functools
import json
import logging

import werkzeug.wrappers
from odoo.addons.restful.common import (
    extract_arguments,
    invalid_response,
    valid_response,
)


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get("access_token")
        if not access_token:
            return invalid_response(
                "access_token_not_found", "missing access token in request header", 401
            )
        access_token_user_id = request.env["res.users"].sudo().search([("token", "=", access_token)], order="id DESC",
                                                                      limit=1)
        if not access_token_user_id:
            return invalid_response("access_token", "Invalid Access Token", 401)
        if access_token_user_id.sudo().has_expired():
            return invalid_response("access_token", "Token seems to have expired or invalid", 401)
        request.session.uid = access_token_user_id.id
        request.uid = access_token_user_id.id
        return func(self, *args, **kwargs)

    return wrap


class MyController(http.Controller):

    @validate_token
    @http.route('/Octave/create', type='http', auth="public", methods=['GET', 'POST'], csrf=False)
    def save_kwargs(self, **kwargs):
        request.env['call.back.log'].sudo().create({'call_log': kwargs})
        return werkzeug.wrappers.Response(
            status=200,
            response=json.dumps(
                {'success': True, 'msg': 'Log created'}
            ),
        )
