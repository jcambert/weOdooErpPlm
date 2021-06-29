# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .models import Model,INNER_MODELS
class PlmStage(Model):
    _name=INNER_MODELS['stage']
    _description='Mrp Plm Stage'
    _order= "sequence, id"
    allow_apply_change=fields.Boolean(string="Autoriser l'application de changements" )
    approval_roles=fields.Char("Rôles de validation",compute='_compute_approval_roles')
    approval_template_ids=fields.One2many(INNER_MODELS['approval_tmpl'],'stage_id',string="Validations")
    final_stage=fields.Boolean(string="Etape finale",compute='_compute_is_final_stage',readonly=True)
    effective_stage = fields.Boolean("Effective")
    reject_stage = fields.Boolean("Rejected")
    fold=fields.Boolean(string="Replié en vue kanban")
    is_blocking=fields.Boolean(readonly=True,string="Etape de blocage")
    name=fields.Char(required=True, translate=True,string="Nom")
    sequence=fields.Integer(string="Séquence")
    type_id=fields.Many2one(INNER_MODELS['type'],'Type',required=True,ondelete='restrict')
    is_closed = fields.Boolean('Closing Stage', help="Tasks in this stage are considered as closed.")

    def _default_sequence(self):
        stage = self.search([], limit=1, order="sequence DESC")
        return stage.sequence or 0


    @api.depends('effective_stage','reject_stage')
    def _compute_is_final_stage(self):
        for record in self:
            record.final_stage=record.effective_stage or record.reject_stage

    def _compute_approval_roles(self):
        for record in self:
            roles=[]
            for r in record.approval_template_ids:
                for role in r.roles:
                    roles.append(role.name)
            record.approval_roles=','.join(roles)