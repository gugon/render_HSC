from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup


def create_nav(app):
    nav = Nav()
    nav.init_app(app)

    @nav.navigation()
    def menu_navbar():
        menu = Navbar('HSC')
        menu.items = [View('Home', 'auth.start'),
                      Subgroup(
                          'Cadastros',
                          View('Meus Dados', 'patient.personal_registration_menu'),
                          View('Exames', 'exam.exam_registration_menu'),
                          View('Meus Médicos', 'doctor.show_doctors')
                      ),
                      Subgroup(
                          'Visualizar Exames',
                          View('RX', 'exam.manage_rx'),
                          # View('Ressonância Magnética', 'exam.manage_rx'),
                      )
                      ]

        menu.items.append(View('Sair', 'auth.logout'))
        return menu

    @nav.navigation()
    def menu_doctor():
        menu = Navbar('HSC')
        menu.items = [View('Home', 'auth.login_doctor'),
                      View('Visualizar Exames', 'doctor.doctor_view')
                      ]
        menu.items.append(View('Sair', 'auth.logout'))
        return menu
