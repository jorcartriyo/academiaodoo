from odoo import fields, models


class Cursos(models.Model):

    _name = 'odoo.academia.cursos'

    name = fields.Char(string="Nombre", required=True)

    id_curso = fields.Many2many('odoo.academia.aula', string="Aulas")

