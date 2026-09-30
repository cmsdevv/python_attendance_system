from database.DatabaseConnection import get_connection

class AdminReportModel:

    @staticmethod
    def get_sections():
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT section_id, section_name FROM sections")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching sections: {e}")
            return []

    @staticmethod
    def get_subjects_by_section(section_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT sc.subject_code_id, sc.subject_code, ss.section_subject_id
                FROM subject_codes sc
                JOIN section_subjects ss ON sc.subject_code_id = ss.subject_code_id
                WHERE ss.section_id = %s
                ORDER BY sc.subject_code
            """
            cursor.execute(query, (section_id,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching subjects: {e}")
            return []

    @staticmethod
    def get_attendance_report(section_id, section_subject_id, date_from, date_to):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    CONCAT(s.last_name, ', ', s.first_name) AS student_name,
                    sc.subject_code,
                    a.date,
                    a.status
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                JOIN section_subjects ss ON a.section_subject_id = ss.section_subject_id
                JOIN subject_codes sc ON ss.subject_code_id = sc.subject_code_id
                WHERE s.section_id = %s
                  AND a.section_subject_id = %s
                  AND a.date BETWEEN %s AND %s
                ORDER BY a.date, s.last_name, s.first_name
            """
            cursor.execute(query, (section_id, section_subject_id, date_from, date_to))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching report: {e}")
            return []