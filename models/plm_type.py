
# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api,_
class PlmType(models.Model):
    _name='mrp.plm.type'
    _description = "Mrp Plm Type"

    # name=fields.Char('Name')
    _inherit=['mrp.plm.seq','mrp.plm.tag']
    # _inherit=['mrp.plm.seq','mrp.plm.tag','mail.alias.mixin']
    # message_attachment_count=fields.Integer(readonly=True,string="Nombre de pièces jointes")
    # message_channel_ids=fields.Many2many('mail.channel',string="Abonnés (Canaux)")
    # message_follower_ids=fields.One2many('mail.followers','res_id',string="Abonnés")
    # message_has_error=fields.Boolean(string="Erreur d'envoi du message")
    # message_has_error_counter=fields.Integer(readonly=True,string="Nombre d'erreurs")
    # message_has_sms_error=fields.Boolean(readonly=True,string="Erreur d'envoi SMS")
    # message_ids=fields.One2many('mail.message','res_id',string="Messages")
    # message_is_follower=fields.Boolean(readonly=True, string="Est un abonné")
    # message_main_attachment_id=fields.Many2one('ir.attachment',index=True,ondelete='set null',string="Pièce jointe principale")
    # message_needaction=fields.Boolean(string="Nécessite une action")
    # message_needaction_counter=fields.Integer(readonly=True,string="Nombre d'actions")
    # message_partner_ids=fields.Many2many('res.partner')

    # message_unread=fields.Boolean(readonly=True,string="Messages non lus")
    # message_unread_counter=fields.Integer(readonly=True,string="Compteur de messages non lus")

    nb_approvals=fields.Integer(readonly=True,string="En attente de validation",compute='_compute_nb_approvals')
    nb_approvals_my=fields.Integer(readonly=True,string="En attente de ma validation",compute='_compute_nb_approvals_my')
    nb_ecos=fields.Integer(readonly=True,compute='_compute_nb_ecos')
    nb_validation=fields.Integer(readonly=True,string="À appliquer",compute='_compute_nb_validation')
    stage_ids=fields.One2many('mrp.plm.stage','type_id',string="Etapes")
    # website_message_ids=fields.One2many('mail.message','res_id',string="Messages du site web")

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