from resource_path import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model.admin_subject_code_model import AdminSubjectCodeModel


class AdminAddSubjectCodeController(QMainWindow):
    def __init__(self, parent=None, admin_id=None):
        super().__init__(parent)
        self.admin_id = admin_id 
        uic.loadUi(resource_path("view", r"AdminAddSubjectCode.ui"), self)

        self.saveSectionBtn.clicked.connect(self.handle_save)
        self.backBtn.clicked.connect(self.close)

    def handle_save(self):
        subject_code = self.lineText_2.text().strip()

        if not subject_code:
            QMessageBox.warning(self, "Validation Error", "Subject code is required.")
            return

        success = AdminSubjectCodeModel.add_subject_code(subject_code)

        if success:
            QMessageBox.information(self, "Success", "Subject code added successfully!")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to add subject code. It may already exist.")