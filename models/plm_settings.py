from odoo import api, fields, models
class PlmConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    can_go_back = fields.Boolean('can go back',default=False)

    def set_values(self):
        res=super(PlmConfigSettings, self).set_values()
        fn=self.env['ir.config_parameter'].set_param
        fn('weOdooErpPlm.can_go_back',self.can_go_back)
        return res
    @api.model
    def get_values(self):
        res = super(PlmConfigSettings, self).get_values()
        fn = self.env['ir.config_parameter'].sudo().get_param
        can_go_back=fn('weOdooErpPlm.can_go_back')
        res.update({'can_go_back':can_go_back})
        return res