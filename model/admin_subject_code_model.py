from database.DatabaseConnection import get_connection

class AdminSubjectCodeModel:

    @staticmethod
    def get_all_subject_codes():
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM subject_codes ORDER BY subject_code")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching subject codes: {e}")
            return []

    @staticmethod
    def add_subject_code(subject_code):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subject_codes (subject_code) VALUES (%s)", (subject_code,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR adding subject code: {e}")
            return False

    @staticmethod
    def delete_subject_code(subject_code_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subject_codes WHERE subject_code_id=%s", (subject_code_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR deleting subject code: {e}")
            return False