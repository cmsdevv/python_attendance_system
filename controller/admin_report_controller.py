from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate, Qt
from model.admin_report_model import AdminReportModel
from controller.base_controller import BaseController

class AdminReportController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id
        uic.loadUi(resource_path("view", r"AttendanceReportPage.ui"), self)

        self.attendanceTable.verticalHeader().setVisible(False)
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit_2.setDate(QDate.currentDate())

        self.load_sections()

        self.cmbSection.currentIndexChanged.connect(self.on_section_changed)
        self.generateBtn.clicked.connect(self.generate_report)

        self.pushButton_8.clicked.connect(self.go_to_dashboard)
        self.pushButton_10.clicked.connect(self.go_to_students)
        self.pushButton_11.clicked.connect(self.go_to_sections)
        self.pushButton_12.clicked.connect(self.go_to_subject_codes)
        self.pushButton_13.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_14.clicked.connect(self.go_to_attendance)
        self.pushButton_15.clicked.connect(self.go_to_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)

    def load_sections(self):
        self.sections = AdminReportModel.get_sections()
        self.cmbSection.clear()
        for section in self.sections:
            self.cmbSection.addItem(section['section_name'], section['section_id'])
        self.on_section_changed()

    def on_section_changed(self):
        section_id = self.cmbSection.currentData()
        if section_id is None:
            return
        subjects = AdminReportModel.get_subjects_by_section(section_id)
        self.cmbSubject.clear()
        for subject in subjects:
            self.cmbSubject.addItem(subject['subject_code'], subject['section_subject_id'])

    def generate_report(self):
        section_id = self.cmbSection.currentData()
        section_subject_id = self.cmbSubject.currentData()

        date_from = self.dateEdit.date().toPyDate()
        date_to = self.dateEdit_2.date().toPyDate()

        if date_from > date_to:
            QMessageBox.warning(self, "Invalid Date", "Start date cannot be after end date.")
            return

        if section_id is None or section_subject_id is None:
            QMessageBox.warning(self, "Warning", "Please select a section and subject.")
            return

        records = AdminReportModel.get_attendance_report(
            section_id, section_subject_id, date_from, date_to
        )

        self.attendanceTable.setRowCount(len(records))

        for row, record in enumerate(records):
            self.attendanceTable.setItem(row, 0, QTableWidgetItem(record['student_name']))
            self.attendanceTable.setItem(row, 1, QTableWidgetItem(record['subject_code']))
            self.attendanceTable.setItem(row, 2, QTableWidgetItem(str(record['date'])))

            status_item = QTableWidgetItem(record['status'])
            status_item.setTextAlignment(Qt.AlignCenter)

            if record['status'] == 'Present':
                status_item.setForeground(QColor('#22C55E'))
            elif record['status'] == 'Absent':
                status_item.setForeground(QColor('#EF4444'))
            elif record['status'] == 'Late':
                status_item.setForeground(QColor('#F59E0B'))

            self.attendanceTable.setItem(row, 3, status_item)

        if not records:
            QMessageBox.information(self, "No Results", "No attendance records found for the selected filters.")

    def go_to_dashboard(self):
        if self.previous_window:
            self.previous_window.show()
        self.hide()

    def go_to_students(self):
        from controller.admin_add_student_controller import AdminAddStudentController
        self.students_win = AdminAddStudentController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.students_win.show()
        self.hide()

    def go_to_sections(self):
        from controller.admin_create_section_controller import AdminCreateSectionController
        self.sections_win = AdminCreateSectionController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.sections_win.show()
        self.hide()

    def go_to_subject_codes(self):
        from controller.admin_subject_code_controller import AdminSubjectCodeController
        self.subject_codes_win = AdminSubjectCodeController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.subject_codes_win.show()
        self.hide()

    def go_to_assign_subjects(self):
        from controller.admin_assign_subject_controller import AdminAssignSubjectController
        self.assign_win = AdminAssignSubjectController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.assign_win.show()
        self.hide()

    def go_to_attendance(self):
        from controller.admin_attendance_controller import AdminAttendanceController
        self.attendance_win = AdminAttendanceController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.attendance_win.show()
        self.hide()

    def go_to_reports(self):
        self.show()