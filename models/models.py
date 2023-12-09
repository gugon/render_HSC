from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
# from app import app


def create_db(app):
    db = SQLAlchemy(app)
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

    medico = Base.classes.Medico
    paciente = Base.classes.Paciente
    imagem = Base.classes.Imagem
    exame = Base.classes.Exame
    pacHasMed = Base.classes.Paciente_has_Medico
    compartilhado = Base.classes.Compartilhado
    return db, paciente, medico, imagem, exame, pacHasMed, compartilhado
