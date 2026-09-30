import sys
from PyQt5.QtWidgets import QApplication
from controller.student_login_controller import StudentLoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentLoginController()
    window.show()
    sys.exit(app.exec_())