# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmTag(models.Model):
    _name='mrp.plm.tag'
    _description='Mrp Plm Tag'
    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')
    
    # display_name=fields.Char(readonly=True,help="Nom affiché")
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]