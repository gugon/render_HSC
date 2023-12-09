from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import EmailField, SubmitField, StringField, TextAreaField, validators, SelectField


class RegisterDoctorForm(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired()])
    crm = StringField('CRM', [validators.DataRequired()])
    uf = SelectField('UF', [validators.DataRequired()],
                     choices=["", 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MS',
                              'MT', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO',
                              'RR', 'SC', 'SP', 'SE', 'TO'])
    especializacao = StringField('Especialização', [validators.DataRequired()])
    email = EmailField('Endereço de email', [validators.DataRequired()])
    informacoes = TextAreaField('Informação Complemetar', [validators.DataRequired()])

    submit = SubmitField('Cadastrar')


class SelectDoctorForm(FlaskForm):
    # medico = SelectField('Selecione um Médico', [validators.DataRequired()], choices=[(" ", " "),
    #                                                                                   (" ", " "), (" ", " ")],
    #                      default=" ")
    medico = SelectField('Selecione um Médico', [validators.DataRequired()], choices=[" "], default=" ")
    submit = SubmitField('Compartilhar Exame(s)')

