# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContainerType(models.Model):
    _description = 'Container Type'
    _name = 'fwdr.container.type'

    name = fields.Char(string="Type", size=4, required=True)
    size = fields.Char(size=2)
    report_type = fields.Char(string="Report Type", size=2, select=True)
    description = fields.Char(translate=True)
    is_reefer = fields.Boolean(string="Reefer")
    teu = fields.Integer(string="TEU")
    ext_dimensions = fields.Char(string="External Dimensions")
    int_dimensions = fields.Char(string="Internal Dimensions")
    max_volume = fields.Char(string="Max Volume")
    tare_weight = fields.Char(string="Tare Weight")    
    max_gross_weight = fields.Char(string="Max Gross Weight")
    net_load_wheight = fields.Char(string="Net Load Weight")
    active = fields.Boolean(default=True)


class Vessel(models.Model):
    _description = 'Vessel'
    _name = 'fwdr.vessel'

    name = fields.Char(string=u"Vessel Name", required=True)
    active = fields.Boolean(default=True)

class VesselSchedule(models.Model):
    _description = 'Vessel Schedule'
    _name = 'fwdr.vessel.schedule'

    vessel_id = fields.Many2one('fwdr.vessel', string="Vessel")
    voyage = fields.Char()
    port_id = fields.Char(string="Port")
    etd = fields.Date(string="ETD")
    active = fields.Boolean(default=True)

class Carrier(models.Model):
    _name = 'fwdr.carrier'

    name = fields.Char(string="Carrier", required=True, translate=True)
    short_name = fields.Char(string="Short Name")
    iata_code = fields.Char(string="IATA Code", help="IATA Code for airlines.")
    bl_prefix = fields.Char(string="B/L Prefix")
    category = fields.Selection([
        ('air', 'Airline'),
        ('sea', 'Line')])
    country_id = fields.Many2one('res.country', string='Country')
    remark = fields.Text()
    active = fields.Boolean(default=True)

class CustomsStatus(models.Model):
    _description = 'Customs Status'
    _name = 'fwdr.customs.state'

    name = fields.Char(string=u"Customs Status", translate=True, required=True)
    active = fields.Boolean(default=True)

class ReferenceType(models.Model):
    _description = 'Reference Type'
    _name = 'fwdr.reference.type'

    name = fields.Char(string=u"Type", translate=True, required=True)
    active = fields.Boolean(default=True)

class ScacCode(models.Model):
    _description = 'SCAC Code'
    _name = 'fwdr.scac.code'

    name = fields.Char(string="SCAC Code", size=4, required=True)
    carrier_id = fields.Many2one('res.partner', string="Carrier")
    active = fields.Boolean(default=True)

class CargoNature(models.Model):
    _description = 'Cargo Nature'
    _name = 'fwdr.cargo.nature'

    code = fields.Char(required=True)
    name = fields.Char(string="Cargo Nature", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)

class TrafficTerm(models.Model):
    _description = 'Traffic Term'
    _name = 'fwdr.traffic.term'

    name = fields.Char(string=u"Traffic Term", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)

class TrafficMode(models.Model):
    _description = 'Traffic Mode'
    _name = 'fwdr.traffic.mode'    

    name = fields.Char(string=u"Traffic Mode", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)

class TransitType(models.Model):
    _description = 'Transit Type'
    _name = 'fwdr.transit.type'

    name = fields.Char(string=u'Transit Type', required=True, translate=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)


class TransitCategory(models.Model):
    _description = 'Transit Category'
    _name = 'fwdr.transit.category'
    _order = 'parent_left, name'
    _parent_store = True
    _parent_order = 'name'

    name = fields.Char(string='Transit Category', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('fwdr.transit.category', string='Parent Category', index=True, ondelete='cascade')
    child_ids = fields.One2many('fwdr.transit.category', 'parent_id', string='Child Category')
    active = fields.Boolean(default=True, help="The active field allows you to hide the transit category without removing it.")
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You can not create recursive type.'))

    @api.multi
    def name_get(self):
        """ Return the type' display name, including their direct
            parent by default.

            If ``context['partner_ctype_display']`` is ``'short'``, the short
            version of the category name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('transit_category_display') == 'short':
            return super(TransitCategory, self).name_get()

        res = []
        for transit_category in self:
            names = []
            current = transit_category
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((transit_category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()


class ProductUoM(models.Model):
    _name = 'product.uom'
    _description = 'Product Unit of Measure'   
    _inherit = 'product.uom' 


class ProductUoMCategory(models.Model):
    _name = 'product.uom.categ'
    _description = 'Product UoM Categories'
    _inherit = 'product.uom.categ' 