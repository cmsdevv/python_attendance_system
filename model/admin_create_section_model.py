from database.DatabaseConnection import get_connection

class AdminCreateSectionModel:

    @staticmethod
    def create_section(section_name, year_level, program):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO sections (section_name, year_level, program) VALUES (%s, %s, %s)"
            cursor.execute(query, (section_name, year_level, program))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"ERROR creating section: {e}")
            return False