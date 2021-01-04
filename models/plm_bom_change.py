# -*- coding: utf-8 -*-

from odoo import models, fields, api
class PlmBomChange(models.Model):
    _name='mrp.plm.bom.change'
    _description="Mrp Plm Bom Change"
    change_type=fields.Selection([('add','Add'),('remove','Remove'),('update','Update')],required=True)
    conflict=fields.Boolean(string="Conflit")
    display_name=fields.Char(readonly=True,string="Nom affiché")
    eco_id=fields.Many2one('mrp.plm','Technical change',ondelete='cascade',required=True,help="Modification technique")
    eco_rebase_id=fields.Many2one('mrp.plm','Last Rebase',ondelete='cascade',required=True,help="Refonte OMT")
    new_operation_id=fields.Many2one('mrp.routing.workcenter',ondelete='set null',string="Nouvellement consommé dans l'opération")
    new_product_qty=fields.Float(string="Nouvelle quantité révisée")
    old_operation_id=fields.Many2one('mrp.routing.workcenter','Last Operation Consumed',ondelete='set null',help="Anciennement consommé dans l'opération")
    new_product_qty=fields.Float(string="Ancienne quantité révisée")
    old_uom_id=fields.Many2one('uom.uom','Last quantity consumed',ondelete='set null',help="Ancienne nomenclature de produit")
    operation_change=fields.Char(readonly=True,string="Consommé dans l'opération")
    product_id=fields.Many2one('product.product','Article',ondelete='restrict',required=True,help="Article")
    rebase_id=fields.Many2one('mrp.plm','Rebase',ondelete='cascade',help="Refonte")
    uom_change=fields.Char(readonly=True,string="Unité de mesure")
    upd_product_qty=fields.Float(readonly=True,string="Quantité")