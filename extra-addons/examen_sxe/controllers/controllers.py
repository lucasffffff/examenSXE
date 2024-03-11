# -*- coding: utf-8 -*-
# from odoo import http


# class ExamenSxe(http.Controller):
#     @http.route('/examen_sxe/examen_sxe', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/examen_sxe/examen_sxe/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('examen_sxe.listing', {
#             'root': '/examen_sxe/examen_sxe',
#             'objects': http.request.env['examen_sxe.examen_sxe'].search([]),
#         })

#     @http.route('/examen_sxe/examen_sxe/objects/<model("examen_sxe.examen_sxe"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('examen_sxe.object', {
#             'object': obj
#         })
