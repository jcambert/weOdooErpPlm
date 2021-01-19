# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
class Plm(models.Model):
    _name='mrp.plm'
    _description='Mrp Plm'
    _inherit=['mail.activity.mixin','mail.thread']
    
    active=fields.Boolean('Active', default=True, help="Si le champ actif est défini sur False, vous pourrez masquer l'ordre de modification technique sans le supprimer.")
    allow_apply_change=fields.Boolean("Afficher les modifications appliquées",compute='_compute_allow_apply_change')
    # allow_change_stage=fields.Boolean(readonly=True, string="Autoriser le changement d'étape")
    approval_ids=fields.One2many('mrp.plm.approval','eco_id',help="Validations")
    # bom_change_ids=fields.One2many('mrp.plm.bom.change','eco_id',readonly=True,help="Modifications de la nomenclature OMT")
    # bom_id=fields.Many2one('mrp.bom',ondelete='set null',help="Nomenclature")
    # bom_rebase_ids=fields.One2many('mrp.plm.bom.change','rebase_id',help="Refonte de la nomenclature")
    color = fields.Integer('Couleur')
    # company_id=fields.Many2one('res.company','Company',ondelete='set null',help="Societé")
    # current_bom_id=fields.Many2one('mrp.bom','Current Bom',ondelete='set null',help="Nouvelle nomenclature")
    # display_name=fields.Char(readonly=True,string="Nom affiché")
    # displayed_image_attachment_id=fields.Many2one('ir.attachment','Attachment',help="Pièce jointe associée")
    # displayed_image_id=fields.Many2one('mrp.document','Image displayed',ondelete='set null',help="Afficher l'image")
    effectivity=fields.Selection([('asap','Asap'),('date','to date')],'Date effective',help="Entrée en vigueur")
    effectivity_date=fields.Date(string="Date d'entrée en vigueur")
    kanban_state=fields.Selection([('normal','Normal'),('done','Done'),('blocked','Blocked')],'Kanban State',compute='_compute_kanban_state',help="État kanban")
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
    name=fields.Char(required=True,string="Référence")
    # new_bom_id=fields.Many2one('mrp.bom',ondelete='set null',help="Nouvelles nomenclatures")
    # new_bom_revision=fields.Integer(string="Révision de la nomenclature")
    note=fields.Text(string='Internal Notes')
    # previous_change_ids=fields.One2many('mrp.plm.bom.change','eco_rebase_id',readonly=True, help="Anciennes modifications de l'OMT")
    # priority = fields.Selection([('0', 'Normal'),('1', 'Important'),], default='0', index=True, help="Priority")
    product_tmpl_id = fields.Many2one('product.template', 'Product Template',auto_join=True, ondelete="set null")
    # routing_change_ids=fields.One2many('mrp.plm.routing.change','eco_id',readonly=True,help="Modifications de l'acheminement OMT")
    stage_id=fields.Many2one('mrp.plm.stage',ondelete='restrict',help="Etape")
    state=fields.Selection([('confirmed','Confirmed'),('progress','Progress'),('rebase','Rebase'),('conflict','Conflict'),('done','Done')],'Status',required=True,readonly=True,help="Statut")
    # tag_ids=fields.Many2many('mrp.plm.tag','Tag',string="Étiquettes")
    tag_ids = fields.Many2many('mrp.plm.tag', 'mrp_plm_tags_rel', 'plm_id', 'tag_id', string='Tags')
    # type=fields.Selection([()],'Appliqué sur',required=True,help="Appliqué sur")
    type_id=fields.Many2one('mrp.plm.type','Type',ondelete='restrict',required=True,help="Type",store=True)
    user_can_approve=fields.Boolean("Peut Approuver",compute='_compute_user_can_approve')
    user_can_reject=fields.Boolean("Peut Refuser",compute='_compute_user_can_reject')
    user_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="responsable")
    # website_message_ids=fields.One2many('mail.message','res_id',help="Messages du site web")
    can_purchase=fields.Boolean("Peut acheter",default=False)
    can_manufacture=fields.Boolean("Peut Produire",default=False)
    can_deliver=fields.Boolean("Peut Livrer",default=False)
    can_receive=fields.Boolean("Peut receptionner",default=False)

    is_sale=fields.Boolean(store=False)
    is_purchase=fields.Boolean(store=False)
    
    def _compute_allow_apply_change(self):
        for record in self:
            record.allow_apply_change=True
    def _compute_user_can_approve(self):
        for record in self:
            record.user_can_approve=True
    def _compute_user_can_reject(self):
        for record in self:
            record.user_can_reject=True
    def _compute_kanban_state(self):
        for record in self:
            record.kanban_state='normal'
    def _compute_is_sale(self):
        if self.product_tmpl_id.exists():
            return self.product_tmpl_id.sale_ok
        else:
            return False
    def _compute_is_purchase(self):
        if self.product_tmpl_id.exists():
            return self.product_tmpl_id.purchase_ok
        else:
            return False

    @api.model
    def default_get(self, fields):
        defaults = super(Plm, self).default_get(fields)
        defaults['name']=_('New')
        defaults['state']='confirmed'
        defaults['stage_id']=self.stage_id.search([])[0]
        defaults['kanban_state']='normal'
        defaults['is_sale']=False
        defaults['is_purchase']=False
        defaults['effectivity']='asap'
        defaults['user_can_approve']=True
        defaults['user_can_reject']=True
        return defaults

    @api.onchange('product_tmpl_id')
    def _onchange_purchase_ok(self):
        print("product has changed",self.product_tmpl_id)
        self.is_sale=self._compute_is_sale()
        self.is_purchase=self._compute_is_purchase()

    def action_new_revision(self):
        print('start new Revision')
        self.state='progress'