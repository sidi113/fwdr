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
    m_dest_port_id = fields.Many2one('fwdr.port', sting="Destination Port")
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
    state = fields.Char()    
    ob_invoice_count = fields.Integer(string='# Invoices', compute='_ob_invoice_count')
    shipment_count = fields.Integer(string='# Shipments', compute='_shipment_count')
    hbl_count = fields.Integer(string='# House B/L', compute='_hbl_count')

    @api.depends('shipment_ids')    
    def _shipment_count(self):  
        for r in self:     
            domain = [
                # ('state', '!=', 'cancelled'),
                ('job_id', 'in', self.ids),
            ]
            shipments = self.env['fwdr.shipment'].search(domain)
            r.shipment_count = len(shipments)

    @api.multi
    def action_view_shipment(self):
        self.ensure_one()
        return self.env.ref('fwdr.shipment_action')

        # {'type': 'ir.actions.act_window',
        #         'res_model': 'fwdr.shipment',
        #         'view_mode': 'tree'
        #         # 'res_id': self.product_tmpl_id.id,
        #         }

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
        for r in self:     
            domain = [
                # ('state', '!=', 'cancelled'),
                ('job_id', 'in', self.ids),
            ]
            shipments = self.env['fwdr.shipment'].search(domain)
            domain1 = [
                # ('state', '!=', 'cancelled'),
                ('shipment_id', 'in', shipments.ids),
            ]
            hbls = self.env['fwdr.shipment.hbl'].search(domain)
            r.hbl_count = len(hbls)

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

