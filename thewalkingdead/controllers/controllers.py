# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo import tools
from odoo.fields import Integer

#class banner_survivor_revive_controller(http.Controller):
#    @http.route('/thewalkingdead/revive_banner', auth='user', type='json')
 #   def banner(self):
  #      return {
   #         'html': """
    #            <div  class="thewalkingdead_banner" style="height: 200px; background-image: url(/thewalkingdead/static/src/revive.jpg)">
     #           <div class="thewalkingdead_button" style="position: static; color:#fff;">
      #          <a class="banner_button" type="action" data-reload-on-close="true"
       #         role="button" data-method="action_resurect_wizard" data-model="wizard.revive">Revive Survivors</a>
        #        </div>
         #       </div> """
        #}
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
