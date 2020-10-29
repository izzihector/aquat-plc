from odoo import fields, http, tools, _
from odoo.http import request


class MyController(http.Controller):

    @http.route('/Octave/create', type='http', auth="public", methods=['GET', 'POST'])
    def save_kwargs(self, **kwargs):
        request.env['call.back.log'].sudo().create({'call_log': kwargs})
        return {'success': True, 'msg': 'Log created'}
