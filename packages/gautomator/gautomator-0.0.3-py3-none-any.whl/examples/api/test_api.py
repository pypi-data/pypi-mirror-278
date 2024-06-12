from gautomator.utils.common import AssertUtil, logger, StringUtil
from gautomator.utils.backend import RequestUtil

from gautomator.const.api import RequestConst
from gautomator.factory.request_factory import RequestFactory
from gautomator.factory.swagger_factory import APIFactory, APIConfiguration
from gautomator.utils.common import ObjectSetupUtil




def test_get():
    data = RequestFactory().create_request(request_type=RequestConst.Method.GET)
    r = RequestUtil.request(url='https://petstore.swagger.io/v2/user/login?username=dale&password=dale', data=data)
    logger.info(r.__dict__)
    AssertUtil.true(r)

def test_gen_phone():
    for _ in range(1000):
        output = StringUtil.generate_random_phone_with_prefix()
        AssertUtil.equal(len(output), 10, output)
        
def test_gen_random_number():
    for _ in range(1000):
        output = StringUtil.generate_random_number(length=7)
        AssertUtil.equal(len(str(output)), 7, output)

class TestAPI(APIConfiguration):
    operation_id = 'discovery' # the operation_id of the api , this info is listed in the swagger.json file

    def __init__(self, token=None):
        super().__init__()
        self.api_obj = self.factory_api.generate_data(api_name=self.operation_id).generate
        if not token:
            self.token = ''
        else:
            self.token = token

    def test(self, **kwargs):
        body = ObjectSetupUtil.setup_object(self.api_obj.request, **kwargs)
        params = RequestFactory.create_request(request_type=self.api_obj.method, body=body, token=self.token)
        return RequestUtil.request(url=self.api_obj.endpoint, data=params)
    
