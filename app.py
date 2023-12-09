from flask import Flask
from dynaconf import FlaskDynaconf
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from nav import create_nav

# from app.models.models import create_db

app = Flask(__name__)
FlaskDynaconf(app)
Bootstrap(app)
mail = Mail(app)

db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

medico = Base.classes.Medico
paciente = Base.classes.Paciente
imagem = Base.classes.Imagem
exame = Base.classes.Exame
pacHasMed = Base.classes.Paciente_has_Medico
compartilhado = Base.classes.Compartilhado

# db, paciente, medico, imagem, exame, pacHasMed, compartilhado = create_db(app)

create_nav(app)

from app.routes import default
