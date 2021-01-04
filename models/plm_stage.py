# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmStage(models.Model):
    _name='mrp.plm.stage'
    _description='Mrp Plm Stage'
    allow_apply_change=fields.Boolean(string="Autoriser l'application de changements" )
    approval_roles=fields.Char(readonly =True,string="Rôles de validation")
    approval_template_ids=fields.One2many('mrp.plm.approval.template','stage_id',string="Validations")
    display_name=fields.Char(readonly=True,string="Nom affiché")
    final_stage=fields.Boolean(string="Etape finale")
    folded=fields.Boolean(string="Replié en vue kanban")
    is_blocking=fields.Boolean(readonly=True,string="Etape de blocage")
    name=fields.Char(required=True, translate=True,string="Nom")
    sequence=fields.Integer(string="Séquence")
    type_id=fields.Many2one('mrp.plm.type','Type',required=True,ondelete='restrict')