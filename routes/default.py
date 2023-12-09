from run import app
from app.routes.auth import auth_bp
from app.routes.doctor import doctor_bp
from app.routes.patient import patient_bp
from app.routes.exam import exam_bp
from app.routes.email import email_bp


app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(email_bp)

