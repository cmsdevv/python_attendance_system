from database.DatabaseConnection import get_connection

class AdminDeleteStudentModel:

    @staticmethod
    def search_student(student_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT s.student_id, s.first_name, s.last_name,
                       sec.year_level, sec.section_name
                FROM students s
                JOIN sections sec ON s.section_id = sec.section_id
                WHERE s.student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR searching student: {e}")
            return None

    @staticmethod
    def delete_student(student_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR deleting student: {e}")
            return False