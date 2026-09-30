from database.DatabaseConnection import get_connection

class AdminAssignSubjectModel:

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
    def get_available_subjects(section_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT sc.subject_code_id, sc.subject_code
                FROM subject_codes sc
                WHERE sc.subject_code_id NOT IN (
                    SELECT ss.subject_code_id
                    FROM section_subjects ss
                    WHERE ss.section_id = %s
                )
                ORDER BY sc.subject_code
            """
            cursor.execute(query, (section_id,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching available subjects: {e}")
            return []

    @staticmethod
    def get_assigned_subjects(section_id):
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
            print(f"ERROR fetching assigned subjects: {e}")
            return []

    @staticmethod
    def assign_subject(section_id, subject_code_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO section_subjects (section_id, subject_code_id) VALUES (%s, %s)",
                (section_id, subject_code_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR assigning subject: {e}")
            return False

    @staticmethod
    def remove_subject(section_subject_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM section_subjects WHERE section_subject_id = %s",
                (section_subject_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR removing subject: {e}")
            return False