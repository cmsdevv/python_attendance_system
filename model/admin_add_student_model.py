from database.DatabaseConnection import get_connection

class AdminAddStudentModel:

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
    def add_student(student_id, first_name, last_name, section_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO students (student_id, first_name, last_name, section_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (student_id, first_name, last_name, section_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR adding student: {e}")
            return False