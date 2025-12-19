from flask import jsonify, make_response

class NotificationService:
    @staticmethod
    def notify_error(message: str, status_code: int = 400):
        response = {
            "error": True,
            "message": message
        }
        return make_response(jsonify(response), status_code)