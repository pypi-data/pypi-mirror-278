from gautomator.factory.swagger_factory import APIFactory
from gautomator.factory.request_factory import RequestFactory

class APIConfiguration:
    def __init__(self):
        self.factory_request = RequestFactory
        self.factory_api = APIFactory()
        

    def validate_response_schema(self, schema, actual) -> bool:
        return self.factory_api.validate_response(schema, actual)
