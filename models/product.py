# -*- coding: utf-8 -*-

from odoo import models, fields, api
class WeAddonProduct(models.Model):
    _inherit = ['product.template']
    _description = 'Product Erp extensions'
    # valtec = fields.Boolean( default=True, help="If unchecked, it will allow you to disable launch manufacturing")
    state = fields.Selection(selection=[
        ('new','New'),
        ('active', 'Confirmed'),
        ('under_lifecycle_change','Under Lifecycle Change'),
         ('inactive', 'Deactivated')
    ],string='State',required=True,store=True,readonly=True,default='new')
    plm=fields.One2many('mrp.plm','product_tmpl_id',help="PLM")
    eco_count=fields.Integer('Plm Count',compute='_compute_eco_count',store=True,required=True,default=0)
    can_purchase = fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_manufacture=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_deliver=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    can_receive=fields.Boolean(compute='_compute_eco_count',readonly=True,store=True,required=True,default=True)
    @api.model
    def default_get(self, fields):
        defaults = super(WeAddonProduct, self).default_get(fields)
        # defaults['eco_count']=10
        return defaults

    @api.depends('plm.stage_id')
    def _compute_eco_count(self):
        for record in self:
            record.eco_count= self.plm.search_count([('state','!=','done')])
            if record.eco_count>0:
                record.can_purchase = self.plm.search_count([('state','!=','done'),('can_purchase','=',True)])>0
                record.can_manufacture = self.plm.search_count([('state','!=','done'),('can_manufacture','=',True)])>0 
                record.can_deliver = self.plm.search_count([('state','!=','done'),('can_deliver','=',True)])>0 
                record.can_receive = self.plm.search_count([('state','!=','done'),('can_receive','=',True)])>0 
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

