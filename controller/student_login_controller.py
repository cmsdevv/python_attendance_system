from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model.student_login_model import StudentLoginModel
from model.session_manager import SessionManager


class StudentLoginController(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("view", r"StudentLogin.ui"), self)

        self.loginBtn.clicked.connect(self.handle_login)
        self.adminBtn.clicked.connect(self.go_to_admin_login)

    def handle_login(self):
        student_id = self.lineEdit.text().strip()
        last_name = self.lineEdit_2.text().strip()

        if not student_id or not last_name:
            QMessageBox.warning(self, "Error", "Please enter your Student ID and Surname.")
            return

        student = StudentLoginModel.login(student_id, last_name)

        if student:
            SessionManager.set_admin(student)
            self.open_dashboard(student)
        else:
            QMessageBox.warning(self, "Error", "Invalid Student ID or Surname.")

    def open_dashboard(self, student):
        from controller.student_dashboard_controller import StudentDashboardController
        self.dashboard = StudentDashboardController(student=student)
        self.dashboard.show()
        self.hide()

    def go_to_admin_login(self):
        from controller.admin_login_controller import AdminLoginController
        self.admin_login = AdminLoginController()
        self.admin_login.show()
        self.hide()