from flask import flash, Blueprint, redirect, url_for, session, render_template, request
from werkzeug.security import generate_password_hash

from app import db, paciente
from app.forms.patient_forms import *
from app.forms.quick_registration import QuickRegistrationForm

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/quick_registration', methods=['GET', 'POST'])
def quick_registration():
    if session.get('paciente_login'):
        return redirect(url_for('auth.start'))
    form = QuickRegistrationForm()
    if form.validate_on_submit():
        if form.signup.data:
            user_visitant = db.session.query(paciente).filter(paciente.CPF == form.cpf.data).first()
            if user_visitant:
                flash('Usuário já Cadastrado')
                return redirect(url_for('patient.quick_registration'))
            else:
                cadastraPaciente = paciente(
                    CPF=form.cpf.data,
                    senha=generate_password_hash(form.senha.data),
                    Permissao_idPermissao=2)
                db.session.add(cadastraPaciente)
                db.session.commit()

                flash('Cadastro Rápido realizado com sucesso')
                return redirect(url_for('auth.login_patient'))

        else:
            return redirect(url_for('auth.login_patient'))

    return render_template('quick_registration.html', title='Cadastro Rápido', form=form)


@patient_bp.route('/personal_registration_menu', methods=['GET', 'POST'])
def personal_registration_menu():
    if session.get('paciente_login'):
        return render_template('personal_registration_menu.html', title='Meus Dados', menu=0)


@patient_bp.route('/show_personal_information', methods=['GET', 'POST'])
def show_personal_information():
    if session.get('paciente_login'):
        ID = session.get('idPaciente')
        result = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
        return render_template('show_personal_information.html', title='Informações Pessoais', data=result, menu=0)


@patient_bp.route('/register_patient_name', methods=['GET', 'POST'])
def register_patient_name():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatientNameForm()
        if form.validate_on_submit():
            if form.cadastra_name.data or form.edita_name.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.nome = form.nome.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))
        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


@patient_bp.route('/register_patient_date', methods=['GET', 'POST'])
def register_patient_date():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatientDateForm()
        if form.validate_on_submit():
            if form.cadastra_data.data or form.edita_data.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.dataNascimento = form.dataNascimento.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))
        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


@patient_bp.route('/register_patient_cpf', methods=['GET', 'POST'])
def register_patient_cpf():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatienCpfForm()
        if form.validate_on_submit():
            if form.cadastra_cpf.data or form.edita_cpf.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.cpf = form.cpf.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))
        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


@patient_bp.route('/register_patient_gender', methods=['GET', 'POST'])
def register_patient_gender():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatientGenderForm()
        if form.validate_on_submit():
            if form.cadastra_genero.data or form.edita_genero.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.genero = form.genero.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))
        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


@patient_bp.route('/register_patient_email', methods=['GET', 'POST'])
def register_patient_email():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatienEmailForm()
        if form.validate_on_submit():
            if form.cadastra_email.data or form.edita_email.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.email = form.email.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))
        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


@patient_bp.route('/register_patient_phone', methods=['GET', 'POST'])
def register_patient_phone():
    if session.get('paciente_login'):
        decisao = request.args.get('decisao')
        dados = request.args.get('coluna')

        ID = session.get('idPaciente')

        form = RegisterPatienPhoneForm()
        if form.validate_on_submit():
            if form.cadastra_telefone.data or form.edita_telefone.data:
                cadastro = db.session.query(paciente).filter(ID == paciente.idPaciente).first()
                cadastro.telefone = form.telefone.data

                db.session.add(cadastro)
                db.session.commit()

                flash('Ação realizada com sucesso')
                return redirect(url_for('patient.show_personal_information'))
            else:
                return redirect(url_for('auth.404'))

        return render_template('registration_patient_info.html', form=form, data1=decisao, data2=dados)


# @patient_bp.route('/teste', methods=["GET"])
# def teste():  # put application's code here
#     if session.get('paciente_login'):
#         return render_template('teste2.html')
