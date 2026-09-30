from database.DatabaseConnection import get_connection
import traceback
class AdminLoginModel:

    @staticmethod
    def login(username, password):
        try:
            conn = get_connection()
            if conn is None:
                print("CONNECTION IS NONE")
                return None
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM admins WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            print(f"Login result: {result}")
            return result
        except Exception as e:
            print(f"LOGIN ERROR: {e}")
            traceback.print_exc()
            return None