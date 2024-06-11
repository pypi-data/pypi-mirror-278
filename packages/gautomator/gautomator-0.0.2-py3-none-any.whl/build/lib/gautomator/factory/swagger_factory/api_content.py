from .swagger_content_generator import APIGenerator, APIResponseValidator
from gautomator.utils.common import logger


class APIFactory(object):
    """_summary_
    this factory will help to convert the request's body data into object
    So we can use this object in the RequestFactory
    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """

    @staticmethod
    def generate_data(api_name: str):
            logger.info(f'Generate all params of api: {api_name}')
            return APIGenerator(api_name=api_name)

    @staticmethod
    def validate_response(expected, actual):
        return APIResponseValidator(expected=expected, response=actual)