# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PlmActivity(models.Model):
    _name='mrp.plm.activity'
    _description='Mrp Plm Activity'
    _inherit=['mail.activity.mixin']
    # active=fields.Boolean(string="Actif")
    # activity_date_deadline=fields.Date(readonly=True,string="Date limite de l'Activité à Venir")
    # activity_exception_decoration=fields.Selection([
    #     ('warning', 'Alert'),
    #     ('danger', 'Error')],readonly=True,help="Activité d'exception de décoration")
    # activity_exception_icon=fields.Char(readonly=True, string="Icone")
    # activity_ids=fields.One2many('mail.activity','res_id',string="Activités")
    # activity_state=fields.Selection([
    #     ('overdue','Overdue'),
    #     ('today','Today'),
    #     ('planned','Planned')],'State',readonly=True)
    # activity_summary=fields.Char(string="Résumé d'activité suivante")
    # activity_type_icon=fields.Char(readonly=True, string="Icône de type d'activité")
    # activity_type_id=fields.Many2one('mail.activity.type',domain="['|', ('res_model_id', '=', False), ('res_model_id', '=', res_model_id)]",string="Type d'activités à venir")
    # activity_user_id=fields.Many2one('res.users',string="Utilisateur Responsable")