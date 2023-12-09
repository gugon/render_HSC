from flask import flash, Blueprint, redirect, url_for, session, render_template
from werkzeug.security import check_password_hash

from app import db, paciente, medico
from app.forms.login_forms import LoginPatientForm
from app.forms.login_forms import LoginDoctorForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def start():
    if session.get('paciente_login'):
        patient = db.session.query(paciente).filter(paciente.idPaciente == session.get('idPaciente')).first()
        return render_template('index.html', title='HSC', paciente=patient.nome, menu=0)
    else:
        return redirect(url_for('auth.login_patient'))


@auth_bp.route('/login_patient', methods=['GET', 'POST'])
def login_patient():
    if session.get('paciente_login'):
        return redirect(url_for('auth.start'))

    form = LoginPatientForm()
    if form.validate_on_submit():
        if form.signin.data:
            user = db.session.query(paciente).filter(
                paciente.CPF == form.cpf.data).first()

            if user:
                if check_password_hash(user.senha, form.senha.data):
                    session['paciente_login'] = True
                    session['idPaciente'] = user.idPaciente
                    session['nome'] = user.nome
                    session['CPF'] = user.CPF

                    return redirect(url_for('auth.start'))

            flash('Usuário ou senha inválidos')

            return redirect(url_for('auth.login_patient'))
        elif form.signup.data:
            return redirect(url_for('patient.quickRegistration'))
        else:
            return redirect(url_for('auth.login_patient'))
    return render_template('login.html', title='Autenticação de usuários', form=form)


@auth_bp.route('/indexDoctor', methods=['GET', 'POST'])
def indexDoctor():
    if session.get('logged_inMedico'):
        return render_template('index.html', title='HSC', medico=session.get('nome'), menu=1)
    else:
        return redirect(url_for('auth.login_doctor'))


@auth_bp.route('/login_doctor', methods=['GET', 'POST'])
def login_doctor():
    if session.get('logged_inMedico'):
        return redirect(url_for('auth.indexDoctor'))

    doctor_login_form = LoginDoctorForm()
    if doctor_login_form.validate_on_submit():
        if doctor_login_form.confirm.data:
            userMedico = db.session.query(medico).filter(
                medico.CRM == doctor_login_form.crm.data).first()

            if userMedico:
                if check_password_hash(userMedico.senha, doctor_login_form.senha.data):
                    session['logged_inMedico'] = True
                    session['idMedico'] = userMedico.idMedico
                    session['nome'] = userMedico.nome
                    session['CRM'] = userMedico.CRM

                    return render_template('index.html', title='HSC', medico=session.get('nome'), menu=1)

            flash('Usuário ou senha inválidos')
            return redirect(url_for('auth.login_doctor'))
        else:
            return redirect(url_for('auth.login_doctor'))
    return render_template('login_doctor.html', title='Acesso de Medico', form=doctor_login_form)


@auth_bp.route('/logout')
def logout():
    if session.get('paciente_login'):
        session.clear()
        flash('Logout realizado com sucesso!', 'info')
        return redirect(url_for('auth.start'))
    else:
        session.clear()
        flash('Logout realizado com sucesso!', 'info')
        return redirect(url_for('auth.login_doctor'))
