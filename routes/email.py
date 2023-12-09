from flask import flash, Blueprint, redirect, url_for, render_template
from flask_mail import Message

from app import mail
from app.forms.email_forms import EmailForm

email_bp = Blueprint('email', __name__)


# @email_bp.route('/send_email', methods=['GET', 'POST'])
def send_email(email_content):
    destinatario = email_content["Medico"]["email"]
    assunto = "Senha de acesso a plataforma HSC"
    corpo = e_mail(email_content)

    try:
        mensagem = Message(assunto, recipients=[destinatario])
        mensagem.body = corpo
        mail.send(mensagem)

        flash('E-mail enviado com sucesso!', 'success')
        return redirect(url_for('auth.start'))
    except Exception as e:
        flash(f'Erro ao enviar e-mail: {str(e)}', 'danger')
        return redirect(url_for('auth.start'))

    # form = EmailForm()

    # if form.validate_on_submit():
    #     destinatario = form.destinatario.data #pegar o email do medico
    #     assunto = form.assunto.data 
    #     corpo = form.corpo.data

    #     try:
    #         # Enviar e-mail
    #         mensagem = Message(assunto, recipients=[destinatario])
    #         mensagem.body = corpo
    #         mail.send(mensagem)

    #         flash('E-mail enviado com sucesso!', 'success')
    #         return redirect(url_for('auth.start'))
    #     except Exception as e:
    #         flash(f'Erro ao enviar e-mail: {str(e)}', 'danger')
    #         return redirect(url_for('auth.start'))

    # return render_template('teste.html', form=form)


def e_mail(email_content):
    body_html = f""" 
        Olá, Dr. { email_content['Medico']['nome'] },
        A senha de acesso para a plataforma HSC é { email_content['Medico']['senha'] }
        
        Atenciosamente seu paciente, { email_content['Paciente']['nome']}
    
    """
    # <html>
    #     <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; color: #333; padding: 20px;">
    #         <h1 style="color: #007BFF;">Senha de acesso a plataforma HSC</h1>
    #         <p style="font-size: 16px;">Olá Dr. {{ email_content['Medico']['nome'] }},</p>
    #         <p style="font-size: 16px;">A senha de acesso para a plataforma HSC é {{ email_content['Medico']['senha'] }}</p>
    #         <p style="font-size: 16px;"></p>
    #         <p style="font-size: 16px;">Atenciosamente seu paciente,<br>Seu Nome</p>
    #     </body>
    # </html>

    

    # # Corpo do e-mail com HTML
    # body_html = """
    #     <html>
    #         <head>
    #             <style>
    #                 /* Estilos CSS aqui */
    #                 body {
    #                     font-family: Arial, sans-serif;
    #                     background-color: #f2f2f2;
    #                     color: #333;
    #                     padding: 20px;
    #                 }
    #
    #                 h1 {
    #                     color: #007BFF;
    #                 }
    #
    #                 p {
    #                     font-size: 16px;
    #                 }
    #             </style>
    #         </head>
    #         <body>
    #             <h1>Senha de acesso a plataforma HSC</h1>
    #             <p>Olá Dr. email_content["Medico"]["nome"],</p>
    #             <p>A senha de acesso para a plataforma HSC é {email_content["Medico"]["senha"]}</p>
    #             <p></p>
    #             <p>Atenciosamente seu paciente,<br>Seu Nome</p>
    #         </body>
    #     </html>
    #     """
    return body_html
