# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmSequence(models.Model):
    _name='mrp.plm.seq'
    _description = "Mrp Plm Sequence"
    sequence = fields.Integer(help="Used to order the note stages", default=1)