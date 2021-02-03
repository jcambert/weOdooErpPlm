
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError
class WeAddonMrpProduction(models.Model):
    _inherit=['mrp.production']

    eco_count=fields.Integer(compute='_compute_eco_count')
    can_manufacture=fields.Boolean(compute='_compute_eco_count')
    can_planned=fields.Boolean(compute='_compute_eco_count')
    kanban_state=fields.Selection(
        [('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')],
        string= 'Kanban State',
        default='normal',
        compute='_compute_eco_count',
        help="État kanban",store=True,tracking=True,copy=False,required=True)

    @api.depends('product_tmpl_id','product_tmpl_id.eco_count','state')
    def _compute_eco_count(self):
        for record in self:
            if record.state in ['draft','confirmed']:
                record.eco_count=record.product_tmpl_id.eco_count
                record.can_manufacture=record.product_tmpl_id.can_manufacture
                record.can_planned=record.product_tmpl_id.can_planned
                record.kanban_state = 'normal' if record.can_manufacture else 'blocked'
               
            else:
                record.eco_count=0
                record.can_manufacture=True
                record.can_planned=False
                record.kanban_state = 'done' if record.state in ['done','cancel'] else 'normal'
  
    

    def action_confirm(self):
        for record in self:
            if record.eco_count>0 and not record.can_manufacture:
                raise UserError(_("You cannot manufacture a product while an ECO is running on ")+record.product_tmpl_id.name)
        super(WeAddonMrpProduction, self).action_confirm()

    def _plan_workorders(self, replan=False):
        """ Plan all the production's workorders depending on the workcenters
        work schedule.

        :param replan: If it is a replan, only ready and pending workorder will be take in account
        :type replan: bool.
        """
        self.ensure_one()

        if not self.workorder_ids:
            return
        if not self.can_planned:
            raise UserError(_("You cannot plane a manufacture for product while an ECO is running on ")+self.product_tmpl_id.name)
        super(WeAddonMrpProduction, self)._plan_workorders()
    def action_view_plm(self):
        action = self.env["ir.actions.actions"]._for_xml_id("weOdooErpPlm.mrp_plm_action")
        action['domain'] = [('state', '!=', 'done'), ('product_tmpl_id', 'in', self.ids)]
        action['context'] = {}
        return action
