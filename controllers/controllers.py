# -*- coding: utf-8 -*-
from odoo import http

# class Fms(http.Controller):
#     @http.route('/fms/fms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fms/fms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fms.listing', {
#             'root': '/fms/fms',
#             'objects': http.request.env['fms.fms'].search([]),
#         })

#     @http.route('/fms/fms/objects/<model("fms.fms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fms.object', {
#             'object': obj
#         })