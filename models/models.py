from odoo import models, fields, api,_
from ast import literal_eval as _literal_eval
import logging
from random import randint
_logger = logging.getLogger(__name__)

INNER_MODELS={
    # 'plm':'mrp.plm', 
    # 'task':'mrp.plm.task',
    # 'type':'mrp.plm.type',
    # 'tag':'mrp.plm.tag',
    # 'approval':'mrp.plm.approval',
    # 'approval_tmpl':'mrp.plm.approval.template',
    # 'stage':'mrp.plm.stage',
    # 'stage_template':'mrp.plm.stage.template',
    'product':'product.product',
    'product.tmpl':'product.template',
    'eco.type':'mrp.plm.eco.type',
    'eco.stage':'mrp.plm.eco.stage',
    'eco.tag':'mrp.plm.eco.tag',
    'eco':'mrp.plm.eco',
    'eco.approval':'mrp.plm.eco.approval',
    'eco.approval.template':'mrp.plm.eco.approval.template',
    'eco.bom.change':'mrp.plm.eco.bom.change',
    'eco.routing.change':'mrp.plm.eco.routing.change',
    'mrp.document':'mrp.document',
    'mrp.bom':'mrp.bom',
    'mrp.routing.workcenter':'mrp.routing.workcenter',
    'mrp.workcenter':'mrp.workcenter',
    'res.users':'res.users',
    'uom.uom':'uom.uom',
    'attachment':'ir.attachment'}

def literal_eval(arg):
    if isinstance(arg,bool):
        return arg
    return _literal_eval(arg)

class Models():
    __slots__=('__dict__')
    def __init__(self,*args):
        for arg in args:
            if isinstance(arg,dict):
                _dict={}
                for k in arg.keys():
                    _dict[k.replace('.','_')]=arg[k]
                self.__dict__.update(_dict)
            else:
                _logger.error('Models name arg must be a dict')
        
    def __getitem__(self,key):
        return self.__dict__[key]

class Model(models.Model):
    """ Main super-class for regular database-persisted Odoo models.

    Odoo models are created by inheriting from this class::

        class user(Model):
            ...

    The system will later instantiate the class once per database (on
    which the class' module is installed).
    """
    _auto = True                # automatically create database backend
    _register = False           # not visible in ORM registry, meant to be python-inherited only
    _abstract = False           # not abstract
    _transient = False          # not transient

    _model_prefix='_'
    _models=Models( INNER_MODELS)
    
    
        
    def get_param(self,key):
        return literal_eval( self.env['ir.config_parameter'].get_param(key) or False)

    

    def __getattr__(self,key):
        
        _key=(key if isinstance(key,str) else str(key))
        if _key.startswith(self._model_prefix) and _key[len(self._model_prefix):]  in self._models.__dict__:
            return self.env[self._models[_key[len(self._model_prefix):]]]
        if not hasattr(super(models.Model,self),key):
            raise AttributeError
        res =super(models.Model,self).__getattr__(key)
        return res
        


    def map(self,fn):
        return map(fn,self)


class BaseArchive(models.AbstractModel):
    _name='archive.mixin'
    _description='Archive Mixin'
    active = fields.Boolean('Active',default=True)

    def do_archive(self):
        for rec in self:
            rec.active = True

class BaseSequence(models.AbstractModel):
    _name='sequence.mixin'
    _description='Sequence Mixin'
    _sequence_name=''
    sequence = fields.Integer(string='Sequence',default=1,help="Ordering sequence")

    @api.model
    def seq_next_by_code(self,name=''):
        return self.env['ir.sequence'].next_by_code(name or self._sequence_name or self._name)

    @api.model
    def create(self,vals):
        seq=self.seq_next_by_code()
        if vals.get('sequence',_('New'))==_('New'):
            vals['sequence']=(seq or _('New')) 
        elif seq:
            vals['sequence']=seq
        res=super(BaseSequence,self).create(vals)
        return res
class BaseCompany(models.AbstractModel):
    _name='company.mixin'
    _description='Company Mixin'
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

class BaseColor(models.AbstractModel):
    _name='color.mixin'
    _description='Color Mixin'
    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer(string='Color Index', default=_get_default_color)

class BaseKanbanState(models.AbstractModel):
    _name='kanban.mixin'
    _description='kanban Mixin'

    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Kanban State',
        copy=False, default='normal', required=True)

class BasePriority(models.AbstractModel):
    _name='priority.mixin'
    _description='Priority Mixin'

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True, string="Priority")