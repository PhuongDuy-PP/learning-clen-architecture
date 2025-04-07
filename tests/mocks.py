class MockLogger:
    def info(self, message):
        pass

    def error(self, message):
        pass

    def warning(self, message):
        pass

class MockValidator:
    def validate_email(self, email):
        return True

    def validate_password(self, password):
        return True

    def validate_username(self, username):
        return True 