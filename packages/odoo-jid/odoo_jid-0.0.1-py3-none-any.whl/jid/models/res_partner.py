from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    jid = fields.Char(string='JID')
