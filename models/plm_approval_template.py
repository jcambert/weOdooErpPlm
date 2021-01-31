# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PlmApprovalTemplate(models.Model):
    _name="mrp.plm.approval.template"
    _description="Mrp Plm Validation Template"
    _inherit=['mrp.plm.seq']
    approval_type=fields.Selection([
        ('selection','Selection'),
        ('mandatory','Mandatory'),
        ('comment','Comment')],required=True,string="Type de validation")
    display_name=fields.Char(readonly=True,string="Nom affiché")
    
    roles=fields.Many2one('res.users.role',string="Roles")
    stage_id=fields.Many2one('mrp.plm.stage',ondelete='restrict',string="Etape")
    