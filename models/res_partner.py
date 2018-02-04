# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):    
    _name = 'res.partner'
    _inherit = 'res.partner'

    port_id = fields.Many2one('fwdr.port', string="Port")
    print_label = fields.Text(string="Print Label")
    alias = fields.Char()


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = 'res.partner.category'  
    
    shipment_role = fields.Boolean()  
    seqence = fields.Integer()


class PartnerTitle(models.Model):
    _name = 'res.partner.title'
    _inherit = 'res.partner.title' 

