# -*- coding: utf-8 -*-
import odoo
from odoo import api, fields, models, _


class CallBackLog(models.Model):
    _name = "call.back.log"
    call_log = fields.Text('Keyword Argument Log')
