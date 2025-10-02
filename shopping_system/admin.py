class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def to_dict(self):
        """转换为字典"""
        return {
            "username": self.username,
            "password": self.password,
            "role": "admin"
        }