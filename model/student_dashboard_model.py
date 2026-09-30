from database.DatabaseConnection import get_connection

class StudentDashboardModel:

    @staticmethod
    def get_attendance(student_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    sc.subject_code,
                    a.date,
                    a.status
                FROM attendance a
                JOIN section_subjects ss ON a.section_subject_id = ss.section_subject_id
                JOIN subject_codes sc ON ss.subject_code_id = sc.subject_code_id
                WHERE a.student_id = %s
                ORDER BY a.date DESC, sc.subject_code
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"ERROR fetching student attendance: {e}")
            return []