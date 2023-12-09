from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
import email_validator

class EmailForm(FlaskForm):
    destinatario = StringField('Destinatário', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    corpo = TextAreaField('Corpo do E-mail', validators=[DataRequired()])
    enviar = SubmitField('Enviar')