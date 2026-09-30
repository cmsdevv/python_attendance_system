from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model.admin_create_section_model import AdminCreateSectionModel
from controller.base_controller import BaseController

class AdminCreateSectionController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        uic.loadUi(resource_path("view", r"AdminCreateSection.ui"), self)

        self.previous_window = previous_window
        self.admin_id = admin_id
        self.saveSectionBtn.clicked.connect(self.handle_save)
        self.backBtn.clicked.connect(self.handle_back)
        
        self.pushButton.clicked.connect(self.go_to_dashboard)
        self.pushButton_2.clicked.connect(self.go_to_students)
        self.pushButton_3.clicked.connect(self.go_to_sections)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_5.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_6.clicked.connect(self.go_to_attendance)
        self.pushButton_7.clicked.connect(self.go_to_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)
        
    def go_to_dashboard(self):
        if self.previous_window:
            self.previous_window.show()
        self.hide()

    def go_to_students(self):
        from controller.admin_add_student_controller import AdminAddStudentController
        self.students = AdminAddStudentController(previous_window=self.previous_window)
        self.students.show()
        self.hide()

    def go_to_sections(self):
        self.show()       

    def handle_save(self):
        section_name = self.sectionName.text().strip()
        year_level = int(self.yearLevel.currentText())
        program = self.program.currentText()

        if not section_name:
            QMessageBox.warning(self, "Validation Error", "Section name is required.")
            return

        success = AdminCreateSectionModel.create_section(section_name, year_level, program)

        if success:
            QMessageBox.information(self, "Success", "Section created successfully!")
            self.sectionName.clear()
            self.yearLevel.setCurrentIndex(0)
            self.program.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to create section. It may already exist.")

    def handle_back(self):
        if self.previous_window:
            self.previous_window.show()
        self.close()
        
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