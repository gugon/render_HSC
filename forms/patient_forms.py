from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, StringField, SelectField, validators


class PersonalRegistrationForm(FlaskForm):
    nome = StringField('Nome')
    sobreNome = StringField('Sobrenome')
    dataNascimento = DateField('Data de nascimento', format='%Y/%m/%d')
    cpf = StringField('CPF')
    genero = SelectField('Gênero', choices=[(''), ('Masculino'), ('Feminino'), ('Outros')])
    telefone = StringField('Telefone')
    email = StringField('E-mail')
    submit_cadastra = SubmitField('Cadastrar')
    submit_edita = SubmitField('Editar')


class RegisterPatientNameForm(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired()])
    cadastra_name = SubmitField('Cadastrar')
    edita_name = SubmitField('Editar')


class RegisterPatientSurNameForm(FlaskForm):
    sobre_nome = StringField('Sobrenome', [validators.DataRequired()])
    cadastra_sobre_nome = SubmitField('Cadastrar')
    edita_sobre_nome = SubmitField('Editar')


class RegisterPatientDateForm(FlaskForm):
    dataNascimento = DateField('Data de nascimento', [validators.DataRequired()])
    cadastra_data = SubmitField('Cadastrar')
    edita_data = SubmitField('Editar')


class RegisterPatienCpfForm(FlaskForm):
    cpf = StringField('CPF', [validators.DataRequired()])
    cadastra_cpf = SubmitField('Cadastrar')
    edita_cpf = SubmitField('Editar')


class RegisterPatientGenderForm(FlaskForm):
    genero = SelectField('Gênero', [validators.DataRequired()], choices=[(''),
                                                                         ('Masculino'),
                                                                         ('Feminino'),
                                                                         ('Outros')])
    cadastra_genero = SubmitField('Cadastrar')
    edita_genero = SubmitField('Editar')


class RegisterPatienPhoneForm(FlaskForm):
    telefone = StringField('Telefone', [validators.DataRequired()])
    cadastra_telefone = SubmitField('Cadastrar')
    edita_telefone = SubmitField('Editar')


class RegisterPatienEmailForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    cadastra_email = SubmitField('Cadastrar')
    edita_email = SubmitField('Editar')
