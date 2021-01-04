from odoo import models, fields, api
class PlmApproval(models.Model):
    _name="mrp.plm.approval"
    _description="Mrp Plm Validation "
    approval_date=fields.Datetime(string="Date de validation")
    approval_template_id=fields.Many2one('mrp.plm.approval.template',ondelete='cascade',required=True,string="Modèle")
    display_name=fields.Char(readonly=True,help="Nom affiché")
    eco_id=fields.Many2one('mrp.plm','Technical Change',ondelete='cascade',required=True,help="Modification technique")
    eco_stage_id=fields.Many2one('mrp.plm.stage',string="Étape OMT")
    is_approved=fields.Boolean(readonly=True,string="Est approuvé")
    is_closed=fields.Boolean(readonly=True,string="Est Fermé")
    is_rejected=fields.Boolean(readonly=True,string="Est refusé")
    name=fields.Char(required=True,string="Rôle")
    required_user_ids=fields.Many2many('res.users',string="Utilisateurs requis")
    status=fields.Selection([
        ('none','not yet'),
        ('comment','Comment'),
        ('approved','Approved'),
        ('rejected','Rejected')],'Statut',required=True)
    template_stage_id=fields.Many2one('mrp.plm.stage',string="Étape de validation")
    user_id=fields.Many2one('res.users','Approuvé par',ondelete='set null')