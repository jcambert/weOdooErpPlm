from odoo import models, fields, api
class PlmApproval(models.Model):
    _name="mrp.plm.approval"
    _description="Mrp Plm Validation "
    approval_date=fields.Datetime(string="Date de validation")
    approval_template_id=fields.Many2one('mrp.plm.approval.template',ondelete='cascade',required=True,string="Modèle")
    # display_name=fields.Char(readonly=True,help="Nom affiché")
    eco_id=fields.Many2one('mrp.plm','Technical Change',ondelete='cascade',required=True,help="Modification technique")
    eco_stage_id=fields.Many2one('mrp.plm.stage',string="Étape OMT")
    is_approved=fields.Boolean("Is approved",compute='_compute_is_approved',readonly=True)
    is_closed=fields.Boolean("Is closed",compute='_compute_is_closed',store=True,readonly=True)
    is_rejected=fields.Boolean("Is rejected",compute='_compute_is_rejected',store=True,readonly=True)
    # name=fields.Char(required=True,string="Rôle")
    roles=fields.Many2one('res.users.role',string="Roles")
    roles_names=fields.Char('Roles', compute='_compute_roles_name')
    # required_user_ids=fields.Many2many('res.users',string="Utilisateurs requis")
    status=fields.Selection([
        ('none','not yet'),
        ('comment','Comment'),
        ('approved','Approved'),
        ('rejected','Rejected')],'Statut',required=True)
    template_stage_id=fields.Many2one('mrp.plm.stage',string="Étape de validation")
    user_id=fields.Many2one('res.users','Approuvé par',ondelete='set null')

    @api.model
    def default_get(self, fields):
        defaults = super(PlmApproval, self).default_get(fields)
        defaults['status']='none'
        return defaults
    
    @api.model
    def approve(self):
        if self.is_treated():
            return
        self.status='approved'
        self.approval_date=fields.Datetime.now()
        self.user_id=self.env.user.id
    @api.model
    def reject(self):
        if self.is_treated():
            return
        self.status='rejected'
        self.approval_date=fields.Datetime.now()
        self.user_id=self.env.user.id   
    @api.model
    def is_treated(self):
        return self.status=='approved' or self.status=='rejected' 
    @api.model
    def need_approval(self):
        return self.status!='approved' and self.status!='rejected' 

    @api.depends('status')
    def _compute_is_approved(self):
        for record in self:
            record.is_approved=record.status=='approved'

    @api.depends('status')
    def _compute_is_rejected(self):
        for record in self:
            record.is_rejected= record.status=='rejected'
    def _compute_is_closed(self):
        for record in self:
            record.is_closed= False

    def _compute_roles_name(self):
        for record in self:
            roles=[]
            for role in record.roles:
                roles.append(role.name)
            record.roles_names=','.join(roles)