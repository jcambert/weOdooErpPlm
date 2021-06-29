    # -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _, SUPERUSER_ID
from .models import INNER_MODELS, Model
DEFAULT_PLM_ID = 'default_plm_id'


class Plm(Model):
    _name = INNER_MODELS['plm']
    _description = 'Product Lifecycle'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'archive.mixin',
                'sequence.mixin', 'company.mixin', 'color.mixin']
    _order = "sequence, name, id"
    _check_company_auto = True

    name = fields.Char("Name", index=True, required=True, tracking=True)
    description = fields.Html(string='Description')
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              default=lambda self: self.env.uid,
                              index=True, tracking=True)
    type_id = fields.Many2one(INNER_MODELS['type'],  string='Types Of Lifecycle')
    stage_ids = fields.One2many(INNER_MODELS['stage'],'plm_id',string='Stages',domain=[('fold', '=', False)])
    def action_view_tasks(self):
        action = self.with_context(active_id=self.id, active_ids=self.ids) \
            .env.ref('weOdooErpPlm.open_mrp_plm_2_mrp_plm_stage_all') \
            .sudo().read()[0]
        action['display_name'] = self.name
        return action
    @api.model
    def create(self,vals):
        plm = super(Plm, self).create(vals)
        t=plm[0]
        for tmpl in t.type_id.stage_type_ids:
            stage=tmpl.copy2stage(plm.id)
            print(stage.name)
            
        return plm

class PlmType(Model):
    """
    Type of Plm
    -New Product
    -Modification Request
    -Indice Request
    """
    _name = INNER_MODELS['type']
    _description = 'Product Lifecycle Type'
    _inherit = ['sequence.mixin', 'archive.mixin', 'color.mixin']
    _order = "sequence,id"

    name = fields.Char(string='Title', required=True, index=True)
    description = fields.Char(string='Description')
    plm_ids = fields.One2many(INNER_MODELS['plm'], 'type_id' ,string='Lifecycle')
    stage_type_ids=fields.Many2many(INNER_MODELS['stage_template'],'type_stage_type_rel','type_id','stage_type_id',string='Stage Types')

class PlmStageTemplate(Model):
    """
    -New
    -Running
    -Validated
    -Rejected
    """
    _name = INNER_MODELS['stage_template']
    _description = 'Lifecycle stage type'
    _inherit = ['sequence.mixin', 'archive.mixin']
    _order = 'sequence, id'
    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Ready'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    closing = fields.Boolean(
        'Closing Stage', help="Tasks in this stage are considered as closed.")

    type_ids=fields.Many2many(INNER_MODELS['type'],'type_stage_type_rel','stage_type_id','type_id',string='Plm Types')

    is_template=fields.Boolean(compute='_compute_is_template')

    plm_id = fields.Many2one(INNER_MODELS['plm'], string='LifecycleProject',
                             store=True, readonly=False, index=True, tracking=True, check_company=True, change_default=True)
                             
    def _compute_is_template(self):
        self.is_template=True
    
    @api.returns('mrp.plm.stage')
    def copy2stage(self,plm_id):
        self.ensure_one()
        res=self.env['mrp.plm.stage'].create({'stage_tmpl_id':self.id,
                                        'name':self.name,
                                        'plm_id':plm_id
                                        })
        return res
class PlmStage(Model):
    """
    Concrete Stage inherited from mrp.plm.stage.template
    add some logic to plm stage managment
    """
    _name = INNER_MODELS['stage']
    _description = 'Product Lifecycle stage'
    _inherits = {INNER_MODELS['stage_template']: 'stage_tmpl_id'}
    _inherit = ['mail.activity.mixin', 'mail.thread', 'archive.mixin', 'sequence.mixin', 'company.mixin', 'color.mixin', 'kanban.mixin']
    _order = "priority desc, sequence, id desc"
    _check_company_auto = True

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        plm_id = self.env.context.get(DEFAULT_PLM_ID)
        if not plm_id:
            return False
        return self.stage_find(plm_id, [('fold', '=', False), ('closing', '=', False)])

    
    name = fields.Char(string='Title', tracking=True,
                       required=True, index=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True, string="Priority")

    plm_id = fields.Many2one(INNER_MODELS['plm'], string='LifecycleProject',
                             store=True, readonly=False, index=True, tracking=True, check_company=True, change_default=True)

    stage_tmpl_id = fields.Many2one(INNER_MODELS['stage_template'], string='Stage', compute='_compute_stage_id',
                               store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
                               default=_get_default_stage_id, group_expand='_read_group_stage_ids', copy=False,required=True)

    user_id = fields.Many2one('res.users',
                              string='Created by',
                              default=lambda self: self.env.uid,
                              index=True, tracking=True)
    is_template=fields.Boolean(compute='_compute_is_template')

    is_closed=fields.Boolean('Is Closed')

    def _compute_is_template(self):
        self.is_template=True

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)] + domain
        # if DEFAULT_PLM_ID in self.env.context:
        #     search_domain = ['|', ('project_ids', '=', self.env.context[DEFAULT_PLM_ID])] + search_domain

        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.depends('plm_id')
    def _compute_stage_id(self):
        for stage in self:
            if stage.plm_id:
                stage.stage_id = stage.stage_find(
                    stage.plm_id.id, [('fold', '=', False), ('closing', '=', False)])
            else:
                stage.stage_id = False

    def stage_find(self, section_id, domain=[], order='sequence'):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        # collect all section_ids
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('plm_id').ids)
        search_domain = []

        search_domain += list(domain)
        # perform search, return the first found
        return self._stage_type.search(search_domain, order=order, limit=1).id



