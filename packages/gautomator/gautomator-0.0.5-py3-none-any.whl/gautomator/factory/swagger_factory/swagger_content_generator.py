from copy import deepcopy

from gautomator.utils.backend.swagger_parser_util import SwaggerUtil
from gautomator.utils.common import GetUtil, logger, StoreUtil, JsonConverterUtil
from gautomator.const.common import EnvConst


class DataGenerate(object):

    def __int__(self):
        self.generate = None

    def generate_data(self):
        return self.generate


class DataValidator(object):
    def __init__(self):
        self.validate = None

    def validate_response(self):
        return self.validate


class APIGenerator(DataGenerate):
    """This method will cook the swagger object and set all parameters as None,
    then it can be re-cooked later.
    e.g.
    >> {'photo': {'type': 'string', 'required': False},
        'name': {'type': 'string', 'required': True}}
    >> { 'photo': None, 'name': None}

    Args:
        api_name: string: represent your tested api
        convert: boolean: if you wish to convert the output to object else it will return the json string
        swagger_content: object: this will lookup into the suite_store to get the Swagger_obj
    """

    def __init__(self,  api_name: str, convert: bool = True, swagger_content = None):
        if not swagger_content: 
            swagger_content = GetUtil.suite_get(EnvConst.Swagger.SWAGGER_OBJ)
        if not GetUtil.suite_get(api_name):
            __obj = SwaggerUtil.swagger_parser_factory(file_content=swagger_content)
            final = deepcopy(__obj)
            __tmp = __obj[api_name]['request']
            __final = final[api_name]['request']
            if __tmp:
                for k in __tmp.keys():
                    __final[k] = None
            logger.debug(f'Converted swagger: {final[api_name]}')
            if convert:
                __data = JsonConverterUtil.convert_json_to_object(final[api_name])
                StoreUtil.suite_store(keyword=api_name, data=__data)
                self.generate = __data
            else:
                StoreUtil.suite_store(keyword=api_name, data=final[api_name])
                self.generate = final[api_name]
        else:
            self.generate = GetUtil.suite_get(api_name)


class APIResponseValidator(DataValidator):
    def __init__(self, expected: dict, response: dict):
        """
        This method will do the validation for response object
        This will compare the actual response from the request with the schema defined in swagger.
        Return boolean value.
        """
        if type(response).__name__ == 'ObjConverter':
            _res = response.__dict__  # convert object to dict
        else:
            _res = response
        logger.debug(f'Comparing response\n{_res} \n and default schema \n{expected}')
        a = set([True if type(v).__name__ in expected[k] else False for k, v in _res.items()])
        logger.info(f'Data returns as {list(a)}')
        self.validate = True if (list(a)[0] and len(a) == 1) else False