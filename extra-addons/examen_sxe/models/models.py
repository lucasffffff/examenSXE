# -*- coding: utf-8 -*-

from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Modelo de prueba"

    producto = fields.Char(string="Producto")
    viabilidad = fields.Float(string="Viabilidad")
