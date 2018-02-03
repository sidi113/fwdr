# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

def print_label(self, partner):
    label = partner.name
    if partner.street:
        label = "%s\n%s" % (label, partner.street)
    if partner.street2:
        label = "%s\n%s" % (label, partner.street2) 
    if partner.city:
        label = "%s\n%s" % (label, partner.city)
    if partner.state_id:
        state = self.env['res.state'].browse(partner.state_id.id).with_context(lang=None).read(['name'])
        label = "%s, %s" % (label, state[0]['name'])                
    if partner.zip:
        label = "%s, %s" % (label, partner.zip)
    if partner.country_id:
        country = self.env['res.country'].browse(partner.country_id.id).with_context(lang=None).read(['name'])
        if partner.state_id:
            label = "%s\n%s" % (label, country[0]['name'])
        else:
            label = "%s, %s" % (label, country[0]['name'])
    return label


class DoorPickup(models.Model):
    _name = 'fwdr.door.pickup'
    
    pickup_address_id = fields.Char()
    pickup_contact = fields.Char()
    pickup_contact_phone = fields.Char()
    pickup_address = fields.Text()
    pickup_remark = fields.Text()
    pickup_time = fields.Datetime()
    pickup_multi_stop = fields.Boolean()
    pickup_vender_id = fields.Many2one('res.partner')


class DoorDelivery(models.Model):
    _name = 'fwdr.door.delivery'
    
    delivery_address_id = fields.Char()
    delivery_contact = fields.Char()
    delivery_contact_phone = fields.Char()
    delivery_address = fields.Text()
    delivery_remark = fields.Text()
    delivery_time = fields.Datetime()
    delivery_multi_stop = fields.Boolean()
    delivery_vender_id = fields.Many2one('res.partner')


class CustomsEntry(models.Model):
    _name = 'fwdr.customs.entry'

    customs_entry_number = fields.Char(string="Entry Number")
    customs_entry_date = fields.Date(string="Entry Date") 
    customs_state_id = fields.Many2one('fwdr.customs.state', string="Entry Status")
    customs_state_date = fields.Date(string="Entry Status Date")   
    it_number = fields.Char(string="I.T. Number")
    it_place = fields.Char(string="I.T. Place")
    it_date = fields.Date(string="I.T. Date")  


class ShippingParty(models.Model):
    _name = 'fwdr.shipping.party'

    @api.model
    def _default_role(self):
        role = {'Booking Party', 'Consignee', 'Notify'}
        parties = self.mapped('shipment_id.shipping_party_ids.role.name')
        for r in role:
            if r not in parties:
                return self.env['res.partner.category'].search([('name','=',r)]).id
            else:
                return self.env['res.partner.category'].search([('name','=','Billing Party')]).id
        # if self._context.get('shipment_role'):
        #     if 'Booking Party' not in parties:
        #         role = 'Booking Party'
        #     elif 'Consignee' not in parties:
        #         role = 'Consignee'
        #     elif 'Notify' not in parties: 
        #         role = 'Notify'  
        #     else:
        #         role = 'Billing Party'
        

    @api.model      
    def _get_role_list(self):
        domain = []
        parties = self.mapped('shipment_id.shipping_party_ids.role.name')
        if self._context.get('shipment_role'):
            domain = ['&', 
                ('name','not in', parties), 
                ('name','<>','Shipper'), 
                ('shipment_role','=',True)
                ]
        return domain
     
    name = fields.Char(related='partner_id.name', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    role = fields.Many2one('res.partner.category', domain=_get_role_list, default=_default_role )
    address = fields.Text()
    contact = fields.Char()
    shipment_id = fields.Many2one('fwdr.shipment')
    job_id = fields.Many2one('fwdr.job', related='shipment_id.job_id', store=True)


class Shipment(models.Model):
    _name = 'fwdr.shipment'
    _rec_name = 'shipment_number'
    _inherit = ['mail.thread']
    _inherits = {
        'fwdr.job': 'job_id',
        'fwdr.door.pickup': 'door_pickup_id',
        'fwdr.door.delivery': 'door_delivery_id',
        'fwdr.customs.entry': 'customs_entry_id',
    }     

    shipment_number = fields.Char(string="Shipment ID", required=True, copy=False, readonly=True, default=lambda self: _('New'))  
    h_traffic_term_id = fields.Many2one('fwdr.traffic.term', string="Traffic Term")
    h_traffic_mode_id = fields.Many2one('fwdr.traffic.mode', string="Traffic Mode")
    
    # Door Halugage
    door_pickup = fields.Boolean(string="Door Pickup")
    door_pickup_id = fields.Many2one('fwdr.door.pickup')
    door_delivery = fields.Boolean(string="Door Delivery")
    door_delivery_id = fields.Many2one('fwdr.door.delivery')      

    # Customs
    customs_entry_id = fields.Many2one('fwdr.customs.entry')

    # Shipment route
    h_por_id = fields.Many2one('res.city', string="Pickup Place")
    # h_pol_location_id = fields.Many2one('res.partner', string="POL Location", 
        # domain="[('port_id', '=', m_load_port_id)]")
    # h_pol_contact = fields.Char(string="POL Contact")
    h_pod_location_id = fields.Many2one('res.partner', string="POD Location",
        domain="[('port_id', '=', m_dest_port_id)]")  
    h_pod_contact = fields.Char(string="POD Contact")    
    # h_load_port_id = fields.Many2one('fwdr.port', string="Load Port")
    # h_dsch_port_id = fields.Many2one('fwdr.port', string="Discharge Port")
    h_dest_port_id = fields.Many2one('fwdr.port', string="Destination Port")
    h_fnd_id = fields.Many2one('res.city', string="Delivery Place")
    # h_voyage_id = fields.Many2one('fwdr.vessel.schedule')
    # h_voyage = fields.Char(string="Voyage/Flight")
    # h_cutoff = fields.Date(string="Cutoff")
    # h_etd = fields.Date(string="ETD")
    h_eta1 = fields.Date(string="ETA")
    h_eta2 = fields.Date(string="ETA")
 


    # Shipping Party
    shipping_party_ids = fields.One2many('fwdr.shipping.party', 'shipment_id', string="Shipping Party")
    booking_party_id = fields.Many2one('res.partner', string="Booking Party")
    s_shipper_id = fields.Many2one('res.partner', string="Shipper")
    s_shipper = fields.Char(string="Shipper")
    consignee_id = fields.Many2one('res.partner', string="Consignee")
    consignee_label = fields.Text()    
    notify_id = fields.Many2one('res.partner', string="Notify")
    notify_label = fields.Text()
    agent_label = fields.Text()
    billing_party_id = fields.Many2one('res.partner', string="Billing Party")
    sales_id = fields.Many2one('res.users', string="Sales")   

    active = fields.Boolean(default=True)       
    state = fields.Selection([
        ('open','Open'),
        ('ib_start','I/B Start'),
        ('cancel','Cancelled')],
        default='open', string="Status")

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
    # state = fields.Char(string="Status")
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
    job_id = fields.Many2one('fwdr.job', string="Job ID", ondelete='cascade')
    hbl_ids = fields.One2many('fwdr.shipment.hbl', 'shipment_id', string="House B/L")  
    shipment_item_ids = fields.One2many('fwdr.shipment.item', 'shipment_id', string="Shipment Item")  
    invoice_ids = fields.Many2many('account.invoice', string='Invoices', compute="_get_invoiced", readonly=True, copy=False)

    # order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    @api.model
    def create(self, vals):            
        if vals.get('shipment_number', 'New') == 'New':
            vals['shipment_number'] = self.env['ir.sequence'].next_by_code('shipment.number') or '/'
            if self._context.get('multi_shmt') :
                vals['job_id'] = self._context.get('job_id')
                return super(Shipment, self).create(vals)
            else:
                if vals.get('job_number', 'New') == 'New':
                    vals['job_number'] = self.env['ir.sequence'].next_by_code('job.number') or '/'
        return super(Shipment, self).create(vals)

    @api.onchange('consignee_id')
    def onchange_consignee_id(self):
        partner = self.mapped('consignee_id')
        label = ''
        if partner.print_label:
            label = partner.print_label
        else:
            if partner:
                label = print_label(self, partner)           
        self.consignee_label = label 

    @api.onchange('notify_id')
    def onchange_notify_id(self):
        partner = self.mapped('notify_id')
        label = ''
        if partner.print_label:
            label = partner.print_label
        else:        
            if partner:
                label = print_label(self, partner)           
        self.notify_label = label 

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

    @api.multi
    def action_cancel_shipment(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_reactive_shipment(self):
        self.write({'state': 'open'})

    @api.multi
    def action_multi_shipment(self):
        r = self
        ctx = dict(
            default_job_id=r.job_id.id, 
            job_id = r.job_id.id,
            multi_shmt = 1,
        )
        return {
            'name': 'New Shipment',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fwdr.shipment',
            'views': [(self.env.ref('fwdr.view_shipment_form2').id, 'form')],
            'view_id': self.env.ref('fwdr.view_shipment_form2').id,
            # 'target': 'new',
            'context': ctx,
        } 


# House B/L
class FwdrShipmentHbl(models.Model):
    _name = 'fwdr.shipment.hbl'
    _rec_name = 'hbl_number'
    _inherits = {'fwdr.shipment': 'shipment_id'}
    _inherit = ['mail.thread']

    hbl_number = fields.Char()
    shipment_id = fields.Many2one('fwdr.shipment', string="Shipment", ondelete='restrict')
    h_shipper_id = fields.Many2one('res.partner', string="Shipper")
    shipper = fields.Text()
    # h_consignee_id = fields.Many2one('res.partner', string="Consignee")
    # consignee = fields.Text()
    # h_notify_id = fields.Many2one('res.partner', string="Notify")
    # notify = fields.Text()

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


class ShipmentItem(models.Model):
    _name = 'fwdr.shipment.item'
    _rec_name = 'house_bl_number'
    _inherits = {'fwdr.shipment': 'shipment_id'}

    house_bl_number = fields.Char()
    shipper_id = fields.Many2one('res.partner', string="Shipper")
    shipper_label = fields.Text(string="Shipper")
    gross_wt = fields.Float()
    gross_wt_unit_id = fields.Many2one('product.uom')
    volume = fields.Float()
    quantity = fields.Integer()
    package_type_id = fields.Many2one('product.uom')
    shipment_id = fields.Many2one('fwdr.shipment')
    job_id = fields.Many2one('fwdr.job', related='shipment_id.job_id', store=True)
    # shipper_id = fields.Many2one('fwdr.shipping.party')
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('release', 'Released'),
        ('telex', 'Telex Released'),
        ('receive','Received')])

    @api.onchange('shipper_id')
    def onchange_shipper_id(self):
        partner = self.mapped('shipper_id')
        label = ''
        if partner.print_label:
            label = partner.print_label
        else:        
            if partner:
                label = print_label(self, partner)           
        self.shipper_label = label 