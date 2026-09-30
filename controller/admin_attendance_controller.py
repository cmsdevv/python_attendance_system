from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import (QMessageBox, QTableWidgetItem, QRadioButton, QWidget, QHBoxLayout, QButtonGroup)
from PyQt5.QtCore import Qt, QDate
from model.admin_attendance_model import AdminAttendanceModel
from controller.base_controller import BaseController
from database.DatabaseConnection import get_connection
from model.session_manager import SessionManager;

class AdminAttendanceController(BaseController):
    def __init__(self, previous_window=None, admin_id=None):
        super().__init__()
        self.previous_window = previous_window
        self.admin_id = admin_id
        
        if self.admin_id is None:
            print("WARNING: admin_id is None in AdminAttendanceController")

            if previous_window and hasattr(previous_window, 'admin_id'):
                self.admin_id = previous_window.admin_id
                print(f"Got admin_id from previous_window: {self.admin_id}")
            
            if self.admin_id is None:
                self.admin_id = SessionManager.get_admin_id()
                if self.admin_id:
                    print(f"Got admin_id from session: {self.admin_id}")
            
            if self.admin_id is None:
                try:
                    from database.DatabaseConnection import get_connection
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT admin_id FROM admins LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        self.admin_id = result[0]
                        print(f"Using first admin from database: {self.admin_id}")
                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(f"Error getting admin from database: {e}")
                    self.admin_id = 1 
        
        print(f"AdminAttendanceController initialized with admin_id: {self.admin_id}")
        self.button_groups = []
        uic.loadUi(resource_path("view", r"AdminAttendanceRecording.ui"), self)

        self.load_sections()

        self.cmbSection.currentIndexChanged.connect(self.on_section_changed)
        self.cmbSubject.currentIndexChanged.connect(self.load_students)
        self.btnSaveAttendance.clicked.connect(self.handle_save)

        self.pushButton.clicked.connect(self.go_to_dashboard)
        self.pushButton_2.clicked.connect(self.go_to_students)
        self.pushButton_3.clicked.connect(self.go_to_sections)
        self.pushButton_4.clicked.connect(self.go_to_subject_codes)
        self.pushButton_5.clicked.connect(self.go_to_assign_subjects)
        self.pushButton_6.clicked.connect(self.go_to_attendance)
        self.pushButton_7.clicked.connect(self.go_to_reports)
        self.pushButton_9.clicked.connect(self.handle_logout)
        
    def load_sections(self):
        self.sections = AdminAttendanceModel.get_sections()
        self.cmbSection.blockSignals(True)
        self.cmbSection.clear()
        for section in self.sections:
            self.cmbSection.addItem(section['section_name'], section['section_id'])
        self.cmbSection.blockSignals(False)
        self.on_section_changed()

    def on_section_changed(self):
        section_id = self.cmbSection.currentData()
        if section_id is None:
            return
        self.subjects = AdminAttendanceModel.get_subjects_by_section(section_id)
        self.cmbSubject.blockSignals(True)
        self.cmbSubject.clear()
        for subject in self.subjects:
            self.cmbSubject.addItem(subject['subject_code'], subject['section_subject_id'])
        self.cmbSubject.blockSignals(False)
        self.load_students()

    def load_students(self):
        section_id = self.cmbSection.currentData()
        section_subject_id = self.cmbSubject.currentData()
        if section_id is None:
            return

        students = AdminAttendanceModel.get_students_by_section(section_id)
        date = self.dateEdit.date().toPyDate()

        existing = {}
        if section_subject_id:
            existing = AdminAttendanceModel.get_existing_attendance(section_subject_id, date)

        self.button_groups = []
        self.attendanceTable.setRowCount(len(students))
        self.students_data = students

        for row, student in enumerate(students):
            full_name = f"{student['last_name']}, {student['first_name']}"
            self.attendanceTable.setItem(row, 0, QTableWidgetItem(str(student['student_id'])))
            self.attendanceTable.setItem(row, 1, QTableWidgetItem(full_name))
            self.attendanceTable.setItem(row, 2, QTableWidgetItem(str(student['year_level'])))

            btn_group = QButtonGroup()
            existing_status = existing.get(student['student_id'], 'Present')

            for col, status in enumerate(['Present', 'Late', 'Absent'], start=3):
                radio = QRadioButton()
                radio.setStyleSheet("QRadioButton { margin-left: 40px; }")
                if existing_status == status:
                    radio.setChecked(True)
                btn_group.addButton(radio, col)

                container = QWidget()
                layout = QHBoxLayout(container)
                layout.addWidget(radio)
                layout.setAlignment(Qt.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                self.attendanceTable.setCellWidget(row, col, container)

            self.button_groups.append(btn_group)

    def handle_save(self):
        """Save attendance records"""
        if not self.admin_id:
            QMessageBox.warning(self, "Warning", "Admin ID is missing. Please log in again.")
            return
        
        section_subject_id = self.cmbSubject.currentData()
        if section_subject_id is None:
            QMessageBox.warning(self, "Warning", "Please select a subject first.")
            return

        date = self.dateEdit.date().toPyDate()
        
        records = []
        for row, student in enumerate(self.students_data):
            btn_group = self.button_groups[row]
            checked_id = btn_group.checkedId()

            status_map = {3: 'Present', 4: 'Late', 5: 'Absent'}
            status = status_map.get(checked_id, 'Present')

            records.append((
                student['student_id'],
                section_subject_id,
                date,
                status,
                self.admin_id
            ))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if records:
                sample_section_subject_id = records[0][1]
                cursor.execute("SELECT section_subject_id FROM section_subjects WHERE section_subject_id = %s", 
                            (sample_section_subject_id,))
                if not cursor.fetchone():
                    print(f"ERROR: section_subject_id {sample_section_subject_id} does not exist")
                    QMessageBox.warning(self, "Error", f"Section subject ID {sample_section_subject_id} does not exist.")
                    cursor.close()
                    conn.close()
                    return
                
                cursor.execute("SELECT admin_id FROM admins WHERE admin_id = %s", (self.admin_id,))
                if not cursor.fetchone():
                    print(f"ERROR: admin_id {self.admin_id} does not exist")
                    QMessageBox.warning(self, "Error", f"Admin ID {self.admin_id} does not exist.")
                    cursor.close()
                    conn.close()
                    return
            
            print(f"Attempting to save {len(records)} attendance records")
            for i, record in enumerate(records[:3]):
                print(f"Record {i}: student_id={record[0]}, section_subject_id={record[1]}, "
                    f"date={record[2]}, status={record[3]}, recorded_by={record[4]}")
            
            query = """
                INSERT INTO attendance (student_id, section_subject_id, date, status, recorded_by)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    status = VALUES(status), 
                    recorded_by = VALUES(recorded_by)
            """
            
            cursor.executemany(query, records)
            conn.commit()
            
            cursor.close()
            conn.close()
            
            QMessageBox.information(self, "Success", "Attendance saved successfully!")
            self.load_students()
            
        except Exception as e:
            print(f"ERROR saving attendance: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to save attendance: {str(e)}")
        
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
        self.show()
    
    def go_to_reports(self):
        from controller.admin_report_controller import AdminReportController
        self.reports = AdminReportController(previous_window=self.previous_window, admin_id=self.admin_id)
        self.reports.show()
        self.hide()