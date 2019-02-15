from odoo import fields, models

class Alunmos(models.Model):

    _inherit = 'res.partner'

    id_aula = fields.Many2one(comodel_name="odoo.academia.alumnos",
                                 string="Alumnos")

    estudiante = fields.Boolean("Estudiante", default=True)
