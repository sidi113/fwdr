# -*- coding: utf-8 -*-
from lxml import etree
from odoo import models, fields, api, _

def unit_to_word(u):
    convert_table = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE",
    }
    return convert_table[u]

def tens_to_word(t):
    convert_table = {
    0: "",
    10: "TEN",
    11: "ELEVEN",
    12: "TWELVE",
    13: "THIRTEEN",
    14: "FOURTEEN",
    15: "FIFTEEN",
    16: "SIXTEEN",
    17: "SEVENTEEN",
    18: "EIGHTEEN",
    19: "NINETEEN",
    2: "TWENTY",
    3: "THIRTY",
    4: "FORTY",
    5: "FIFTY",
    6: "SIXTY",
    7: "SEVENTY",
    8: "EIGHTY",
    9: "NINETY",
    }
    if 9 < t < 20:
        return convert_table[t]
    else:
        tens = convert_table[t/10] + " " + unit_to_word(t%10)
        return tens

def hundreds_to_word(h):
    if h > 99:
        word = unit_to_word(h/100) + " HUNDRED"
        tens = h % 100
        if tens == 0:
            return word
        else:
            return word + " AND " + tens_to_word(tens)
    else:
        return tens_to_word(h)

# Job
class FwdrJob(models.Model):
    _name = 'fwdr.job'
    _rec_name = 'job_number'
    # _inherit = ['mail.thread']
    # _inherits = {'fwdr.shipment': 'master_shipment_id'}
    _order = 'id desc'

    @api.model
    def _default_ob_office(self):
        if self.env.context.get('ob'):
            return self.env.user.company_id   
        else:
            return False     

    @api.model
    def _default_ib_office(self):
        if self.env.context.get('ib'):
            return self.env.user.company_id
        else:
            return False  

    job_number = fields.Char(string="Job ID", required=True, readonly=True, copy=False, default=lambda self: _('New'))
    master_shipment_id = fields.Many2one('fwdr.shipment', string="Shipment #")
    transit_type_id = fields.Many2one('fwdr.transit.type', string="Transit Type")
    # transit_type = fields.Many2one('fwdr.tansit.category', string="Transit Type")
    traffic_mode = fields.Selection([
        ('fcl','FCL'),
        ('lcl','LCL'),
        ('colo','CO-LO'),
        ('air','Air')],
        default='fcl',
        string="Traffic Mode")
    m_traffic_term_id = fields.Many2one('fwdr.traffic.term', string="Traffic Term")
    # ob_traffic_term = fields.Char(default='CY', string="OB Term")
    # ib_traffic_term = fields.Char(default='CY', string="IB Term")
    # service_contract = fields.Char(string="Service Contract")
    ob_transaction_date = fields.Date(string="Transaction Date") 
    ob_billing_date = fields.Date(string="Billing Date") 
    ib_transaction_date = fields.Date(string="Transaction Date") 
    ib_billing_date = fields.Date(string="Billing Date") 

    # party
    ob_office_id = fields.Many2one('res.partner', string="OB Office", default=_default_ob_office)            
    ib_office_id = fields.Many2one('res.partner', string="IB Office", default=_default_ib_office)
    carrier_id = fields.Many2one('fwdr.carrier', string="Carrier")
    # executing_carrier_id = fields.Many2one('res.partner', string="Executing Carrier")

    # route
    pol_location_id = fields.Many2one('fwdr.terminal', string="POL Location", 
        domain="[('port_id', '=', load_port_id)]")
    pol_contact = fields.Char(string="POL Contact")
    m_pod_location_id = fields.Many2one('fwdr.terminal', string="POD Location",
        domain="[('port_id', '=', m_dest_port_id)]")    
    m_pod_contact = fields.Char(string="POD Contact")    
    load_port_id = fields.Many2one('fwdr.port', string="Load Port")
    dsch_port_id = fields.Many2one('fwdr.port', string="Discharge Port")
    m_dest_port_id = fields.Many2one('fwdr.port', string="Destination Port")
    m_fnd_id = fields.Many2one('res.city', string="Delivery Place")
    voyage_id = fields.Many2one('fwdr.vessel.schedule')
    voyage = fields.Char(string="Voyage/Flight")    
    cutoff = fields.Date(string="Cutoff")
    etd = fields.Date(string="ETD")
    m_eta1 = fields.Date(string="ETA")
    m_eta2 = fields.Date(string="ETA")

    # relations
    shipment_ids = fields.One2many('fwdr.shipment', 'job_id', string="Shipment")
    shipment_item_ids = fields.One2many('fwdr.shipment.item', 'job_id', string="Shipment Item")
    mbl_ids = fields.One2many('fwdr.job.mbl', 'job_id', string="MBL/AMS")
    shipping_party_ids = fields.One2many('fwdr.shipping.party', 'job_id', string="Shipping Party")

    # container
    container_ids = fields.One2many('fwdr.job.container', 'job_id', string="Container")
    container_units = fields.Integer(string="Units", readonly=True, compute='_container_compute', store=True)
    container_teus = fields.Integer(string="TEUs", readonly=True, compute='_container_compute', store=True)
    container_summary = fields.Char(string="Containers", readonly=True, compute='_container_compute')
    cargo_summary = fields.Char(string="Cargo", readonly=True, compute='_container_compute')

    # status
    # ob_active = fields.Boolean()
    ob_state = fields.Selection([
        ('open','Open'),
        ('compelte','Completed'),        
        ('lock','Locked'),
        ('cancel','Cancelled')],        
        string="Status")  
    ib_state = fields.Selection([
        ('open','Open'),
        ('compelte','Completed'),
        ('lock','Locked'),
        ('cancel','Cancelled')],        
        string="Status")  
    state = fields.Selection([
        ('draft','Draft'),
        ('open','Open'),
        ('ib_start','I/B Start'),
        ('compelte','Completed'),
        ('lock','Locked'),
        ('cancel','Cancelled')],
        default='open',
        string="Status")  
    active = fields.Boolean(default=True)    
    ib_start_uid = fields.Many2one('res.user', string="I/B Start User")
    ib_start = fields.Boolean()
    ob_invoice_count = fields.Integer(string='# Invoices')
    shipment_count = fields.Integer(string='# Shipments', compute='_shipment_count')
    multi_shmt = fields.Boolean(compute='_shipment_count', string="Multi Shipments", store=True)
    hbl_count = fields.Integer(string='# House B/L', compute='_hbl_count')
    # is_ib_office = fields.Boolean(compute='_get_cu')

    # @api.model
    # def create(self, vals):
    #     if self._context.get('multi_shmt'):
    #         return super(FwdrJob, self).create(vals)
    #     else:
    #         if vals.get('job_number', 'New') == 'New':
    #             vals['job_number'] = self.env['ir.sequence'].next_by_code('job.number') or '/'
    #         return super(FwdrJob, self).create(vals)

    @api.depends('container_ids')
    def _container_compute(self):
        teus = 0
        cntr_sum = ''
        cntrs = self.mapped('container_ids')
        contr_count = len(cntrs)
        self.container_units = contr_count

        if contr_count > 0:
            self.cargo_summary = "SAY" + hundreds_to_word(contr_count) + " CONTAINER"
            if contr_count > 1:
                self.cargo_summary = self.cargo_summary + "S"
        
        for cntr in cntrs:
            teus += cntr.type_id.teu
        self.container_teus = teus

        cntrs =cntrs.sorted(lambda r: r.type_id.name)
        for cntr_type in cntrs.mapped('type_id'):
            cntr_sum += '%dx%s ' % (len(self.container_ids.filtered(lambda r: r.type_id.id == cntr_type.id)), cntr_type.name)
        self.container_summary = cntr_sum


    @api.multi
    def action_create_shipment(self):
        r = self
        ctx = dict(
            default_job_id=r.id, 
            # default_h_pol_location_id = r.m_pol_location_id.id,
            # default_h_pol_contact = r.m_pol_contact,
            default_h_pod_location_id = r.m_pod_location_id.id,
            default_h_pod_contact = r.m_pod_contact,
            # default_h_load_port_id = r.m_load_port_id.id,
            # default_h_dsch_port_id = r.m_dsch_port_id.id,
            default_h_dest_port_id = r.m_dest_port_id.id,
            default_h_fnd_id = r.m_fnd_id.id,
            # default_h_voyage_id = r.m_voyage_id.id,
            # default_h_voyage = r.m_voyage,
            # default_h_cutoff = r.m_cutoff,
            # default_h_etd = r.m_etd,
            default_h_eta1 = r.m_eta1,
            default_h_eta2 = r.m_eta2,
        )
        return {
            'name': 'New Shipment',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fwdr.shipment',
            'views': [(self.env.ref('fwdr.view_shipment_form').id, 'form')],
            'view_id': self.env.ref('fwdr.view_shipment_form').id,
            # 'target': 'new',
            'context': ctx,
        }        

    # @api.onchange('shipment_ids')
    # def onchange_shipment():
    #     shipments = self.mapped('shipment_ids')
    #     if self.state!='cancel':
    #         if len(shipments)==0:
    #             self.state = 'draft'
    #         else
    #             self.state = 'open'

    @api.depends('shipment_ids')    
    def _shipment_count(self):  
        count = len(self.shipment_ids.filtered(lambda r: r.state != 'cancel')) 
        self.shipment_count = count
        if count > 1:
           self.multi_shmt = True      
        else:
           self.multi_shmt = False      

    @api.multi
    def action_view_shipment(self):
    	# action = {}
    	shipments = self.mapped('shipment_ids')                              
        action = self.env.ref('fwdr.action_shipment').read()[0]
        if len(shipments) > 1:
            action['domain'] = [('id', 'in', shipments.ids)]
        elif len(shipments) == 1:
            action['views'] = [(self.env.ref('fwdr.view_shipment_form').id, 'form')]
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

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        # for shmt in self.mapped('shipment_ids'):
        #     shmt.active = False
        # for hbl in self.mapped('shipment_ids.hbl_ids'):
        #     hbl.active = False

    @api.multi
    def action_reactive(self):
        self.write({'state': 'open'})
        # for shmt in self.mapped('shipment_ids'):
        #     shmt.active = True
        # for hbl in self.mapped('shipment_ids.hbl_ids'):
        #     hbl.active = True

    @api.multi
    def action_complete(self):
        self.write({'state': 'compelte'})

    @api.multi
    def action_lock(self):
        self.write({'state': 'lock'})

    @api.multi
    def action_ib_start(self):
        self.write({
            'state': 'ib_start',
            'ib_start': True,
            'ib_start_uid': self.env.user.id,
            'ib_transaction_date': fields.date.today()
        })
        for shmt in self.env['fwdr.shipment'].search(['&',('job_id','=',self.id),('state','!=','cancel')]):
            shmt.write({'state':'ib_start'})

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):  
        res = super(FwdrJob, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)  
        if self._context.get('incoming'):
            if res['type']=="form": 
                doc = etree.XML(res['arch'])                    
                doc.xpath("//form")[0].set("create","false")                                                                         
                doc.xpath("//form")[0].set("edit","false") 
                res['arch']=etree.tostring(doc) 
            if res['type']=="tree":  
                doc = etree.XML(res['arch'])         
                doc.xpath("//tree")[0].set("create","false") 
                res['arch']=etree.tostring(doc)            
        return res

# Inbound Job
# class FwdrIbJob(models.Model):
#     _name = 'fwdr.ib.job'
#     _inherits = {'fwdr.job': 'job_id'}  

#     job_id = fields.Many2one('fwdr.job')
#     ib_transaction_date = fields.Date(string="Transaction Date") 
#     ib_billing_date = fields.Date(string="Billing Date") 
#     ib_active = fields.Boolean()    
    
#     # customs
#     m_custom_entry_number = fields.Char(string="Entry Number")
#     m_custom_entry_date = fields.Char(string="Entry Date")    
#     m_it_number = fields.Char(string="I.T. Number")
#     m_it_place = fields.Char(string="I.T. Place")
#     m_it_date = fields.Date(string="I.T. Date")    


# MB/L and AMS of Job
class FwdrJobMbl(models.Model):
    _name = 'fwdr.job.mbl'
    _rec_name = 'mbl_number'

    mbl_number = fields.Char(string="MBL/AMS#", required=True)
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
    _order = 'container_number asc'

    container_number = fields.Char(string="Container Number")
    type_id = fields.Many2one('fwdr.container.type', string="Type")
    seal_number = fields.Char(string="Seal Number")
    job_id = fields.Many2one('fwdr.job', string="Job ID")

