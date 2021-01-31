
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError
class WeAddonMrpProduction(models.Model):
    _inherit=['mrp.production']

    eco_count=fields.Integer(compute='_compute_eco_count')
    can_manufacture=fields.Boolean(compute='_compute_eco_count')
    kanban_state=fields.Selection(
        [('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')],
        string= 'Kanban State',
        default='normal',
        compute='_compute_eco_count',
        help="État kanban",store=True,tracking=True,copy=False,required=True)

    @api.depends('product_tmpl_id.eco_count','state')
    def _compute_eco_count(self):
        for record in self:
            if record.state in ['draft']:
                record.eco_count=record.product_tmpl_id.eco_count
                record.can_manufacture=record.product_tmpl_id.can_manufacture
                record.kanban_state = 'normal' if record.can_manufacture else 'blocked'
                continue
            
            record.eco_count=0
            record.can_manufacture=True
            record.kanban_state = 'done' if record.state in ['done','cancel'] else 'normal'
  
    

    def action_confirm(self):
        for record in self:
            if record.eco_count>0 and not record.can_manufacture:
                raise UserError(_("You cannot product while an ECO is running on ")+record.product_tmpl_id.name)
        super(WeAddonMrpProduction, self).action_confirm()
    def action_view_plm(self):
        action = self.env["ir.actions.actions"]._for_xml_id("weOdooErpPlm.mrp_plm_action")
        action['domain'] = [('state', '!=', 'done'), ('product_tmpl_id', 'in', self.ids)]
        action['context'] = {}
        return action
