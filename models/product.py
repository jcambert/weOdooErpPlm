# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .models import Model,INNER_MODELS
class WeAddonProduct(Model):
    _inherit = [ INNER_MODELS['product_tmpl']]
    _description = 'Product Erp extensions'
    # valtec = fields.Boolean( default=True, help="If unchecked, it will allow you to disable launch manufacturing")
    state = fields.Selection(selection=[
        ('new','New'),
        ('active', 'Confirmed'),
        ('under_lifecycle_change','Under Lifecycle Change'),
         ('inactive', 'Deactivated')
    ],string='State',required=True,store=True,readonly=True,default='new')
    plm=fields.One2many(INNER_MODELS['plm'] ,'product_tmpl_id',help="PLM")
    eco_count=fields.Integer('Plm Count',compute='_compute_eco_count',store=True,required=True,default=0)
    can_purchase = fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_manufacture=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_deliver=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_receive=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_planned=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    @api.model
    def default_get(self, fields):
        defaults = super(WeAddonProduct, self).default_get(fields)
        # defaults['eco_count']=10
        return defaults

    @api.depends('plm.stage_id','plm.can_planned','plm.can_purchase','plm.can_manufacture','plm.can_deliver','plm.can_receive')
    def _compute_eco_count(self):
        _can_purchase=lambda c:c.can_purchase
        _can_manufacture=lambda c:c.can_manufacture
        _can_deliver=lambda c:c.can_deliver
        _can_receive=lambda c:c.can_receive
        _can_planned=lambda c:c.can_planned
        for record in self:
            
            eco=self._plm.search([('product_tmpl_id','=',record.id), ('state','!=','done')])
            record.eco_count= len(eco.ids)
            # record.plm.search_count([('id','=',record.id), ('state','!=','done')])
            if record.eco_count>0:
                record.can_purchase = len(eco.filtered(_can_purchase))>0
                # record.plm.search_count([('state','!=','done'),('can_purchase','=',True)])>0
                record.can_manufacture =len(eco.filtered(_can_manufacture))>0
                #  record.plm.search_count([('state','!=','done'),('can_manufacture','=',True)])>0 
                record.can_deliver =len(eco.filtered(_can_deliver))>0
                #  record.plm.search_count([('state','!=','done'),('can_deliver','=',True)])>0 
                record.can_receive =len(eco.filtered(_can_receive))>0
                #  record.plm.search_count([('state','!=','done'),('can_receive','=',True)])>0 
                record.can_planned= len(eco.filtered(_can_planned))>0
                #  record.plm.search_count([('state','!=','done'),('can_planned','=',True)])>0 
            else:
                record.can_purchase = True
                record.can_manufacture =True
                record.can_deliver = True
                record.can_receive = True
                
    def action_view_plm(self):
        action = self.env["ir.actions.actions"]._for_xml_id("weOdooErpPlm.mrp_plm_action")
        action['domain'] = [('state', '!=', 'done'), ('product_tmpl_id', 'in', self.ids)]
        action['context'] = {}
        return action

