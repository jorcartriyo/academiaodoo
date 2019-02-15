from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Aula(models.Model):

    _name = 'odoo.academia.aula'

    name = fields.Char(string="Nombre", required=True)
    inicio = fields.Date(string="Fecha Inicio", inverse="_inicio_hoy")
    fin = fields.Date(string="Fecha Fin", inverse="_fin_hoy")
    duracion = fields.Char(string="Duración", compute='_set_duracion')
    plazas = fields.Integer(string="Plazas")
    tel = fields.Char()
    email = fields.Char()
    curso = fields.Char(string="Nombre del Curso")
    titulo = fields.Many2one(related="id_profesor.title")
    periodo = fields.Selection([(u'mañana', 'Mañana'), (u'tarde', 'Tarde'), (u'noche', 'Noche')])
    estado = fields.Selection([(u'noiniciada', 'No iniciada'), (u'ejecucion', 'En Ejecución'), (u'finalizada', 'Finalizada')], compute='_estado_aula')

    id_profesor = fields.Many2one(comodel_name="res.partner",
                                  inverse_name="id_aula",
                                    string="Profesor")

    id_estudiante = fields.One2many(comodel_name="res.partner",
                                   inverse_name="id_aula",
                                   string="Estudiantes")

    plazas_restantes = fields.Integer(string="Plazas Restantes", compute='_plazas_restantes')

    @api.one
    @api.depends('plazas','id_estudiante')
    def _plazas_restantes(self):
        for s in self:
            s.plazas_restantes = s.plazas - len(s.id_estudiante)

    @api.one
    @api.depends('inicio', 'fin')
    def _estado_aula(self):
        for st in self:
            if st.inicio:
                if fields.Date.from_string(st.inicio) > fields.Date.from_string(fields.Date.today()):
                    st.write({'estado': u'noiniciada'})
                    st.estado = u'noiniciada'
                elif st.fin and fields.Date.from_string(st.fin) < fields.Date.from_string(fields.Date.today()):
                    st.write({'estado': u'finalizada'})
                    st.estado = u'finalizada'
                elif fields.Date.from_string(st.inicio) <= fields.Date.from_string(fields.Date.today()):
                    st.write({'estado': u'ejecucion'})
                    st.estado = u'ejecucion'

    @api.one
    @api.constrains('id_estudiante')
    def _check_plazas(self):
        for record in self:
            if record.plazas_restantes < 0:
                raise ValidationError("No hay mas plazas disponibles!")

    @api.one
    def busca_profe(self):
        if self.id_profesor:
            self.write({'tel': self.id_profesor.nota, 'email': self.id_profesor.email})

    @api.one
    def _inicio_hoy(self):
        if not self.inicio:
            self.write({'inicio': fields.date.today()})

    @api.one
    def _fin_hoy(self):
        if not self.fin:
            self.write({'fin': fields.date.today()})

    @api.one
    def _set_duracion(self):
        date_format = "%Y-%m-%d"
        a = datetime.strptime(self.inicio,date_format)
        b = datetime.strptime(self.fin,date_format)
        resultado =(b-a).days
        self.duracion= str(resultado)+' Días'

