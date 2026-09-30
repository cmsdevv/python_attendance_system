from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from controller.base_controller import BaseController
from model.admin_delete_student_model import AdminDeleteStudentModel


class AdminDeleteStudentController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id
        self.current_student = None
        uic.loadUi(resource_path("view", r"admin_delete_student.ui"), self)

        self.logOutBtn.clicked.connect(self.handle_logout)
        self.lineText_1.textChanged.connect(self.handle_search)
        self.deleteStudentBtn.clicked.connect(self.handle_delete)
        self.deleteStudentBtn.setEnabled(False)

        self.dasboardBtn.clicked.connect(self.go_to_dashboard)
        self.studentsBtn.clicked.connect(self.go_to_students)
        self.sectionsBtn.clicked.connect(self.go_to_sections)
        self.subjectCodeBtn.clicked.connect(self.go_to_subject_codes)
        self.assignSubjectsBtn.clicked.connect(self.go_to_assign_subjects)
        self.attendanceBtn.clicked.connect(self.go_to_attendance)
        self.reportsBtn.clicked.connect(self.go_to_reports)

        self.clear_info()

    def handle_search(self):
        student_id = self.lineText_1.text().strip()
        if not student_id:
            self.clear_info()
            return

        student = AdminDeleteStudentModel.search_student(student_id)
        if student:
            self.current_student = student
            self.label_10.setText(str(student['student_id']))
            self.label_11.setText(f"{student['first_name']} {student['last_name']}")
            self.label_12.setText(str(student['year_level']))
            self.label_13.setText(student['section_name'])
            self.label_14.setText("Active")
            self.deleteStudentBtn.setEnabled(True)
        else:
            self.clear_info()
            self.deleteStudentBtn.setEnabled(False)

    def clear_info(self):
        self.label_10.setText("-")
        self.label_11.setText("-")
        self.label_12.setText("-")
        self.label_13.setText("-")
        self.label_14.setText("-")
        self.current_student = None
        self.deleteStudentBtn.setEnabled(False)

    def handle_delete(self):
        if not self.current_student:
            return

        confirm = QMessageBox.question(self, "Confirm Delete",
                                       f"Are you sure you want to delete student {self.current_student['first_name']} {self.current_student['last_name']}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success = AdminDeleteStudentModel.delete_student(self.current_student['student_id'])
            if success:
                QMessageBox.information(self, "Success", "Student deleted successfully!")
                self.lineText_1.clear()
                self.clear_info()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete student.")

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
        from controller.admin_report_controller import AdminReportController
        self.reports_win = AdminReportController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.reports_win.show()
        self.hide()