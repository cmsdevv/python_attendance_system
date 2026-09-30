from PyQt5.QtWidgets import QMainWindow, QMessageBox


class BaseController(QMainWindow):
    def __init__(self):
        super().__init__()

    def handle_logout(self):
        confirm = QMessageBox.question(self, "Logout",
                                       "Are you sure you want to logout?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            from model.session_manager import SessionManager
            SessionManager.clear()
            from controller.admin_login_controller import AdminLoginController
            self.login = AdminLoginController()
            self.login.show()
            self.close()