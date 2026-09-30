from database.DatabaseConnection import get_connection

class AdminAttendanceModel:

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
    def get_students_by_section(section_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT s.student_id, s.first_name, s.last_name, sec.year_level
                FROM students s
                JOIN sections sec ON s.section_id = sec.section_id
                WHERE s.section_id = %s
                ORDER BY s.last_name, s.first_name
            """
            cursor.execute(query, (section_id,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching students: {e}")
            return []

    @staticmethod
    def get_existing_attendance(section_subject_id, date):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_id, status
                FROM attendance
                WHERE section_subject_id = %s AND date = %s
            """
            cursor.execute(query, (section_subject_id, date))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return {row['student_id']: row['status'] for row in result}
        except Exception as e:
            print(f"ERROR fetching existing attendance: {e}")
            return {}

    @staticmethod
    def save_attendance(records, admin_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

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
            return True

        except Exception as e:
            print(f"ERROR saving attendance: {e}")
            return False