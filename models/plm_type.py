
# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api,_
from .models import Model,INNER_MODELS
from .plm_task import DEFAULT_PLM_ID
class PlmType(Model):
    _name=INNER_MODELS['type'] 
    _description = "Mrp Plm Task Stage"
    _inherit=['sequence.mixin','archive.mixin']
    _order="sequence,id"

    def _get_default_plm_ids(self):
        default_project_id = self.env.context.get(DEFAULT_PLM_ID)
        return [default_project_id] if default_project_id else None

    name = fields.Char(string='Stage Name', required=True)
    description = fields.Text('Description')
    plm_ids = fields.Many2many(INNER_MODELS['plm'], 'project_task_type_rel', 'type_id', 'plm_id', string='Projects',
        default=_get_default_plm_ids)
    nb_approvals=fields.Integer(readonly=True,string="En attente de validation",compute='_compute_nb_approvals')
    nb_approvals_my=fields.Integer(readonly=True,string="En attente de ma validation",compute='_compute_nb_approvals_my')
    nb_ecos=fields.Integer(readonly=True,compute='_compute_nb_ecos')
    nb_validation=fields.Integer(readonly=True,string="À appliquer",compute='_compute_nb_validation')
    stage_ids=fields.One2many(INNER_MODELS['stage'],'type_id',string="Etapes")
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Ready'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    tag_ids = fields.Many2many(INNER_MODELS['tag'] , 'mrp_plm_tags_rel', 'plm_id', 'tag_id', string='Tags')
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    is_closed = fields.Boolean('Closing Stage', help="Tasks in this stage are considered as closed.")
    
    def _compute_nb_approvals_my(self):
        for record in self:
            record.nb_approvals_my=1
    def _compute_nb_ecos(self):
        for record in self:
            count=self.env['mrp.plm'].search_count([('active','=',True),('type_id','=',record.id)])
            record.nb_ecos=count
    def _compute_nb_approvals(self):
        for record in self:
            record.nb_approvals=3
    def _compute_nb_validation(self):
        for record in self:
            record.nb_validation=4
    def action_engineering_change(self):
        pass
    def action_my_validation(self):
        pass
    def action_all_validations(self):
        pass
    def action_to_apply(self):
        pass