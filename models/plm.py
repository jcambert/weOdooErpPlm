# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api,_,SUPERUSER_ID
from .models import INNER_MODELS, Model

class Plm(Model):
    _name=INNER_MODELS['plm'] 
    _description='Mrp Plm'
    _inherit=['mail.activity.mixin','mail.thread','mail.alias.mixin','archive.mixin','sequence.mixin','company.mixin' ,'color.mixin']
    _order = "sequence, name, id"
    _check_company_auto = True

    
    def _compute_task_count(self):
        task_data = self._task.read_group([('plm_id', 'in', self.ids), '|', '&', ('stage_id.is_closed', '=', False), ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['plm_id'], ['plm_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.task_count = result.get(project.id, 0)

    name = fields.Char("Name", index=True, required=True, tracking=True)
    description = fields.Html()
    task_ids = fields.One2many(INNER_MODELS['task'] , 'plm_id', string='Tasks',domain=['|', ('stage_id', '=', False), ('stage_id.fold', '=', False)])
    tasks = fields.One2many(INNER_MODELS['task'], 'plm_id', string="Task Activities")
    task_count = fields.Integer(compute='_compute_task_count', string="Task Count")
    type_ids = fields.Many2many(INNER_MODELS['type'], 'plm_task_type_rel', 'plm_id', 'type_id', string='Tasks Stages')
    
    user_id = fields.Many2one('res.users', string='Plm Manager', default=lambda self: self.env.user, tracking=True)



    # ---------------------------------------------------
    #  Actions
    # ---------------------------------------------------

    def action_view_tasks(self):
        action = self.with_context(active_id=self.id, active_ids=self.ids) \
            .env.ref('weOdooErpPlm.act_project_project_2_project_task_all') \
            .sudo().read()[0]
        action['display_name'] = self.name
        return action

    # ---------------------------------------------------
    #  Business Methods
    # ---------------------------------------------------
