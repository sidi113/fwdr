# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Container Type
class FwdrContainerType(models.Model):
    _description = 'Container Type'
    _name = 'fwdr.container.type'

    name = fields.Char(string="Type", size=4, required=True)
    size = fields.Char(size=2)
    report_type = fields.Char(string="Report Type", size=2)
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


# Vessel
class FwdrVessel(models.Model):
    _description = 'Vessel'
    _name = 'fwdr.vessel'

    name = fields.Char(string="Vessel Name")
    active = fields.Boolean(default=True)


# Vessel Schedule
class FwdrVesselSchedule(models.Model):
    _description = 'Vessel Schedule'
    _name = 'fwdr.vessel.schedule'

    vessel_id = fields.Many2one('fwdr.vessel', string="Vessel")
    voyage = fields.Char()
    port_id = fields.Char(string="Port")
    etd = fields.Date(string="ETD")
    active = fields.Boolean(default=True)


# Carrier
class FwdrCarrier(models.Model):
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


# Customs Status 
class FwdrCustomsStatus(models.Model):
    _description = 'Customs Status'
    _name = 'fwdr.customs.state'

    name = fields.Char(string="Status", translate=True, required=True)
    active = fields.Boolean(default=True)


# SCAC Code 
class FwdrScacCode(models.Model):
    _description = 'SCAC Code'
    _name = 'fwdr.scac.code'

    name = fields.Char(string="SCAC Code", size=4, required=True)
    active = fields.Boolean(default=True)

# Cargo Nature
class FwdrCargoNature(models.Model):
    _description = 'Cargo Nature'
    _name = 'fwdr.cargo.nature'

    code = fields.Char(required=True)
    name = fields.Char(string="Cargo Nature", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)


# Traffic Term
class FwdrTrafficTerm(models.Model):
    _description = 'Traffic Term'
    _name = 'fwdr.traffic.term'

    name = fields.Char(string="Traffic Term", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)


# Traffic Mode
class FwdrTrafficTerm(models.Model):
    _description = 'Traffic Mode'
    _name = 'fwdr.traffic.mode'    

    name = fields.Char(string="Traffic Mode", required=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)


# Transit Type
class FwdrTransitType(models.Model):
    _description = 'Transit Type'
    _name = 'fwdr.transit.type'

    name = fields.Char(string=u'Transit Type', required=True, translate=True)
    seqence = fields.Integer()
    active = fields.Boolean(default=True)