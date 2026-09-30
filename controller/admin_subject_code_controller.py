from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton
from model.admin_subject_code_model import AdminSubjectCodeModel
from controller.admin_add_subject_code_controller import AdminAddSubjectCodeController
from controller.base_controller import BaseController

class AdminSubjectCodeController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id
        uic.loadUi(resource_path("view", r"AdminSubjectCodeManagement.ui"), self)
        self.studentTable.verticalHeader().setVisible(False)
        self.studentTable.verticalHeader().setDefaultSectionSize(50)
        self.load_table()
        
        self.addStudentBtn.clicked.connect(self.open_add_subject_code)

        self.pushButton.clicked.connect(self.go_to_dashboard)
        self.pushButton_2.clicked.connect(self.go_to_students)
        self.pushButton_3.clicked.connect(self.go_to_sections)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_5.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_6.clicked.connect(self.go_to_attendance)
        self.pushButton_7.clicked.connect(self.go_to_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)
        
    def load_table(self):
        subject_codes = AdminSubjectCodeModel.get_all_subject_codes()
        self.studentTable.setRowCount(len(subject_codes))

        for row, item in enumerate(subject_codes):
            self.studentTable.setItem(row, 0, QTableWidgetItem(item['subject_code']))

            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8B0C00;
                    color: white;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
                QPushButton:hover { background-color: #67160F; }
            """)
            delete_btn.clicked.connect(lambda checked, sid=item['subject_code_id']: self.handle_delete(sid))
            self.studentTable.setCellWidget(row, 1, delete_btn)

    def handle_delete(self, subject_code_id):
        confirm = QMessageBox.question(self, "Confirm Delete",
                                       "Are you sure you want to delete this subject code?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success = AdminSubjectCodeModel.delete_subject_code(subject_code_id)
            if success:
                self.load_table()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete subject code.")

    def open_add_subject_code(self):
        self.add_subject_code = AdminAddSubjectCodeController(parent=self)
        self.add_subject_code.destroyed.connect(self.load_table)
        self.add_subject_code.show()

    def go_to_dashboard(self):
        if self.previous_window:
            self.previous_window.show()
        self.hide()

    def go_to_students(self):
        from controller.admin_add_student_controller import AdminAddStudentController
        self.students = AdminAddStudentController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.students.show()
        self.hide()

    def go_to_sections(self):
        from controller.admin_create_section_controller import AdminCreateSectionController
        self.sections = AdminCreateSectionController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.sections.show()
        self.hide()

    def go_to_subject_codes(self):
        self.show()  
    
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