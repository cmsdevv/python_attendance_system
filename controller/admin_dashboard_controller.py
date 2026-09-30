from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from datetime import date
from controller.admin_add_student_controller import AdminAddStudentController
from controller.admin_create_section_controller import AdminCreateSectionController
from controller.admin_subject_code_controller import AdminSubjectCodeController
from controller.admin_assign_subject_controller import AdminAssignSubjectController
from controller.admin_attendance_controller import AdminAttendanceController
from controller.admin_report_controller import AdminReportController
from model.admin_dashboard_model import AdminDashboardModel
from model.session_manager import SessionManager
from controller.base_controller import BaseController

class AdminDashboardController(BaseController):
    def __init__(self, admin_id=None):
        self.admin_id = admin_id
        super().__init__()
        try:
            uic.loadUi(resource_path("view", r"AdminDashboard.ui"), self)
            print("Dashboard UI loaded")
        except Exception as e:
            print("DASHBOARD LOAD ERROR:", e)
        
        self.load_stats()
        
        self.pushButton.clicked.connect(self.open_dashboard)
        self.pushButton_2.clicked.connect(self.open_add_student)
        self.pushButton_3.clicked.connect(self.open_create_section)
        self.pushButton_4.clicked.connect(self.open_subject_codes)
        self.pushButton_5.clicked.connect(self.open_assign_subjects)
        self.pushButton_6.clicked.connect(self.open_attendance)
        self.pushButton_7.clicked.connect(self.open_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)
        
    def load_stats(self):
        stats = AdminDashboardModel.get_stats()
        if stats:
            self.lblTotalStudents.setText(str(stats['total_students']))
            self.lblTOtalSections.setText(str(stats['total_sections']))
            self.lblTotalSubjects.setText(str(stats['total_subjects']))
            self.lblCurrentPresent.setText(str(stats['present']))
            self.lblCurrentAbsent.setText(str(stats['absent']))
            self.lblCurrentLate.setText(str(stats['late']))
            self.lblCurrentDate.setText(f"Date: {date.today().strftime('%Y-%m-%d')}")
            
            username = SessionManager.get_username()
            if username:
                self.label_3.setText(f"Welcome, {username}!")
            else:
                if self.admin_id:
                    try:
                        from database.DatabaseConnection import get_connection
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT username FROM admins WHERE admin_id = %s", (self.admin_id,))
                        result = cursor.fetchone()
                        if result:
                            username = result[0]
                            self.label_3.setText(f"Welcome, {username}!")
                        else:
                            self.label_3.setText("Welcome, Admin!")
                        cursor.close()
                        conn.close()
                    except Exception as e:
                        print(f"Error getting username: {e}")
                        self.label_3.setText("Welcome, Admin!")
                else:
                    self.label_3.setText("Welcome, Admin!")
        
    def open_subject_codes(self):
        self.subject_codes = AdminSubjectCodeController(previous_window=self, admin_id=self.admin_id)
        self.subject_codes.show()
        self.hide()

    def open_dashboard(self):
        self.load_stats()

    def open_add_student(self):
        self.add_student = AdminAddStudentController(previous_window=self, admin_id=self.admin_id)
        self.add_student.show()
        self.hide()
        
    def open_create_section(self):
        self.create_section = AdminCreateSectionController(previous_window=self, admin_id=self.admin_id)
        self.create_section.show()
        self.hide()
        
    def open_assign_subjects(self):
        self.assign_subjects = AdminAssignSubjectController(previous_window=self, admin_id=self.admin_id)
        self.assign_subjects.show()
        self.hide()
            
    def open_attendance(self):
        self.attendance = AdminAttendanceController(previous_window=self, admin_id=self.admin_id)
        self.attendance.show()
        self.hide()
        
    def open_reports(self):
        self.reports = AdminReportController(previous_window=self, admin_id=self.admin_id)
        self.reports.show()
        self.hide()
    
    def open_add_student(self):
        self.add_student = AdminAddStudentController(previous_window=self, admin_id=self.admin_id)
        self.add_student.show()
        self.hide()