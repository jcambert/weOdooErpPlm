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
    eco_count=fields.Integer('Plm Count',store=False)
    # eco_count=fields.Integer('Plm Count',compute='_compute_eco_count')

    @api.model
    def default_get(self, fields):
        defaults = super(WeAddonProduct, self).default_get(fields)
        defaults['eco_count']=10
        return defaults

    # @api.depends('plm')
    # def _compute_eco_count(self):
    #     for record in self:
    #         record.eco_count= 5

    def action_view_plm(self):
        print('View PLM')
    # @api.onchange('purchase_ok')
    # def _onchange_purchase_ok(self):
        # if not self.purchase_ok :
        #     self.valtec=True
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
