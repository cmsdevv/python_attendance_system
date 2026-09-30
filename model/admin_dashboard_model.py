from database.DatabaseConnection import get_connection
from datetime import date

class AdminDashboardModel:

    @staticmethod
    def get_stats():
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) AS total FROM students")
            total_students = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM sections")
            total_sections = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM subject_codes")
            total_subjects = cursor.fetchone()['total']

            today = date.today()

            cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE status='Present' AND date=%s", (today,))
            present = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE status='Absent' AND date=%s", (today,))
            absent = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM attendance WHERE status='Late' AND date=%s", (today,))
            late = cursor.fetchone()['total']

            cursor.close()
            conn.close()

            return {
                'total_students': total_students,
                'total_sections': total_sections,
                'total_subjects': total_subjects,
                'present': present,
                'absent': absent,
                'late': late
            }
        except Exception as e:
            print(f"ERROR fetching dashboard stats: {e}")
            return None