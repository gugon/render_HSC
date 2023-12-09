from flask import flash, Blueprint, session, render_template, url_for, redirect, request

from app import db, medico, pacHasMed, compartilhado, exame, imagem
from app.forms.doctor_forms import RegisterDoctorForm
from werkzeug.security import generate_password_hash
import random
import string

from app.routes.email import send_email

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/show_doctors', methods=['GET', 'POST'])
def show_doctors():
    if session.get('paciente_login'):
        list_doc_pat = list_doctor_for_patient()

        form = RegisterDoctorForm()
        if form.validate_on_submit():
            if form.submit.data:
                # random_password = generate_random_password()
                # session['senhaMedico'] = random_password
                # encoded_password = generate_password_hash(random_password)

                cadastrar = medico(nome=form.nome.data,
                                   CRM=form.crm.data,
                                   UF=form.uf.data,
                                   especializacao=form.especializacao.data,
                                   email=form.email.data,
                                   informacoes=form.informacoes.data,
                                   # senha=encoded_password,
                                   idPermissao_Permissao=3)

                db.session.add(cadastrar)
                db.session.commit()

                db.session.refresh(cadastrar)
                id_medico = cadastrar.idMedico

                id_paciente = session.get('idPaciente')
                doctor_patient = pacHasMed(idPaciente_Paciente=id_paciente,
                                           idMedico_Medico=id_medico)

                db.session.add(doctor_patient)
                db.session.commit()

                flash('Cadastro realizado com sucesso')
                return redirect(url_for('doctor.show_doctors'))

            else:
                return redirect(url_for('auth.404'))

        return render_template('show_registered_doctors.html', title="Médicos Cadastrados", medicos=list_doc_pat,
                               form=form, menu=0)


@doctor_bp.route('/delete_doctor', methods=['GET', 'POST'])
def delete_doctor():
    if session.get('paciente_login'):
        idMedico = request.args.get('id')

        delete_item_pacHasMed = db.session.query(pacHasMed).filter(idMedico == pacHasMed.idMedico_Medico).first()
        if delete_item_pacHasMed:
            db.session.delete(delete_item_pacHasMed)
            db.session.commit()

        delete_item_medico = db.session.query(medico).get(idMedico)
        if delete_item_medico:
            db.session.delete(delete_item_medico)
            db.session.commit()

        return redirect(url_for('doctor.show_doctors'))


@doctor_bp.route('/doctor_view', methods=['GET', 'POST'])
def doctor_view():
    resultados = []

    if session.get('logged_inMedico'):
        ID = session.get('idMedico')

        resultExames = db.session.query(
            compartilhado) \
            .join(exame, compartilhado.idExame_Exame == exame.idExame) \
            .join(medico, compartilhado.idMedico_Medico_Comp == medico.idMedico) \
            .filter(medico.idMedico == ID).all()

        if resultExames:
            for i in resultExames:
                nameExame = db.session.query(exame).filter(exame.idExame == i.idExame_Exame).first()
                resultados.append(nameExame)

    return render_template('doctor_view.html', title='Exames Disponíveis', data=resultados, menu=1)


@doctor_bp.route('/doctor_views_exams/<string:name_title>', methods=['GET', 'POST'])
def doctor_views_exams(name_title):
    lista = []
    if session.get('logged_inMedico'):
        ID = session.get('idMedico')

        result = db.session.query(
            imagem) \
            .join(exame, imagem.Exame_idExame == exame.idExame) \
            .join(compartilhado, exame.idExame == compartilhado.idExame_Exame) \
            .join(medico, compartilhado.idMedico_Medico_Comp == medico.idMedico) \
            .filter(medico.idMedico == ID).all()

        if result:
            for i in result:
                lista.append(i)
            return render_template('list_images.html', title='Imagens do Exame', data=lista, tituloPasta=name_title,
                                   menu=1)
        else:
            flash('Não possui nehuma imagem no banco')
            return redirect(url_for('doctor.doctor_view'))


def list_doctor_for_patient():
    listaIdMedicos = []
    listaMedicoPaciente = []
    ID = session.get('idPaciente')
    listaCompletamedicos = db.session.query(pacHasMed).filter(ID == pacHasMed.idPaciente_Paciente).all()

    for a in listaCompletamedicos:
        listaIdMedicos.append(a.idMedico_Medico)

    for i in listaIdMedicos:
        result = db.session.query(medico).filter(medico.idMedico == i).first()
        listaMedicoPaciente.append(result)

    return listaMedicoPaciente


def medical_password_registration(id_doctor):
    email_content = {
        "Medico": {"email": "", "nome": "", "senha": ""},
        "Paciente": {"email": "", "nome": "", "senha": ""}
    }

    random_password = generate_random_password()
    email_content["Medico"]["senha"] = random_password
    # session['senhaMedico'] = random_password
    encoded_password = generate_password_hash(random_password)

    pass_doctor = db.session.query(medico).filter(medico.idMedico == id_doctor).first()

    email_content["Paciente"]["nome"] = session.get('nome')
    email_content["Medico"]["nome"] = pass_doctor.nome
    email_content["Medico"]["email"] = pass_doctor.email

    pass_doctor.senha = encoded_password
    db.session.add(pass_doctor)
    db.session.commit()

    send_email(email_content)


def generate_random_password():
    caracteres = string.digits
    senha_aleatoria = ''.join(random.choice(caracteres) for i in range(6))

    return senha_aleatoria


def return_doctor(list_doctor):
    repost = []

    for i in list_doctor:
        result = db.session.query(medico).filter(medico.idMedico == i).first()
        repost.append(result.nome)
        # repost.append({'nome': result.nome, 'CRM': result.CRM, 'UF': result.UF})

    return repost


def return_id_doctor(name_medico):
    repost = []

    result = db.session.query(medico).filter(medico.nome == name_medico).first()
    repost.append(result.idMedico)

    return repost
