# -*- coding: utf-8 -*-
{
    'name': "Forwarder",

    'summary': """
        Freight forwarder management""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'application': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'product', 'account', ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/job_access_rules.xml',
        'views/fwdr_location.xml',
        'views/res_partner.xml',
        'views/fwdr_base.xml',   
        # 'views/fwdr_shipment_new.xml',
        'views/fwdr_shipment_new1.xml',
        # 'views/fwdr_shipment_ib.xml',
        # 'views/fwdr_hbl.xml',  
        'views/fwdr_hbl_new.xml',                         
        'views/fwdr_job_new.xml',
        # 'views/fwdr_job_ib.xml',
        # 'report/hbl_report.xml',
        # 'report/hbl_report_template.xml'
        'views/fwdr_template.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/fwdr_base_demo.xml',
        # 'demo/fms.dictionary.csv',
        # 'demo/res.country.state.csv',
        # 'demo/fms.carrier.csv',
        # 'demo/fms.equipment.type.csv'
    ],
}