from database.DatabaseConnection import get_connection

class StudentLoginModel:

    @staticmethod
    def login(student_id, last_name):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM students WHERE student_id=%s AND last_name=%s"
            cursor.execute(query, (student_id, last_name))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"LOGIN ERROR: {e}")
            return None