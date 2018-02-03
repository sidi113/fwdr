# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CountryState(models.Model):    
    _name = 'res.country.state'
    _inherit = 'res.country.state'

    name = fields.Char(translate=True)


class County(models.Model):
    _description = "County"
    _name = 'res.county'    

    name = fields.Char(required=True, translate=True)
    country_id = fields.Many2one('res.country', string="Country", required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', domain="[('country_id', '=', country_id)]")
    active = fields.Boolean()


class City(models.Model):
    _name = 'res.city'
    _description = 'City'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    zipcode = fields.Char(string="Zip")
    country_id = fields.Many2one('res.country', string="Country", required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', domain="[('country_id', '=', country_id)]")
    county_id = fields.Many2one(
        'res.county', 'County', domain="[('state_id', '=', state_id)]")
    unlocode = fields.Char(size=5)
    active = fields.Boolean()

    @api.multi
    def name_get(self):
        res = []
        for city in self:
            name = city.name
            if self._context.get('show_full_name'):
                if city.state_id:
                    name += ',' + city.state_id.name
                name += ',' + city.country_id.name                
            res.append((city.id, name)) 
        return res

    @api.model  
    def name_search(self,name='',args=None,operator='ilike',limit=100):  
        args = args or []  
        domain = []  
        if name:  
            domain = ['|',
                ('name',operator,name),
                ('unlocode',operator,name)]  
        pos = self.search(domain + args,limit=limit)  
        return pos.name_get()  

class Port(models.Model):
    _description = "Port"
    _name = 'fwdr.port' 

    name = fields.Char(required=True, translate=True)
    city_id = fields.Many2one('res.city', string=u"City") 
    state_id = fields.Many2one('res.country.state', string=u"State") 
    country_id = fields.Many2one('res.country', string=u"Country")
    code = fields.Char(size=3, required=True)
    category = fields.Selection([
        ('air', 'Airport'),
        ('sea', 'Seaport')])
    active = fields.Boolean(default=True)
    terminal_ids = fields.One2many('res.partner', 'port_id', string=u"Terminal")

    @api.multi
    def name_get(self):
        if not self._context.get('show_full_name'):
            return super(Port, self).name_get()

        res = []
        if self._context.get('show_full_name'):
            for port in self:
                name = port.name            
                if port.state_id:
                    name += ',' + port.state_id.name
                name += ',' + port.country_id.name
                res.append((port.id, name)) 
        return res

    @api.model  
    def name_search(self,name='',args=None,operator='ilike',limit=100):  
        args = args or []  
        domain = []  
        if name:  
            domain = ['|',
                ('name',operator,name),
                ('code',operator,name)]  
        pos = self.search(domain + args,limit=limit)  
        return pos.name_get()  

# class FmsLocation(models.Model):
#     _name = 'fms.location'

#     name = fields.Char('City', required=True)
#     local_name = fields.Char(translate=True)
#     full_name = fields.Char(compute='_compute_full_name')
#     unlocode = fields.Char(string="UNLoCode")
#     iata_code = fields.Char(string="IATA Code")
#     county_id = fields.Many2one('fms.county', string='County')
#     state_id = fields.Many2one(
#         'res.country.state',
#         string='State')
#     country_id = fields.Many2one(
#         'res.country',
#         related='state_id.country_id',
#         string='Country',        
#         context="{'lang':'en_US'}",
#         store=True,
#         required=True)
#     remark = fields.Text()
#     is_port = fields.Boolean()
#     is_air_port = fields.Boolean()

#     # _sql_constraints = [
#     #     ('name_uniq', 'unique(country_id, state_id, county, name)')
#     # ]  

#     def name_get(self):
#         r = []
#         # for r in self:
#         #     r.append((r.id, u"%s (%s)" % (r.code, r.name)))
#         return [(r.id, u"%s (%s)" % (r.full_name, r.unlocode)) for r in self]

#     @api.depends('name', 'state_id')
#     def _compute_full_name(self): 
#         # records = self.with_context({'lang':'en_US'})       
#         for rec in self:
#             if rec.state_id:
#                 rec.full_name = rec.name + ', ' + rec.state_id.name + ', ' + rec.country_id.en_name



# class Country(models.Model):
#     _name = 'res.country'
#     _inherit = 'res.country'

#     loc_name = fields.Char(compute='_compute_loc_name', string='Local Name')
#     en_name = fields.Char(compute='_compute_en_name')

#     @api.multi
#     def _compute_en_name(self):
#         for rec in self:
#             result = self.env['res.country'].browse(rec.id).with_context(lang=None).read(['name'])
#             rec.en_name = result[0]['name'] if result else False

#     @api.multi
#     def _compute_loc_name(self):
#     	lang = self.env.user.lang
#     	for rec in self:
#             result = self.env['res.country'].browse(rec.id).with_context(lang=lang).read(['name'])
#             rec.loc_name = result[0]['name'] if result else False








