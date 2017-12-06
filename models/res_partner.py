# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):    
    _name = 'res.partner'
    _inherit = 'res.partner'

    port_id = fields.Many2one('fwdr.port', string="Port")










