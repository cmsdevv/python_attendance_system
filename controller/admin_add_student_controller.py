from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model.admin_add_student_model import AdminAddStudentModel
from controller.base_controller import BaseController

class AdminAddStudentController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id 
        uic.loadUi(resource_path("view", r"AdminAddStudent.ui"), self)

        self.sections = []
        self.load_sections()

        self.saveBtn.clicked.connect(self.handle_save)
        self.clearBtn.clicked.connect(self.handle_clear)
        
        self.pushButton.clicked.connect(self.go_to_dashboard)
        self.pushButton_2.clicked.connect(self.go_to_students)
        self.pushButton_3.clicked.connect(self.go_to_sections)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_5.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_6.clicked.connect(self.go_to_attendance)
        self.pushButton_7.clicked.connect(self.go_to_reports)
        self.pushButton_8.clicked.connect(self.go_to_delete_student)
        self.pushButton_9.clicked.connect(self.handle_logout)     
        
    def go_to_dashboard(self):
        if self.previous_window:
            self.previous_window.show()
        self.hide()

    def go_to_students(self):
        self.show()

    def go_to_sections(self):
        from controller.admin_create_section_controller import AdminCreateSectionController
        self.create_section = AdminCreateSectionController(previous_window=self.previous_window)
        self.create_section.show()
        self.hide()

    def load_sections(self):
        self.sections = AdminAddStudentModel.get_sections()
        self.section.clear()
        for section in self.sections:
            self.section.addItem(section['section_name'], section['section_id'])

    def handle_save(self):
        student_id = self.studentID.text().strip()
        first_name = self.firstName.text().strip()
        last_name = self.lastName.text().strip()
        section_id = self.section.currentData()

        if not student_id or not first_name or not last_name:
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        if section_id is None:
            QMessageBox.warning(self, "Validation Error", "Please select a section.")
            return

        success = AdminAddStudentModel.add_student(student_id, first_name, last_name, section_id)

        if success:
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.handle_clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to add student. Please try again.")

    def handle_clear(self):
        self.studentID.clear()
        self.firstName.clear()
        self.lastName.clear()
        self.yearLevel.setCurrentIndex(0)
        self.status.setCurrentIndex(0)
        self.section.setCurrentIndex(0)
    
    def go_to_subject_codes(self):
        from controller.admin_subject_code_controller import AdminSubjectCodeController
        self.subject_codes = AdminSubjectCodeController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.subject_codes.show()
        self.hide()

    def go_to_assign_subjects(self):
        from controller.admin_assign_subject_controller import AdminAssignSubjectController
        self.assign = AdminAssignSubjectController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.assign.show()
        self.hide()

    def go_to_attendance(self):
        from controller.admin_attendance_controller import AdminAttendanceController
        self.attendance = AdminAttendanceController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.attendance.show()
        self.hide()

    def go_to_reports(self):
        from controller.admin_report_controller import AdminReportController
        self.reports = AdminReportController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.reports.show()
        self.hide()
        
    def go_to_delete_student(self):
        from controller.admin_delete_student_controller import AdminDeleteStudentController
        self.delete_student_win = AdminDeleteStudentController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.delete_student_win.show()
        self.hide()