from flask import jsonify, json


# This class is a helper class to unify the response of our api. It allows
# us to maintain consistent api response across the application.
class ApiResponse:
    data = []
    message = "Successful request"
    hasError = False

    def __init__(self, data=data, message=message, has_error=hasError):
        self.data = data
        self.message = message
        self.hasError = has_error

    def respond(self):
        status_code = 200
        if self.hasError:
            status_code = 500
        return self.__dict__, status_code

    def get(self):
        return self.__dict__
