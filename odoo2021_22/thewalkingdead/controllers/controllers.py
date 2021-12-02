# -*- coding: utf-8 -*-
# from odoo import http


# class Thewalkingdead(http.Controller):
#     @http.route('/thewalkingdead/thewalkingdead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/thewalkingdead/thewalkingdead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('thewalkingdead.listing', {
#             'root': '/thewalkingdead/thewalkingdead',
#             'objects': http.request.env['thewalkingdead.thewalkingdead'].search([]),
#         })

#     @http.route('/thewalkingdead/thewalkingdead/objects/<model("thewalkingdead.thewalkingdead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('thewalkingdead.object', {
#             'object': obj
#         })
