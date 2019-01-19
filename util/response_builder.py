from flask import jsonify, json

PASS_CODE = 200 # OK
HAS_ERROR_CODE = 422 # Unprocessable Entity


# This class is a helper class to unify the response of our api. It allows
# us to maintain consistent api response across the application.
class ApiResponse:
    data = []
    message = 'Successful request'
    has_error = False
    extra = {}

    def __init__(self, data=data, message=message, has_error=has_error, **kwargs):
        self.data = data
        self.message = message
        self.has_error = has_error
        self.__dict__.update(kwargs)

    def respond(self):
        status_code = PASS_CODE
        if self.has_error:
            status_code = HAS_ERROR_CODE
        return self.__dict__, status_code

    def get(self):
        return self.__dict__
