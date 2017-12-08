# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Job
class FwdrJob(models.Model):
    _name = 'fwdr.job'
    _rec_name = 'job_number'
    _inherit = ['mail.thread']
    _order = 'id desc'

    job_number = fields.Char(string="Job ID")
    transit_type_id = fields.Many2one('fwdr.transit.type', string="Transit Type")
    traffic_mode = fields.Selection([
        ('fcl', 'FCL'),
        ('lcl', 'LCL')],
        default='fcl',
        string="Traffic Mode")
    m_traffic_term_id = fields.Many2one('fwdr.traffic.term', string="Traffic Term")
    ob_traffic_term = fields.Char(default='CY', string="OB Term")
    ib_traffic_term = fields.Char(default='CY', string="IB Term")
    service_contract = fields.Char(string="Service Contract")
    ob_transaction_date = fields.Date(string="Transaction Date") 
    ob_billing_date = fields.Date(string="Billing Date") 

    # party
    ob_office_id = fields.Many2one('res.company', string="OB Office")            
    ib_office_id = fields.Many2one('res.partner', string="IB Office")
    carrier_id = fields.Many2one('fwdr.carrier', string="Carrier")
    executing_carrier_id = fields.Many2one('res.partner', string="Executing Carrier")

    # route
    m_pol_location_id = fields.Many2one('res.partner', string="POL Location", 
        domain="[('port_id', '=', m_load_port_id)]")
    m_pol_contact = fields.Char(string="POL Contact")
    m_pod_location_id = fields.Many2one('res.partner', string="POD Location",
        domain="[('port_id', '=', m_dest_port_id)]")    
    m_pod_contact = fields.Char(string="POD Contact")    
    m_load_port_id = fields.Many2one('fwdr.port', string="Load Port")
    m_dsch_port_id = fields.Many2one('fwdr.port', string="Discharge Port")
    m_dest_port_id = fields.Many2one('fwdr.port', string="Destination Port")
    m_fnd_id = fields.Many2one('res.city', string="Delivery Place")
    m_voyage_id = fields.Many2one('fwdr.vessel.schedule')
    m_voyage = fields.Char(string="Voyage/Flight")    
    m_cutoff = fields.Date(string="Cutoff")
    m_etd = fields.Date(string="ETD")
    m_eta1 = fields.Date(string="ETA")
    m_eta2 = fields.Date(string="ETA")

    # relations
    shipment_ids = fields.One2many('fwdr.shipment', 'job_id', string="Shipment")
    mbl_ids = fields.One2many('fwdr.job.mbl', 'job_id', string="MBL/AMS")
    container_ids = fields.One2many('fwdr.job.container', 'job_id', string="Container")

    # status
    ob_active = fields.Boolean()
    state = fields.Selection([
        ('open','Open'),
        ('compelte','Complete'),
        ('lock','Lock'),
        ('cancel','Cancel')],
        default='open')    
    ob_invoice_count = fields.Integer(string='# Invoices', compute='_ob_invoice_count')
    shipment_count = fields.Integer(string='# Shipments', compute='_shipment_count')
    hbl_count = fields.Integer(string='# House B/L', compute='_hbl_count')

    @api.multi
    def action_create_shipment(self):
        r = self
        ctx = dict(
            default_job_id=r.id, 
            default_h_pol_location_id = r.m_pol_location_id.id,
            default_h_pol_contact = r.m_pol_contact,
            default_h_pod_location_id = r.m_pod_location_id.id,
            default_h_pod_contact = r.m_pod_contact,
            default_h_load_port_id = r.m_load_port_id.id,
            default_h_dsch_port_id = r.m_dsch_port_id.id,
            default_h_dest_port_id = r.m_dest_port_id.id,
            default_h_fnd_id = r.m_fnd_id.id,
            default_h_voyage_id = r.m_voyage_id.id,
            default_h_voyage = r.m_voyage,
            default_h_cutoff = r.m_cutoff,
            default_h_etd = r.m_etd,
            default_h_eta1 = r.m_eta1,
            default_h_eta2 = r.m_eta2,
        )
        return {
            'name': 'New Shipment',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fwdr.shipment',
            'views': [(self.env.ref('fwdr.shipment_form').id, 'form')],
            'view_id': self.env.ref('fwdr.shipment_form').id,
            # 'target': 'new',
            'context': ctx,
        }        


    @api.depends('shipment_ids')    
    def _shipment_count(self):  
        # for r in self:         
        shipments = self.mapped('shipment_ids')
        self.shipment_count = len(shipments)

    @api.multi
    def action_view_shipment(self):
    	# action = {}
    	shipments = self.mapped('shipment_ids')                              
        action = self.env.ref('fwdr.shipment_action').read()[0]
        if len(shipments) > 1:
            action['domain'] = [('id', 'in', shipments.ids)]
        elif len(shipments) == 1:
            action['views'] = [(self.env.ref('fwdr.shipment_form').id, 'form')]
            action['res_id'] = shipments.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
    	return action

    	# if len(shipments) == 1:
        # 	action = {'type': 'ir.actions.act_window',
        #         'res_model': 'fwdr.shipment',
        #         # 'view_mode': 'form',
        #         "views": [(self.env.ref('fwdr.shipment_form').id, 'form')],                
        #         'res_id': shipments.id,
        #         }
        # else:        	
        # 	# shipments = self.env['fwdr.shipment'].search(domain)
        # 	action = {'type': 'ir.actions.act_window',
        #         'res_model': 'fwdr.shipment',                
        #         # 'view_mode': 'tree',
        #         "views": [(self.env.ref('fwdr.shipment_tree').id, 'tree')],
        #         'domain': [('id', 'in', shipments.ids),],                
        #         } 

        # self.ensure_one()
        # return self.env.ref('fwdr.shipment_action')

        #         invoices = self.mapped('invoice_ids')
        # action = self.env.ref('account.action_invoice_tree1').read()[0]
        # if len(invoices) > 1:
        #     action['domain'] = [('id', 'in', invoices.ids)]
        # elif len(invoices) == 1:
        #     action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
        #     action['res_id'] = invoices.ids[0]
        # else:
        #     action = {'type': 'ir.actions.act_window_close'}
        # return action


    @api.depends('shipment_ids')
    def _hbl_count(self):     		        
    	shipments = self.mapped('shipment_ids')    	
        domain = [                
            ('shipment_id', 'in', shipments.ids),
        ]
        hbls = self.env['fwdr.shipment.hbl'].search(domain)
        self.hbl_count = len(hbls)

    @api.multi
    def action_view_hbl(self):
        shipments = self.mapped('shipment_ids')    	
        domain = [                
            ('shipment_id', 'in', shipments.ids),
        ]
        hbls = self.env['fwdr.shipment.hbl'].search(domain)
        action = self.env.ref('fwdr.hbl_action').read()[0]
        if len(hbls) > 1:
            action['domain'] = [('id', 'in', hbls.ids)]
        elif len(hbls) == 1:
            action['views'] = [(self.env.ref('fwdr.hbl_form').id, 'form')]
            action['res_id'] = hbls.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}        
    	return action

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
    def action_view_ob_invoice(self):
        return True


# Inbound Job
class FwdrIbJob(models.Model):
    _name = 'fwdr.ib.job'
    _inherits = {'fwdr.job': 'job_id'}  

    job_id = fields.Many2one('fwdr.job')
    ib_transaction_date = fields.Date(string="Transaction Date") 
    ib_billing_date = fields.Date(string="Billing Date") 
    ib_active = fields.Boolean()    
    
    # customs
    m_custom_entry_number = fields.Char(string="Entry Number")
    m_custom_entry_date = fields.Char(string="Entry Date")    
    m_it_number = fields.Char(string="I.T. Number")
    m_it_place = fields.Char(string="I.T. Place")
    m_it_date = fields.Date(string="I.T. Date")    


# MB/L and AMS of Job
class FwdrJobMbl(models.Model):
    _name = 'fwdr.job.mbl'
    _rec_name = 'mbl_number'

    mbl_number = fields.Char(string="MBL/AMS#")
    bl_type = fields.Selection([
        ('mbl', 'MBL'),
        ('ams', 'AMS')],
        default='mbl',
        string="Type")
    piece_count = fields.Integer(string="Piece Count")    
    job_id = fields.Many2one('fwdr.job', string="Job")


# Containers of Job
class FwdrJobContainer(models.Model):
    _name = 'fwdr.job.container'
    _rec_name = 'container_number'

    container_number = fields.Char(string="Container Number")
    type_id = fields.Many2one('fwdr.container.type', string="Type")
    seal_number = fields.Char(string="Seal Number")
    job_id = fields.Many2one('fwdr.job', string="Job")

