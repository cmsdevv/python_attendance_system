from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from model.student_dashboard_model import StudentDashboardModel


class StudentDashboardController(QMainWindow):
    def __init__(self, student=None):
        super().__init__()
        self.student = student
        uic.loadUi(resource_path("view", r"StudentInterface.ui"), self)

        self.attendanceHistoryTable.verticalHeader().setVisible(False)

        self.label_4.setText(f"Welcome, {student['first_name']}!")
        self.load_attendance()

        self.pushButton.clicked.connect(self.load_attendance)
        self.pushButton_9.clicked.connect(self.handle_logout)

    def load_attendance(self):
        records = StudentDashboardModel.get_attendance(self.student['student_id'])
        self.attendanceHistoryTable.setRowCount(len(records))

        for row, record in enumerate(records):
            self.attendanceHistoryTable.setItem(row, 0, QTableWidgetItem(record['subject_code']))
            self.attendanceHistoryTable.setItem(row, 1, QTableWidgetItem(str(record['date'])))

            status_item = QTableWidgetItem(record['status'])
            status_item.setTextAlignment(Qt.AlignCenter)

            if record['status'] == 'Present':
                status_item.setForeground(QColor('#22C55E'))
            elif record['status'] == 'Absent':
                status_item.setForeground(QColor('#EF4444'))
            elif record['status'] == 'Late':
                status_item.setForeground(QColor('#F59E0B'))

            self.attendanceHistoryTable.setItem(row, 2, status_item)

    def handle_logout(self):
        confirm = QMessageBox.question(self, "Logout",
                                       "Are you sure you want to logout?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            from model.session_manager import SessionManager
            SessionManager.clear()
            from controller.student_login_controller import StudentLoginController
            self.login = StudentLoginController()
            self.login.show()
            self.hide()