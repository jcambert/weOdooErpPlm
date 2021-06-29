from odoo import  fields, models
class PlmConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    can_go_back = fields.Boolean('can go back',config_parameter="plm.can_go_back",default=False)

