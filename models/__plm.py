# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _, SUPERUSER_ID
from .models import INNER_MODELS, Model
DEFAULT_ECO_ID = 'default_eco_id'
DEFAULT_TYPE_ID='default_type_id'
class EcoRoutingChange(Model):
    _name=INNER_MODELS['eco.routing.change']
    _description='ECO Routing Change'
    change_type=fields.Selection([('add','Add'),('remove','Remove'),('update','Update')],required=True)
    eco_id=fields.Many2one(INNER_MODELS['eco'],string='OMT Modification',ondelete='cascade')
    new_time_cycle_manual=fields.Float('New manual time')
    old_time_cycle_manual=fields.Float('Old manual time')
    upd_time_cycle_manual=fields.Float('Update manual time')
    workcenter_id=fields.Many2one(INNER_MODELS['mrp.workcenter'],string='Workcenter')

class EcoBomChange(Model):
    _name=INNER_MODELS['eco.bom.change']
    _description='Eco Bom Change'

    change_type=fields.Selection([('add','Add'),('remove','Remove'),('update','Update')],required=True)
    conflict=fields.Boolean('Conflict')
    eco_id=fields.Many2one(INNER_MODELS['eco'],string='OMT Modification',ondelete='cascade')
    eco_rebase_id=fields.Many2one(INNER_MODELS['eco'],string='OMT Rabase',ondelete='cascade')
    new_operation_id=fields.Many2one(INNER_MODELS['mrp.routing.workcenter'],string='New revised operation')
    new_product_qty=fields.Float('New revised quantity')
    new_uom_id=fields.Many2one(INNER_MODELS['uom.uom'],string='New revised bom')
    old_operation_id=fields.Many2one(INNER_MODELS['mrp.routing.workcenter'],string='Old revised operation')
    old_product_qty=fields.Float('Old revised quantity')
    old_uom_id=fields.Many2one(INNER_MODELS['uom.uom'],string='Old revised bom')
    operation_change=fields.Char('Consumed in operation',readonly=True)
    product_id=fields.Many2one(INNER_MODELS['product'],string='Article', required=True,ondelete='restrict')
    rebase_id=fields.Many2one(INNER_MODELS['eco'],string='Rebase',ondelete='cascade')
    uom_change=fields.Char('Uom',readonly=True)
    upd_product_qty=fields.Float('Quantity',readonly=True)

class Eco(Model):
    _name = INNER_MODELS['eco']
    _description='Plm Eco'
    _inherit = ['mail.activity.mixin', 'mail.thread.cc', 'mail.alias.mixin',
                'archive.mixin', 'sequence.mixin', 'company.mixin', 'color.mixin','kanban.mixin','priority.mixin']
    
    _order = "sequence, name, id"
    _check_company_auto = True

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        type_id = self.env.context.get(DEFAULT_TYPE_ID) or False
        
        return self.stage_find(type_id, [('fold', '=', False), ('final_stage', '=', False)])

    allow_apply_change=fields.Boolean('Allow apply change',compute='_compute_allow_apply_change',help="Show allowed apply changes")
    allow_change_stage=fields.Boolean('Allow change state', compute='_compute_allow_change_state', help="Allowing changing state")
    approval_ids=fields.One2many(INNER_MODELS['eco.approval'],'eco_id',help="validation approvals")
    bom_change_ids=fields.One2many(INNER_MODELS['eco.bom.change'],'eco_id',readonly=True,help='OMT Modification')
    bom_id=fields.Many2one(INNER_MODELS['mrp.bom'],string='Bom')
    bom_rebase_ids=fields.One2many(INNER_MODELS['eco.bom.change'],'rebase_id',string='Bom rebase')
    current_bom_id=fields.Many2one(INNER_MODELS['mrp.bom'],string='Current Bom')
    
    displayed_image_attachment_id=fields.Many2one(INNER_MODELS['attachment'],string='Attached piece')
    displayed_image_id=fields.Many2one(INNER_MODELS['mrp.document'],string='Image')

    effectivity=fields.Selection([('asap','Asap'),('date','to date')],'Effective date ',help="Date to do task",default='asap')
    effectivity_date=fields.Date('Effective date')
    
    mrp_document_count=fields.Integer('Attached document Nb',compute='_compute_mrp_document_count')
    mrp_document_ids=fields.One2many(INNER_MODELS['mrp.document'], 'res_id',help='Attached documents')
    my_activity_date_deadline=fields.Date('My effective date',help="My effective date dead line",readonly=True)
    name=fields.Char('Name',required=True)
    new_bom_id = fields.Many2many(INNER_MODELS['mrp.bom'])
    new_bom_revision=fields.Integer('BOM revision')
    note=fields.Text('Internal Notes')
    previous_change_ids=fields.One2many(INNER_MODELS['eco.bom.change'],'eco_rebase_id',string='Previous changed',readonly=True)
    product_tmpl_id=fields.Many2one(INNER_MODELS['product.tmpl'],string='Article')
    sequence=fields.Char(string='Sequence',required=True,copy=False,readonly=True,default=lambda self:_('New'))
    routing_change_ids=fields.One2many(INNER_MODELS['eco.routing.change'],'eco_id',string='Routing change')
    stage_id=fields.Many2one(INNER_MODELS['eco.stage'] ,
        ondelete='restrict',
        help="Stage",
        compute='_compute_stage_id',
        default=_get_default_stage_id,
        group_expand='_read_group_stage_names',
        index=True, tracking=True,copy=False,readonly=False, store=True,
        domain="[ ('type_id', '=', type_id)]"
        )
    state=fields.Selection(
        [('draft','Draft'),('confirmed','Confirmed'),('done','Done'),('rejected','Rejected')],
        string='State',
        default='draft',
        copy=False,required=True,help="Statut",tracking=True,store=True
        )
    tag_ids = fields.Many2many(INNER_MODELS['eco.tag'] , 'mrp_plm_eco_tags_rel', 'plm_id', 'tag_id', string='Tags')
    type=fields.Selection([('product','Product only'),('bom','BOM'),('routing','Routing'),('both','Both')],default='product',string='Apply to')
    type_id=fields.Many2one(INNER_MODELS['eco.type'],'Type',ondelete='restrict',required=True,help="Type",store=True)
    type_id_name=fields.Char(related='type_id.name',string='Type name')
    user_can_approve=fields.Boolean('Can approve',compute='_compute_user_can_approve',help="User can approve")
    user_can_reject=fields.Boolean('Can reject',compute='_compute_user_can_approve',help="User can reject")
    user_id=fields.Many2one(INNER_MODELS['res.users'],'Responsible',help="User responsible", default=lambda self: self.env.user, tracking=True)

    @api.model
    def create(self, vals):
        if 'state' in vals and vals['state']=='draft':
            vals['state']='confirmed'
        return super(Eco,self).create(vals)

    @api.model
    def default_get(self, default_fields):
        vals = super(Eco, self).default_get(default_fields)

        return vals
    
    @api.depends('type_id')
    def _compute_stage_id(self):
        for eco in self:
            if eco.plm_id:
                eco.stage_id = eco.stage_find(eco.id, [('fold', '=', False), ('final_stage', '=', False)])
            else:
                eco.stage_id = False

    def _compute_mrp_document_count(self):
        for record in self:
            record.mrp_document_count=0

    def _compute_allow_apply_change(self):
        for record in self:
            self.allow_apply_change,self.allow_change_stage=True,True

    
    @api.depends('state','stage_id','approval_ids')
    def _compute_user_can_approve(self):
        for record in self:
            self.user_can_reject=True
            if record.state not in ('draft','done','rejected'):
                record.user_can_approve=record.approval_ids.filtered(lambda r:self.env.user.id in r.required_user_ids).search_count([])
            else:
                record.user_can_approve=False

    def action_new_revision(self):
        self.ensure_one()
        if self.state=='confirmed':
            domain=[('type_id.id','=',self.type_id.id),('sequence','>',self.stage_id.sequence)]
            domain=[('type_id.id','=',self.type_id.id)]
            nextStage=self._eco_stage.search(domain)
            if nextStage.exists():
                for stage in nextStage:
                    print('stage seq:%s' % stage.sequence)
                self.stage_id=nextStage
    def apply_rebase(self):
        pass
    def conflict_resolve(self):
        pass
    def approve(self):
        pass
    def reject(self):
        pass
    def action_apply(self):
        pass
    def action_see_attachments(self):
        pass 
    def open_new_bom(self):
        pass
    def _alias_get_creation_values(self):
        values = super(Eco, self)._alias_get_creation_values()
        values['alias_model_id'] = self.env['ir.model']._get(INNER_MODELS['eco.stage']).id
        return values
    #     print('toto')
    def stage_find(self, type_id, domain=[], order='sequence'):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        # collect all section_ids
        type_ids = set()
        if type_id:
            type_ids.add(type_id)
        for eco in self:
            if eco.type_id:
                type_ids.add(eco.type_id.id)
        # eco_ids.extend(self.mapped('plm_id').ids)
        if type_ids:
            search_domain = [ ('type_id', 'in', list(type_ids))]
        else:
            search_domain = [('type_id', '=', False)]

        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self._eco_stage.search(search_domain, order=order, limit=1).id

    def _read_group_stage_names(self, stages, domain, order):
        type_id = self.env.context.get(DEFAULT_TYPE_ID) or False
        if not type_id:
            domain=[]
        stages_ids=stages.search(domain,order=order)
        return stages_ids


    

class EcoApprovalTemplate(Model):
    _name=INNER_MODELS['eco.approval.template']
    _description='Eco Approval Template'
    _inherit=['sequence.mixin']
    approval_type=fields.Selection([
        ('selection','Selection'),
        ('mandatory','Mandatory'),
        ('comment','Comment')],required=True,string="Validation Type")
    name=fields.Char('Role',required=True)
    stage_id=fields.Many2one(INNER_MODELS['eco.stage'],ondelete='restrict',string="Stage")
    user_ids=fields.Many2many(INNER_MODELS['res.users'],ondelete='restrict',required=True)

class EcoApproval(Model):
    _name=INNER_MODELS['eco.approval']
    _description='Eco Approval'
    _inherits = {INNER_MODELS['eco.approval.template']: 'approval_template_id'}

    approval_date=fields.Datetime('Approval date')
    approval_template_id=fields.Many2one(INNER_MODELS['eco.approval.template'] ,ondelete='cascade',required=True,string="Approval template",help="Approval template")
    eco_id=fields.Many2one(INNER_MODELS['eco'] ,'Technical Change',ondelete='cascade',required=True,help="Technical ECO")
    eco_stage_id=fields.Many2one(INNER_MODELS['eco.stage'],string="ECO Stage",help="ECO Stage")
    is_approved=fields.Boolean("Is approved",compute='_compute_is_approved',readonly=True)
    is_closed=fields.Boolean("Is closed",compute='_compute_is_closed',store=True,readonly=True)
    is_rejected=fields.Boolean("Is rejected",compute='_compute_is_rejected',store=True,readonly=True)
    name=fields.Char('Role',required=True)
    required_user_ids=fields.Many2many(INNER_MODELS['res.users'],string="Utilisateurs requis")
    status=fields.Selection([
        ('none','not yet'),
        ('comment','Comment'),
        ('approved','Approved'),
        ('rejected','Rejected')],'Statut',required=True)
    template_stage_id=fields.Many2one(INNER_MODELS['eco.stage'],string='Validation stage')
    user_id=fields.Many2one(INNER_MODELS['res.users'],'Approuvé par')

    def _compute_is_approved(self):
        for record in self:
            self.is_approved=True
    def _compute_is_closed(self):
        for record in self:
            self.is_closed=True
    def _compute_is_rejected(self):
        for record in self:
            self.is_rejected=True

class EcoType(Model):
    _name = INNER_MODELS['eco.type']
    _description = 'Eco Type'
    _inherit = ['mail.thread', 'mail.alias.mixin', 'mail.activity.mixin',
                'archive.mixin', 'sequence.mixin', 'company.mixin', 'color.mixin']
    _order = "sequence, name, id"
    _check_company_auto = True
    name = fields.Char("Name", index=True, required=True, tracking=True)
    nb_approvals = fields.Integer(
        'Nb Of Approvals', compute='_compute_nb_approval')
    nb_approvals_my = fields.Integer(
        'My Nb Of Approvals', compute='_compute_nb_approval_my')
    nb_ecos = fields.Integer('Nb Of ECOs', compute='_compute_nb_eco')
    nb_validation = fields.Integer(
        'Nb Of validation', compute='_compute_nb_validation')
    stage_ids = fields.One2many(
        INNER_MODELS['eco.stage'], 'type_id', string='Stages')

    def _compute_nb_approval(self):
        for record in self:
            record.nb_approvals = 0

    def _compute_nb_approval_my(self):
        for record in self:
            # res=self._eco.search_count([('user_can_approve','=',True),('type_id.id','=',record.id)])
            res=10
            record.nb_approvals_my = res

    def _compute_nb_eco(self):
        for record in self:
            res=self._eco.search_count([('state','not in',('done','rejected')),('type_id.id','=',record.id)])
            record.nb_ecos = res

    def _compute_nb_validation(self):
        for record in self:
            record.nb_validation = 0

    def _alias_get_creation_values(self):
        values = super(EcoType, self)._alias_get_creation_values()
        values['alias_model_id'] = self.env['ir.model']._get(INNER_MODELS['eco.stage']).id
        
        return values

class EcoStage(Model):
    _name = INNER_MODELS['eco.stage']
    _description = 'Eco Stage'
    _inherit = ['sequence.mixin']
    _order = "sequence, id"
    allow_apply_change = fields.Boolean(
        'Allow apply changes', help='Is this step allowing made changes')
    approval_roles = fields.Char(
        'Approval Roles', compute='_compute_approval_roles', store=True)
    approval_template_ids=fields.One2many(INNER_MODELS['eco.approval.template'],'stage_id',string="Stage Templates")
    final_stage = fields.Boolean('Final stage', help='Is this stage final')
    fold = fields.Boolean('fold in Kanban view',
                            help='Is this stage folded in kanban view')
    is_blocking = fields.Boolean(
        'Block stage', compute='_compute_is_blocking', readonly=True, help='Is this stage blocked')
    name = fields.Char('Name', required=True, translate=True)
    type_id = fields.Many2one(
        INNER_MODELS['eco.type'], 'Type', required=True, ondelete='restrict')
    # sequence_str=fields.Char(compute='_compute_seq')

    # @api.depends('sequence')
    # def _compute_seq(self):
    #     for record in self:
    #         record.sequence_str=str(record.sequence)
    def _compute_approval_roles(self):
        for record in self:
            record.approval_roles = ''

    def _compute_is_blocking(self):
        for record in self:
            record.is_blocking = False

    def name_get(self):
        # type_id = self.env.context.get(DEFAULT_TYPE_ID) or False
        # if not type_id:
        #     return [(stage.id, '%s / %s' % (stage.type_id.display_name, stage.name ) ) for stage in self]
        
        return [(stage.id,  stage.name  ) for stage in self]

class EcoTag(Model):
    _name = INNER_MODELS['eco.tag']
    _description = 'Eco Tag'
    _inherit = ['color.mixin']

    name = fields.Char('Name', required=True, translate=True)
    eco_ids = fields.Many2many(INNER_MODELS['eco'] , 'mrp_plm_eco_tags_rel', 'tag_id', 'plm_id', string='ECOs')
