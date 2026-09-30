class SessionManager:
    _admin_id = None
    _username = None
    
    @classmethod
    def set_admin(cls, admin_data):
        """Store admin data from login"""
        if isinstance(admin_data, dict):
            cls._admin_id = admin_data.get('admin_id')
            cls._username = admin_data.get('username')
            print(f"SESSION SET: admin_id={cls._admin_id}, username={cls._username}")
        else:
            print(f"ERROR: set_admin received unexpected data type: {type(admin_data)}")
    
    @classmethod
    def get_admin_id(cls):
        print(f"SESSION GET admin_id: {cls._admin_id}")
        return cls._admin_id
    
    @classmethod
    def get_username(cls):
        return cls._username
    
    @classmethod
    def clear(cls):
        cls._admin_id = None
        cls._username = None
        print("SESSION CLEARED")