# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Shipment
class FwdrShipment(models.Model):
    _name = 'fwdr.shipment'
    _rec_name = 'shipment_number'
    _inherits = {'fwdr.job': 'job_id'}     

    shipment_number = fields.Char()  
    h_traffic_term_id = fields.Many2one('fwdr.traffic.term', string="Traffic Term")
    h_traffic_mode_id = fields.Many2one('fwdr.traffic.mode', string="Traffic Mode")
    door_pickup = fields.Boolean(string="Door Pickup")
    door_delivery = fields.Boolean(string="Door Delivery")    

    # Shipment route
    h_por_id = fields.Many2one('res.city', string="Pickup Place")
    h_pol_location_id = fields.Char(string="POL Location")
    h_pol_contact = fields.Char(string="POL Contact")
    h_pod_location_id = fields.Char(string="POD Location")
    h_pod_contact = fields.Char(string="POD Contact")    
    h_load_port_id = fields.Many2one('fwdr.port', string="Load Port")
    h_dsch_port_id = fields.Many2one('fwdr.port', string="Discharge Port")
    h_dest_port_id = fields.Many2one('fwdr.port', sting="Destination Port")
    h_fnd_id = fields.Many2one('res.city', string="Delivery Place")
    h_voyage_id = fields.Many2one('fwdr.vessel.schedule')
    h_voyage = fields.Char(string="Voyage/Flight")
    h_cutoff = fields.Date(string="Cutoff")
    h_etd = fields.Date(string="ETD")
    h_eta1 = fields.Date(string="ETA")
    h_eta2 = fields.Date(string="ETA")
 
    # customs
    h_custom_entry_number = fields.Char(string="Entry Number")
    h_custom_entry_date = fields.Char(string="Entry Date") 
    h_customs_state_id = fields.Many2one('fwdr.customs.state', string="Entry Status")
    h_customs_state_date = fields.Date(string="Entry Status Date")   
    h_it_number = fields.Char(string="I.T. Number")
    h_it_place = fields.Char(string="I.T. Place")
    h_it_date = fields.Date(string="I.T. Date")  

    # Partner
    booking_party_id = fields.Many2one('res.partner', string="Booking Party", required=True)
    s_shipper_id = fields.Many2one('res.partner', string="Shipper")
    s_consignee_id = fields.Many2one('res.partner', string="Consignee")
    s_notify_id = fields.Many2one('res.partner', string="Notify")
    billing_party_id = fields.Many2one('res.partner', string="Billing Party")
    sales_id = fields.Many2one('res.users', string="Sales")    
    
    # Shipment Note
    payment_term = fields.Selection([
        ('pp', 'Prepaid'),
        ('cc', 'Collect')],
        default='pp',
        string="Payment Term")    
    bl_type = fields.Selection([
        ('hbl', 'House B/L'),
        ('mbl', 'Master B/L')],
        default='hbl',
        string="B/L Type") 
    bl_issue_method = fields.Selection([
        ('telex', 'Telex'),
        ('obl', 'Original')],
        default='obl',
        string="B/L Issue Method") 
    shipment_note = fields.Text(string="Shipment Note")

    # status
    state = fields.Char(string="Status")
    ob_invoice_state = fields.Selection([
        ('full', 'Fully'),
        ('partial', 'Partial'),
        ('unbilled', 'Unbilled'),
        ('no', 'No Freight')], 
        string="Invoice Status", 
        readonly=True)
        # ], string='Invoice Status', compute='_get_invoiced', store=True, readonly=True)
    ib_invoice_state = fields.Selection([
        ('full', 'Fully'),
        ('partial', 'Partial'),
        ('unbilled', 'Unbilled'),
        ('no', 'No Freight')], 
        string="Invoice Status", 
        readonly=True)
        # ], string='Invoice Status', compute='_get_invoiced', store=True, readonly=True)
    hbl_count = fields.Integer(string='# of HB/L', compute='_get_hbl', readonly=True)
    mbl_count = fields.Integer(string='# of MB/L', compute='_get_mbl', readonly=True)
    invoice_count = fields.Integer(string='# of Invoices', compute='_get_invoiced', readonly=True)    

    # Cargo Summary
    gross_wheight = fields.Float()
    gross_wt_unit_id = fields.Many2one('product.uom')
    chargeable_weight = fields.Float()
    chargeable_wt_unit_id = fields.Many2one('product.uom')
    declared_value = fields.Float()
    insurance_required = fields.Boolean()
    insurance_amount = fields.Float()

    # relation
    job_id = fields.Many2one('fwdr.job', string="Job ID")
    hbl_ids = fields.One2many('fwdr.shipment.hbl', 'shipment_id', string="House B/L")    
    invoice_ids = fields.Many2many('account.invoice', string='Invoices', compute="_get_invoiced", readonly=True, copy=False)

    # order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)


    @api.depends('state')
    def _get_hbl(self):
        return True

    @api.multi
    def action_view_hbl(self):
        return True

    @api.depends('state')
    def _get_mbl(self):
        return True

    @api.multi
    def action_view_mbl(self):
        return True

    @api.depends('state')
    def _get_invoiced(self):
        return True

    @api.multi
    def action_view_invoice(self):
        return True


# House B/L
class FwdrShipmentHbl(models.Model):
    _name = 'fwdr.shipment.hbl'
    _rec_name = 'hbl_number'
    _inherits = {'fwdr.shipment': 'shipment_id'}

    hbl_number = fields.Char()
    shipment_id = fields.Many2one('fwdr.shipment', string="Shipment")
    h_shipper_id = fields.Many2one('res.partner', string="Shipper")
    shipper = fields.Text()
    h_consignee_id = fields.Many2one('res.partner', string="Consignee")
    consignee = fields.Text()
    h_notify_id = fields.Many2one('res.partner', string="Notify")
    notify = fields.Text()

    load_port = fields.Char(string="Load Port")
    dsch_port = fields.Char(string="Discharge Port")
    dest_port = fields.Char(sting="Destination Port")
    fnd = fields.Char(string="Delivery Place")    

    # Cargo Summary
    hbl_gross_wt = fields.Float()
    hbl_gross_wt_unit_id = fields.Many2one('product.uom')
    hbl_volume = fields.Float()
    hbl_quantity = fields.Integer()
    hbl_package_type = fields.Many2one('product.uom')
    chargeable_wt = fields.Float()
    chargeable_wt_unit_id = fields.Many2one('product.uom')
    declared_value = fields.Float()
    insurance_required = fields.Boolean()
    insurance_amount = fields.Float()
    bl_release_type = fields.Char()
    bl_release_date = fields.Date() 
    po_number = fields.Char()
    declared_value = fields.Float()
    marks = fields.Text()
    full_description = fields.Text()
    brief_description = fields.Char()
    bl_remark = fields.Text()