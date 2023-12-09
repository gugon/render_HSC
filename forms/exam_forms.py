from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, StringField, TextAreaField, validators, BooleanField


class XRayRegistrationForm(FlaskForm):
  titulo = StringField('Título', [validators.DataRequired()])
  local = StringField('Local', [validators.DataRequired()])
  medico = StringField('Médico Solicitante', [validators.DataRequired()])
  protocolo = StringField('Protocolo', [validators.DataRequired()])
  dataExame = DateField('Data do Exame')
  informacoes = TextAreaField('Informações', [validators.DataRequired()])
  submit = SubmitField('Criar')


class SelectExamForm(FlaskForm):
  confirmation = BooleanField('Confirma.')
  submit = SubmitField('Selecionar Exame(s)')