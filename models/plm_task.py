
from odoo import models, fields, api,SUPERUSER_ID
from .models import Model,INNER_MODELS
DEFAULT_PLM_ID='default_plm_id'
class PlmTask(Model):
    """
    No need to work according to company
    """
    _name = INNER_MODELS['task']
    _description = "PLM Task"
    _date_name = "date_assign"
    _inherit = [ 'mail.thread.cc', 'mail.activity.mixin','archive.mixin','sequence.mixin','color.mixin']
    _mail_post_access = 'read'
    _order = "priority desc, sequence, id desc"
    
    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get(DEFAULT_PLM_ID)
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False), ('is_closed', '=', False)])
    

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if DEFAULT_PLM_ID in self.env.context:
            search_domain = ['|', ('plm_ids', '=', self.env.context[DEFAULT_PLM_ID])] + search_domain

        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    name = fields.Char(string='Title', tracking=True, required=True, index=True)
    note=fields.Text(string='Internal Notes')
    product_tmpl_id = fields.Many2one(INNER_MODELS['product_tmpl'], 'Product',auto_join=True, ondelete="set null")

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True, string="Priority")
    stage_id = fields.Many2one(INNER_MODELS[ 'type'], string='Stage', compute='_compute_stage_id',
        store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        domain="[('plm_ids', '=', plm_id)]", copy=False)
    tag_ids = fields.Many2many(INNER_MODELS['tag'], string='Tags')
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Kanban State',
        copy=False, default='normal', required=True)
    kanban_state_label = fields.Char(compute='_compute_kanban_state_label', string='Kanban State Label', tracking=True)
    
    plm_id = fields.Many2one(INNER_MODELS['plm'] , string='PLM',
        store=True, readonly=False,
        index=True, tracking=True, check_company=True, change_default=True)
    legend_blocked = fields.Char(related='stage_id.legend_blocked', string='Kanban Blocked Explanation', readonly=True, related_sudo=False)
    legend_done = fields.Char(related='stage_id.legend_done', string='Kanban Valid Explanation', readonly=True, related_sudo=False)
    legend_normal = fields.Char(related='stage_id.legend_normal', string='Kanban Ongoing Explanation', readonly=True, related_sudo=False)
    is_closed = fields.Boolean(related="stage_id.is_closed", string="Closing Stage", readonly=True, related_sudo=False)
    # is_closed = fields.Boolean( string="Closing Stage")

    #TODO ADD TASK FIELDS FROM mrp.plm
    allow_apply_change=fields.Boolean("Afficher les modifications appliquées",compute='_compute_allow_apply_change')
    allow_change_stage=fields.Boolean(compute='_compute_allow_change_state', string="Autoriser le changement d'étape")
    approval_ids=fields.One2many(INNER_MODELS['approval'],'eco_id',help="Validations")
    has_approval = fields.Integer('Has approval',readonly=True,compute='_compute_has_approval')
    effectivity=fields.Selection([('asap','Asap'),('date','to date')],'Date effective',help="Entrée en vigueur",default='asap')
    effectivity_date=fields.Date(string="Date d'entrée en vigueur")
    state=fields.Selection(
        [('draft','Draft'),('confirmed','Confirmed'),('done','Done'),('rejected','Rejected')],
        string='State',
        default='draft',
        copy=False,required=True,help="Statut",tracking=True,store=True
        )

    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'normal':
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'blocked':
                task.kanban_state_label = task.legend_blocked
            else:
                task.kanban_state_label = task.legend_done

    @api.depends('plm_id')
    def _compute_stage_id(self):
        for task in self:
            if task.plm_id:
                if task.plm_id not in task.stage_id.plm_ids:
                    task.stage_id = task.stage_find(task.plm_id.id, [
                        ('fold', '=', False), ('is_closed', '=', False)])
            else:
                task.stage_id = False


    def _compute_allow_apply_change(self):
        for record in self:
            record.allow_apply_change=True
 
    @api.depends('state')
    def _compute_can_start_revision(self):
        for record in self:
            # record.allow_start_revision=
            record.can_start_revision = (record.state=='draft' and record.create_date!=False)

    @api.depends('state')
    def _compute_allow_change_state(self):
        for record in self:
            record.allow_change_stage= record.state not in ['draft','done','rejected']

    @api.depends('approval_ids')
    def _compute_has_approval(self):
        for record in self:
            record.has_approval = len(record.approval_ids.ids)>0

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
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('plm_ids', '=', section_id))
        search_domain += list(domain)
        # perform search, return the first found
        return self._type.search(search_domain, order=order, limit=1).id