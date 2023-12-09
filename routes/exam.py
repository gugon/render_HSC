from flask import flash, Blueprint, redirect, url_for, session, render_template, request, Response

from app import db, exame, paciente, pacHasMed, imagem, compartilhado
from app.forms.doctor_forms import SelectDoctorForm
from app.forms.exam_forms import XRayRegistrationForm

from werkzeug.utils import secure_filename

from app.routes.doctor import return_doctor, return_id_doctor, medical_password_registration

exam_bp = Blueprint('exam', __name__)


@exam_bp.route('/exam_registration_menu', methods=['GET', 'POST'])
def exam_registration_menu():
    if session.get('paciente_login'):
        return render_template('exam_registration_menu.html', title='Menu Exames', menu=0)


@exam_bp.route('/exam_registration', methods=['GET', 'POST'])
def exam_registration():  # cadastroExame
    if session.get('paciente_login'):
        form = XRayRegistrationForm()

        if form.validate_on_submit():
            cadastroRX = exame(titulo=form.titulo.data,
                               local=form.local.data,
                               medicoSolicitado=form.medico.data,
                               protocolo=form.protocolo.data,
                               dataExame=form.dataExame.data,
                               informacoes=form.informacoes.data,
                               Paciente_idPaciente=session.get('idPaciente'))

            db.session.add(cadastroRX)
            db.session.commit()

            db.session.refresh(cadastroRX)
            id_Exame = cadastroRX.idExame

            flash('Campo de Exame Criado com Sucesso')
            return redirect(url_for('exam.select_image', id=id_Exame))
    return render_template('exam_registration.html', title='Cadastro de Exames', form=form, menu=0)


@exam_bp.route('/select_image', methods=['GET', 'POST'])
def select_image():
    if session.get('paciente_login'):
        return render_template('upload.html', title='Upload de Imagens',
                               idExame=request.args.get('id'))


@exam_bp.route('/upload/<int:id>', methods=['GET', 'POST'])
def upload(id):
    if request.method == 'POST':

        if 'exames[]' not in request.files:
            flash('No file part')
            return redirect(url_for('exam.upload'))

        files = request.files.getlist('exames[]')

        for file in files:

            filename = secure_filename(file.filename)
            mimetype = file.mimetype
            if not filename or not mimetype:
                flash('Bad upload!')
                redirect(url_for('upload'))

            img = imagem(img=file.read(), Exame_idExame=id, name=filename, mimetype=mimetype)
            db.session.add(img)
            db.session.commit()

    flash('File(s) successfully uploaded')
    return redirect(url_for('auth.start'))


@exam_bp.route('/rx', methods=['GET', 'POST'])
def manage_rx():
    lista = []
    listaMedicos = []

    if session.get('paciente_login'):
        ID = session.get('idPaciente')

        result = db.session.query(
            exame) \
            .join(paciente, exame.Paciente_idPaciente == paciente.idPaciente) \
            .filter(exame.Paciente_idPaciente == ID).all()

        if result:
            for i in result:
                lista.append(i)

            listaCompletamedicos = db.session.query(pacHasMed).filter(ID == pacHasMed.idPaciente_Paciente).all()

            for a in listaCompletamedicos:
                listaMedicos.append(a.idMedico_Medico)

            session['listaMedicos'] = listaMedicos

            if request.method == 'POST':
                listaExamesSelecionados = request.form.getlist('mycheckbox')
                session['listaExames'] = listaExamesSelecionados

                if not listaExamesSelecionados:
                    flash("Nenhum exame selecionado!")
                else:
                    return redirect(url_for('exam.share_exams'))

            return render_template('manage_rx.html', title='Lista de Exames', data=lista, menu=0)
        else:
            flash('Não possui nenhum exame cadastrado!')
            return redirect(url_for('auth.start'))


@exam_bp.route('/list_images/<string:name_title>', methods=['GET', 'POST'])
def list_images(name_title):
    lista = []
    if session.get('paciente_login'):
        ID = session.get('idPaciente')

        result = db.session.query(
            imagem) \
            .join(exame, imagem.Exame_idExame == exame.idExame) \
            .join(paciente, exame.Paciente_idPaciente == paciente.idPaciente) \
            .filter(exame.titulo == name_title) \
            .filter(exame.Paciente_idPaciente == ID).all()

        if result:
            for i in result:
                lista.append(i)
            return render_template('list_images.html', title='Imagens do Exame', data=lista, tituloPasta=name_title,
                                   menu=0)
        else:
            flash('Não possui nehuma imagem no banco')
            return redirect(url_for('auth.start'))


@exam_bp.route('/get_img/<int:id>')
def get_img(id):
    img = db.session.query(imagem).filter(imagem.id_imagem == id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)


@exam_bp.route('/share_exams', methods=['GET', 'POST'])
def share_exams():
    if session.get('paciente_login'):
        doctor_list = session['listaMedicos']
        exam_list_share = session['listaExames']
        id_doctor_email = ""

        select_doctor_form = SelectDoctorForm()

        for doctor in return_doctor(doctor_list):
            select_doctor_form.medico.choices.append(doctor)

        if select_doctor_form.validate_on_submit:
            if select_doctor_form.submit.data:
                if select_doctor_form.medico.data == " ":
                    flash("Selecione alguma opção da lista!")
                else:
                    for element in exam_list_share:
                        id_doctor = return_id_doctor(select_doctor_form.medico.data)
                        id_doctor_email = id_doctor
                        share_exam = compartilhado(idExame_Exame=element,
                                                   idMedico_Medico_Comp=id_doctor)
                        db.session.add(share_exam)

                    db.session.commit()
                    medical_password_registration(id_doctor_email)
                    return redirect(url_for('auth.start'))

        return render_template('manage_sharing.html', title='Compartilhar Exames',
                               form=select_doctor_form, menu=0)
