# [QA-QC] Gautomator Guideline
########################

## Unittest
```shell
behave
```

### Definition
```python
api_obj = APIFactory.generate_data(api_name='Service_Liveness').generate
```

The `api_obj` will have the content of 
```python
{
    'endpoint': str ,
    'content_type': str,
    'method': str,
    'request': RequestObj(),
    'response': ResponseObj()
}
```

### Usage

```python
from gautomator.cores.utils.common import ObjectSetupUtil
from gautomator.cores.factory.swagger_factory import APIFactory, APIConfiguration

class TestAPI(APIConfiguration):
    operation_id = 'Test_API' # the operation_id of the api , this info is listed in the swagger.json file

    def __init__(self, token=None):
        super().__init__()
        self.api_obj = self.factory_api.generate_data(api_name=self.operation_id).generate

    def test(self, **kwargs):
        body = ObjectSetupUtil.setup_object(self.api_obj.request, **kwargs)
        params = RequestFactory.create_request(request_type=self.api_obj.method, body=body, token=self._token)
        return RequestUtil.request(url=, data=params)
        
```