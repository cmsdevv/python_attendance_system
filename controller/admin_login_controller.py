from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from model.admin_login_model import AdminLoginModel
from controller.admin_dashboard_controller import AdminDashboardController
from model.session_manager import SessionManager

class AdminLoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("view", r"AdminLogin.ui"), self)

        self.loginBtn.clicked.connect(self.handle_login)
        self.adminBtn.clicked.connect(self.go_to_student_login)

    def handle_login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        admin = AdminLoginModel.login(username, password)

        if admin:
            SessionManager.set_admin(admin)
            self.open_dashboard(admin)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def open_dashboard(self, admin):
        self.dashboard = AdminDashboardController(admin_id=admin['admin_id'])
        self.dashboard.show()
        self.hide()
        
    
    def go_to_student_login(self):
        from controller.student_login_controller import StudentLoginController
        self.student_login = StudentLoginController()
        self.student_login.show()
        self.hide()