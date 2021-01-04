
# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmType(models.Model):
    _name='mrp.plm.type'
    _description = "Mrp Plm Type"
    _inherit=['mail.alias.mixin','mrp.plm.seq','mrp.plm.tag']
    
    message_attachment_count=fields.Integer(readonly=True,string="Nombre de pièces jointes")
    message_channel_ids=fields.Many2many('mail.channel',string="Abonnés (Canaux)")
    message_follower_ids=fields.One2many('mail.followers','res_id',string="Abonnés")
    message_has_error=fields.Boolean(string="Erreur d'envoi du message")
    message_has_error_counter=fields.Integer(readonly=True,string="Nombre d'erreurs")
    message_has_sms_error=fields.Boolean(readonly=True,string="Erreur d'envoi SMS")
    message_ids=fields.One2many('mail.message','res_id',string="Messages")
    message_is_follower=fields.Boolean(readonly=True, string="Est un abonné")
    message_main_attachment_id=fields.Many2one('ir.attachment',index=True,ondelete='set null',string="Pièce jointe principale")
    message_needaction=fields.Boolean(string="Nécessite une action")
    message_needaction_counter=fields.Integer(readonly=True,string="Nombre d'actions")
    message_partner_ids=fields.Many2many('res.partner')

    message_unread=fields.Boolean(readonly=True,string="Messages non lus")
    message_unread_counter=fields.Integer(readonly=True,string="Compteur de messages non lus")
    nb_approvals=fields.Integer(readonly=True,string="En attente de validation")
    nb_approvals_my=fields.Integer(readonly=True,string="En attente de ma validation")
    nb_ecos=fields.Integer(readonly=True)
    nb_validation=fields.Integer(readonly=True,string="À appliquer")
    stage_ids=fields.One2many('mrp.plm.stage','type_id',string="Etapes")
    website_message_ids=fields.One2many('mail.message','res_id',string="Messages du site web")
    