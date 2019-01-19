import constants
from util.response_builder import ApiResponse


# custom validator decorator that help us validate product ids
# It only needs the field name of the product_id
def product_id_validator(key):
    def validate_key(route_func):
        def wrap(*args, **kwargs):
            id = kwargs.get(key)
            print(id)
            if id > constants.MAX_INT or id < 0:
                return ApiResponse(message="Invalid product id", has_error=True)
            return route_func(*args, **kwargs)
        return wrap
    return validate_key
