# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .models import Model
from random import randint

class PlmTag(Model):
    _name='mrp.plm.tag'
    _description='Mrp Plm Tag'

    def _get_default_color(self):
        return randint(1, 11)
    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index', default=_get_default_color)
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]