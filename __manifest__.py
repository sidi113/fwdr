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
    'depends': ['base', 'product', 'account'],

    # always loaded
    'data': [
        # 'views/test.xml'
        # 'security/ir.model.access.csv',
        'views/fwdr_location.xml',
        'views/res_partner.xml',
        'views/fwdr_base.xml',   
        'views/fwdr_shipment.xml',
        'views/fwdr_hbl.xml',                   
        'views/fwdr_job.xml',
        'report/hbl_report.xml',
        'report/hbl_report_template.xml'
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