from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from model.admin_assign_subject_model import AdminAssignSubjectModel
from controller.base_controller import BaseController

class AdminAssignSubjectController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id 
        uic.loadUi(resource_path("view", r"AdminAssignSubject.ui"), self)

        self.load_sections()
        self.available_assigned_subjectTable.verticalHeader().setVisible(False)
        self.cmbSections.currentIndexChanged.connect(self.load_subjects)
        self.addSubjectBtn.clicked.connect(self.handle_add)
        self.removeSubjectBtn.clicked.connect(self.handle_remove)

        self.pushButton.clicked.connect(self.go_to_dashboard)
        self.pushButton_2.clicked.connect(self.go_to_students)
        self.pushButton_3.clicked.connect(self.go_to_sections)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_5.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_6.clicked.connect(self.go_to_attendance)
        self.pushButton_7.clicked.connect(self.go_to_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)
        
        
    def load_sections(self):
        self.sections = AdminAssignSubjectModel.get_sections()
        self.cmbSections.clear()
        for section in self.sections:
            self.cmbSections.addItem(section['section_name'], section['section_id'])
        self.load_subjects()

    def load_subjects(self):
        section_id = self.cmbSections.currentData()
        if section_id is None:
            return

        available = AdminAssignSubjectModel.get_available_subjects(section_id)
        assigned = AdminAssignSubjectModel.get_assigned_subjects(section_id)

        max_rows = max(len(available), len(assigned))
        self.available_assigned_subjectTable.setRowCount(max_rows)

        self.available_subjects = available
        self.assigned_subjects = assigned

        for row, item in enumerate(available):
            cell = QTableWidgetItem(item['subject_code'])
            cell.setData(Qt.UserRole, item['subject_code_id'])
            cell.setTextAlignment(Qt.AlignCenter)
            self.available_assigned_subjectTable.setItem(row, 0, cell)

        for row in range(len(available), max_rows):
            self.available_assigned_subjectTable.setItem(row, 0, QTableWidgetItem(""))

        for row, item in enumerate(assigned):
            cell = QTableWidgetItem(item['subject_code'])
            cell.setData(Qt.UserRole, item['section_subject_id'])
            cell.setTextAlignment(Qt.AlignCenter)
            self.available_assigned_subjectTable.setItem(row, 1, cell)

        for row in range(len(assigned), max_rows):
            self.available_assigned_subjectTable.setItem(row, 1, QTableWidgetItem(""))

    def handle_add(self):
        selected = self.available_assigned_subjectTable.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a subject from the left column.")
            return

        item = selected[0]
        if item.column() != 0:
            QMessageBox.warning(self, "Warning", "Please select from the Available Subjects column.")
            return

        subject_code_id = item.data(Qt.UserRole)
        section_id = self.cmbSections.currentData()

        if not subject_code_id:
            return

        success = AdminAssignSubjectModel.assign_subject(section_id, subject_code_id)
        if success:
            self.load_subjects()
        else:
            QMessageBox.critical(self, "Error", "Failed to assign subject.")

    def handle_remove(self):
        selected = self.available_assigned_subjectTable.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a subject from the right column.")
            return

        item = selected[0]
        if item.column() != 1:
            QMessageBox.warning(self, "Warning", "Please select from the Assigned Subjects column.")
            return

        section_subject_id = item.data(Qt.UserRole)
        if not section_subject_id:
            return

        confirm = QMessageBox.question(self, "Confirm Remove",
                                       "Remove this subject from the section?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success = AdminAssignSubjectModel.remove_subject(section_subject_id)
            if success:
                self.load_subjects()
            else:
                QMessageBox.critical(self, "Error", "Failed to remove subject.")

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
        from controller.admin_subject_code_controller import AdminSubjectCodeController
        self.subject_codes = AdminSubjectCodeController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.subject_codes.show()
        self.hide()

    def go_to_assign_subjects(self):
        self.show()  
        
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