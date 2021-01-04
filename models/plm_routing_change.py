# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmRoutingChange(models.Model):
    _name='mrp.plm.routing.change'
    _description="Mrp Plm Routing Change"
    change_type=fields.Selection([('add','Add'),('remove','Remove'),('update','Update')],'Change Type',required=True)
    display_name=fields.Char(readonly=True,string="Nom affiché")
    eco_id=fields.Many2one('mrp.plm','Technical change',ondelete='cascade',required=True,help="Modification technique")
    new_time_cycle_manual=fields.Float(string="Nouvelle durée manuelle")
    old_time_cycle_manual=fields.Float(string="Ancienne durée manuelle")
    upd_time_cycle_manual=fields.Float(string="Modification de la durée manuelle",readonly=True)
    workcenter_id=fields.Many2one('mrp.workcenter',ondelete='set null')