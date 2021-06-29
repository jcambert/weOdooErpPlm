# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .models import Model,INNER_MODELS
class PlmApprovalTemplate(Model):
    _name=INNER_MODELS['approval_tmpl']
    _description="Mrp Plm Validation Template"
    _inherit=['sequence.mixin']
    approval_type=fields.Selection([
        ('selection','Selection'),
        ('mandatory','Mandatory'),
        ('comment','Comment')],required=True,string="Type de validation")
    display_name=fields.Char(readonly=True,string="Nom affiché")
    
    roles=fields.Many2one('res.users.role',string="Roles")
    stage_id=fields.Many2one(INNER_MODELS['stage'],ondelete='restrict',string="Etape")
    