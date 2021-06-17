# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api,_
class Plm(models.Model):
    _name='mrp.plm'
    _description='Mrp Plm'
    _inherit=['mail.activity.mixin','mail.thread']
    # bom_change_ids=fields.One2many('mrp.plm.bom.change','eco_id',readonly=True,help="Modifications de la nomenclature OMT")
    # bom_id=fields.Many2one('mrp.bom',ondelete='set null',help="Nomenclature")
    # bom_rebase_ids=fields.One2many('mrp.plm.bom.change','rebase_id',help="Refonte de la nomenclature")
    # company_id=fields.Many2one('res.company','Company',ondelete='set null',help="Societé")
    # current_bom_id=fields.Many2one('mrp.bom','Current Bom',ondelete='set null',help="Nouvelle nomenclature")
    # display_name=fields.Char(readonly=True,string="Nom affiché")
    # displayed_image_attachment_id=fields.Many2one('ir.attachment','Attachment',help="Pièce jointe associée")
    # displayed_image_id=fields.Many2one('mrp.document','Image displayed',ondelete='set null',help="Afficher l'image")
    # message_attachment_count=fields.Integer(readonly=True, string="Nombre de pièces jointes")
    # message_channel_ids=fields.Many2many('mail.channel',readonly=True,string="Abonnés (Canaux)")
    # message_follower_ids=fields.One2many('mail.followers','res_id',help="Abonnés")
    # message_has_error=fields.Boolean(readonly=True,help="Erreur d'envoi du message")
    # message_has_error_counter=fields.Integer(readonly=True,string="Nombre d'erreurs")
    # message_has_sms_error=fields.Integer(readonly=True,string="Erreur d'envoi SMS")
    # message_ids=fields.One2many('mail.message','res_id',help="Messages")
    # message_is_follower=fields.Boolean(readonly=True,string="Est un abonné")
    # message_main_attachment_id=fields.Many2one('ir.attachment',ondelete='set null',index=True)
    # message_needaction=fields.Boolean(readonly=True,string="Nécessite une action")
    # message_needaction_counter=fields.Integer(readonly=True,string="Nombre d'actions")
    # message_partner_ids=fields.Many2many('res.partner',readonly=True,string="Abonnés (Partenaires)")
    # message_unread=fields.Boolean(readonly=True,string="Messages non lus")
    # message_unread_counter=fields.Integer(readonly=True,string="Compteur de messages non lus")
    # mrp_document_count=fields.Integer(readonly=True,string="Nb. pièces jointes")
    # mrp_document_ids=fields.One2many('mrp.document','res_id',help="Pièces jointes")
    # new_bom_id=fields.Many2one('mrp.bom',ondelete='set null',help="Nouvelles nomenclatures")
    # new_bom_revision=fields.Integer(string="Révision de la nomenclature")
    # previous_change_ids=fields.One2many('mrp.plm.bom.change','eco_rebase_id',readonly=True, help="Anciennes modifications de l'OMT")
    # priority = fields.Selection([('0', 'Normal'),('1', 'Important'),], default='0', index=True, help="Priority")
    # routing_change_ids=fields.One2many('mrp.plm.routing.change','eco_id',readonly=True,help="Modifications de l'acheminement OMT")
    # tag_ids=fields.Many2many('mrp.plm.tag','Tag',string="Étiquettes")
    # type=fields.Selection([()],'Appliqué sur',required=True,help="Appliqué sur")
    # website_message_ids=fields.One2many('mail.message','res_id',help="Messages du site web")
   
    active=fields.Boolean('Active', default=True, help="Si le champ actif est défini sur False, vous pourrez masquer l'ordre de modification technique sans le supprimer.")
    allow_apply_change=fields.Boolean("Afficher les modifications appliquées",compute='_compute_allow_apply_change')
    allow_change_stage=fields.Boolean(compute='_compute_allow_change_state', string="Autoriser le changement d'étape")
    # allow_start_revision=fields.Boolean(compute='_compute_can_start_revision')
    approval_ids=fields.One2many('mrp.plm.approval','eco_id',help="Validations")
    color = fields.Integer('Couleur')
    effectivity=fields.Selection([('asap','Asap'),('date','to date')],'Date effective',help="Entrée en vigueur",default='asap')
    effectivity_date=fields.Date(string="Date d'entrée en vigueur")
    has_approval = fields.Integer('Has approval',readonly=True,compute='_compute_has_approval')
    
    name=fields.Char('Name',required=True,default=_('New'))
    note=fields.Text(string='Internal Notes')
    product_tmpl_id = fields.Many2one('product.template', 'Product',auto_join=True, ondelete="set null")
    stage_id=fields.Many2one('mrp.plm.stage',
        ondelete='restrict',
        help="Etape",
        compute='_compute_stage_id',
        group_expand='_read_group_stage_names',
        index=True, tracking=True,copy=False,readonly=False, store=True,
        domain="[ ('type_id', '=', type_id)]"
        )
    kanban_state_label = fields.Char(compute='_compute_kanban_state', string='Kanban State Label', tracking=True)
    kanban_state=fields.Selection(
        # [('waiting','Waiting start revision'), ('none','Not needed') ,('normal','Normal'),('done','Done'),('blocked','Blocked')],
        [('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')],
        string= 'Kanban State',
        default='normal',
        compute='_compute_kanban_state',
        help="État kanban",store=True,tracking=True,copy=False,required=True)
    state=fields.Selection(
        [('draft','Draft'),('confirmed','Confirmed'),('done','Done'),('rejected','Rejected')],
        string='State',
        default='draft',
        copy=False,required=True,help="Statut",tracking=True,store=True
        )
        
    tag_ids = fields.Many2many('mrp.plm.tag', 'mrp_plm_tags_rel', 'plm_id', 'tag_id', string='Tags')
    type_id=fields.Many2one('mrp.plm.type','Type',ondelete='restrict',required=True,help="Type",store=True)
    user_can_approve=fields.Boolean("Peut Approuver",compute='_compute_user_can_approve')
    user_can_reject=fields.Boolean("Peut Refuser",compute='_compute_user_can_approve')
    user_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="responsable")
    can_purchase=fields.Boolean("Peut acheter",default=False)
    can_manufacture=fields.Boolean("Peut Produire",default=False)
    can_deliver=fields.Boolean("Peut Livrer",default=False)
    can_receive=fields.Boolean("Peut receptionner",default=False)
    can_start_revision=fields.Boolean("can start revision",default=True,compute="_compute_can_start_revision")
    is_sale=fields.Boolean(store=True,readonly=True,compute='_compute_is_sale_or_purchase')
    is_purchase=fields.Boolean(store=True,readonly=True,compute='_compute_is_sale_or_purchase')

    # def write(self, vals):
    #     # Overridden to reset the kanban_state to normal whenever
    #     # the stage (stage_id) of the Maintenance Request changes.
    #     if vals and 'kanban_state' not in vals and 'stage_id' in vals:
    #         vals['kanban_state'] = 'normal'

   
    def _read_group_stage_names(self, stages, domain, order):
        # search_domain = [ ('id', 'in', stages.ids)]
        search_domain=[]
        stages_ids = stages.search(search_domain)
        return stages_ids

    @api.depends('state')
    def _compute_allow_change_state(self):
        for record in self:
            record.allow_change_stage= record.state not in ['draft','done','rejected']

    @api.depends('type_id')
    def _compute_stage_id(self):
        for record in self:
            if not record.stage_id:
                record.stage_id = record._stage_find(domain=[('fold', '=', False)]).id

    def _stage_find(self,  domain=None, order='sequence'):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param team_id
            :param domain : base search domain for stage
            :returns crm.stage recordset
        """
        search_domain=[]
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        result= self.env['mrp.plm.stage'].search(search_domain, order=order, limit=1)           
        return result

    def _compute_allow_apply_change(self):
        for record in self:
            record.allow_apply_change=True
 
    @api.depends('state')
    def _compute_can_start_revision(self):
        for record in self:
            # record.allow_start_revision=
            record.can_start_revision = (record.state=='draft' and isinstance(record.id,models.NewId))

    @api.depends('state','stage_id')
    def _compute_user_can_approve(self):
        me=self.env.user
        for record in self:
            if(record.state!='confirmed'):
                record.user_can_approve= False
                record.user_can_reject= False
                continue
            candidates=record.approval_ids.search([('template_stage_id','=',record.stage_id.id)])
            if candidates.exists():
                for candidate in candidates:
                    if candidate.is_approved:
                        record.user_can_approve= False
                        record.user_can_reject= True
                        break
                   
                    is_in_role=me.is_in_role(record.approval_ids.roles)
                    record.user_can_approve=is_in_role 
                    record.user_can_reject= is_in_role
            else:
                record.user_can_approve=False
                record.user_can_reject= False
    

    # @api.depends('kanban_state')
    # def _compute_kanban_state_label(self):
    #     for record in self:
    #         if record.kanban_state == 'normal':
    #             record.kanban_state_label = _('Progress')
    #         elif record.kanban_state == 'blocked':
    #             record.kanban_state_label = _('Blocked')
    #         else:
    #             record.kanban_state_label = _('Done')

    @api.depends('stage_id','state')
    def _compute_kanban_state(self):
        for record in self:
            candidates=record.approval_ids.search([('template_stage_id','=',record.stage_id.id)])
            if not candidates.exists():
                if record.state=='confirmed':
                    record.kanban_state='normal'    
                elif record.state=='done':
                    record.kanban_state='done'
                elif record.state=='rejected':
                    record.kanban_state='blocked'
            else:
                for candidate in candidates:
                    if candidate.is_rejected:
                        record.kanban_state='blocked'
                        break
                    if candidate.need_approval():
                        record.kanban_state='normal'
                        break
                    if candidate.is_treated():
                        record.kanban_state='done'
            if record.kanban_state == 'normal':
                record.kanban_state_label = _('Progress')
            elif record.kanban_state == 'blocked':
                record.kanban_state_label = _('Blocked')
            else:
                record.kanban_state_label = _('Done')
            # if record.state=='done':
            #     record.kanban_state='done'
            # else:
            #     record.kanban_state='normal'

    @api.depends('product_tmpl_id')
    def _compute_is_sale_or_purchase(self):
        for record in self:
            if record.product_tmpl_id.exists():
                record.is_sale= record.product_tmpl_id.sale_ok
                record.is_purchase= record.product_tmpl_id.purchase_ok
            else:
                record.is_sale = False
                record.is_purchase= False
    
    @api.depends('approval_ids')
    def _compute_has_approval(self):
        for record in self:
            record.has_approval = len(record.approval_ids.ids)>0
    # @api.depends('state')
    # def _compute_can_start_revision(self):
    #     for record in self:
    #         record.allow_start_revision= not isinstance(record.id,models.NewId) and record.state=='confirmed'
                
    @api.model
    def default_get(self, fields):
        defaults = super(Plm, self).default_get(fields)
        # defaults['name']=_('New')
        # defaults['state']='draft'
        # defaults['stage_id']=self.stage_id.search([])[0]
        #defaults['kanban_state']='normal'
        # defaults['is_sale']=False
        # defaults['is_purchase']=False
        # defaults['effectivity']='asap'
        # defaults['user_can_approve']=True
        # defaults['user_can_reject']=True
        defaults['user_id']=self.env.user

        return defaults
    
    
    # @api.onchange('product_tmpl_id')
    # def _onchange_purchase_ok(self):
    #     print("product has changed",self.product_tmpl_id)
    #     self.is_sale=self._compute_is_sale_or_purchase()
    #     self.is_purchase=self._compute_is_sale_or_purchase()

    @api.onchange('type_id')
    def _onchange_type_id(self):
        items=self.env['mrp.plm.stage'].search([('type_id.id','=',self.type_id.id)])
        if items.exists():
            self.stage_id=items[0]

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        can_go_back = self.env['ir.config_parameter'].get_param('weOdooErpPlm.can_go_back') or False
        def restore(record):
            record.stage_id=record._origin.stage_id
        
        for record in self.filtered(lambda r:r._origin.state!=False):
            if record.state in ['draft'] :
                restore(record)
                raise UserError("You cannot change step when modification is in draft mode")
            # if  isinstance(record.id,models.NewId ) or record.stage_id.id==record._origin.stage_id.id :
            #     continue
            
                
            # elif record._origin.stage_id.final_stage:
            #     restore(record)
            #     raise UserError("You cannot move a final staged modification")

            if record.stage_id.sequence<record._origin.stage_id.sequence and not can_go_back:
                restore(record)
                raise UserError("You cannot go back")
            elif record.stage_id.sequence<record._origin.stage_id.sequence and can_go_back:
                if record.stage_id.reject_stage:
                    record.state='rejected'
                elif record.stage_id.final_stage:
                    record.state='done'
                else:
                    record.state='confirmed'
                continue
            if record.need_approval(record._origin.stage_id) and not record.stage_id.reject_stage:
                
                restore(record)
                raise UserError("An approval is needed")
            
            if record.stage_id.reject_stage:
                record.state='rejected'
            elif record.stage_id.final_stage:
                 record.state='done'
                # record.kanban_state='done'
                # record.update({'state':'done'})
    @api.model
    def need_approval(self,stage_id):
        result=True
        candidates=self.approval_ids.search([('template_stage_id','=',stage_id.id)])
        if candidates.exists():
            for candidate in candidates:
                result=candidate.need_approval() and result
        else:
            result=False       
        return result
    def action_new_revision(self):
        # raise UserError("You can't do that!")
        # return
        record=self
        if isinstance(self.id, models.NewId):
            return False
        print('start new Revision')
        # record.update(state='confirmed')
        # record.state='confirmed'
        model=self.env['mrp.plm.approval']
        stages=self.env['mrp.plm.stage'].search([('type_id.id','=',record.type_id.id)])
        for stage in stages.sorted(key=lambda s:s.sequence):
            for approval_tmpl in stage.approval_template_ids:
                for role in approval_tmpl.roles.mapped("id") :
                    print('create approval')
                    model.create({
                    "approval_template_id":approval_tmpl.id,
                    "eco_id":record.id,
                    "eco_stage_id":record.stage_id.id,
                    "template_stage_id":approval_tmpl.stage_id.id,
                    "roles":role 
                    
                    })
        return record.write({'state':'confirmed'})
    def _get_first_approval_can_approve(self):
        me=self.env.user
        candidates = self.approval_ids.search([('template_stage_id','=',self.stage_id.id)])
        if not candidates.exists():
            return None
        
        for candidate in candidates:
            for role in candidate.roles:
                is_in_role=me.is_in_role([role])
                if is_in_role:
                    return candidate
        return None
        
    def action_approve(self):
        candidate=self._get_first_approval_can_approve()
        if candidate is not None:
            candidate.approve()

    def action_reject(self):
        self.approval_ids.reject(self.stage_id)
        _current=self.stage_id
        _next=self.env['mrp.plm.stage'].search([('type_id.id','=',_current.type_id.id), ('sequence','>',_current.sequence)])
        if _next.exists():
            self.stage_id=_next[len(_next.ids)-1].id
