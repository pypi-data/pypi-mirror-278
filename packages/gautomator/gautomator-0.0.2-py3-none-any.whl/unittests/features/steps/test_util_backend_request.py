from gautomator.const.api import RequestConst
from gautomator.const.custom_exception import RequestError
from gautomator.utils.backend import RequestUtil
from gautomator.utils.common import AssertUtil
from gautomator.model.request import ResponseObjModel, RequestObjModel

from behave import *

import json
from unittest.mock import patch

import requests
from requests import Response, PreparedRequest
from requests.adapters import HTTPAdapter


def mock_response(context, status_code):
    _res = Response()
    _res.status_code = int(status_code)
    _res._content = json.dumps(context.data.body).encode()
    return _res

#########
# ----- Given ----------
#########


@Given('a RequestUtil func')
def step_imp(context):
    context.default_url = 'https://google.com'
    context.data = {"payload": {"id": 1}, "status": {"message": "available", "code": "1"}, "meta": {"msg": "meta"}}
    context.request_obj_model_data = RequestObjModel(**{"method": "GET", "header": {"Content-Type": "application/json", "Authorization": "Bearer"}, "body": {"name": "unittest"}})
    context.expected_output = ResponseObjModel(
        **{"status_code": 200,
           "status_msg": "1",
           "message": "available",
           "response_data": {"id": 1},
           "meta_data": {"msg": "meta"}}
    )
    _resp = Response()
    _resp.status_code = 200
    _resp._content = json.dumps(context.data).encode()
    _resp.connection = HTTPAdapter()
    _resp.request = PreparedRequest()
    _resp.request.prepare(method='GET', url=context.default_url)
    context.expected_response = _resp
    context.request = RequestUtil


@Given('a RequestUtil func for request {request_object_model_dict}')
def step_imp(context, request_object_model_dict):
    context.data = RequestObjModel(**json.loads(request_object_model_dict))
    context.payload_data = {"payload": {"id": 1}, "status": {"message": "available", "code": "1"}, "meta": {"msg": "meta"}}
    context.request = RequestUtil


@Given('a RequestUtil')
def step_imp(context):
    context.request = RequestUtil

#########
# ----- When ----------
#########


@When('init _parse_data function with valid data')
def step_imp(context):
    _res = Response()
    _res.status_code = 200
    _res._content = json.dumps(context.data).encode()
    context.parse_data = context.request._parse_data(_res)


@When('init {request_method} function with valid data {status_code}')
def step_imp(context, request_method, status_code):
    context.resp_data = None
    if request_method == RequestConst.Method.POST:
        context.resp_data = context.request._post('https://example.com', context.data)
    elif request_method == RequestConst.Method.GET:
        context.resp_data = context.request._get('https://example.com', context.data)
    elif request_method == RequestConst.Method.PUT:  # mock
        with patch('requests.put') as mock_resp:
            context.resp_data = mock_response(context, status_code)
            context.request._put('https://example.com', context.data)
    elif request_method == RequestConst.Method.DELETE:  # mock
        with patch('requests.delete') as mock_resp:
            context.resp_data = mock_response(context, status_code)
            context.request._delete('https://example.com', context.data)
    elif request_method == RequestConst.Method.ATTACH:
        context.resp_data = context.request._attach('https://example.com', context.data)
    else:
        pass


@When('init retry_until_die method')
def step_imp(context):
    try:
        context.resp_data = context.request.retry_until_die()
    except AttributeError as e:
        context.error = e


@When('init retry_until_die method with {max_retries} {resp} {request_url} {data} {is_convert} {method}')
def step_imp(context, max_retries, resp, request_url, data, is_convert, method):
    _is_convert = True if is_convert == 'True' else False
    context.is_convert = _is_convert
    _max_retries = None if max_retries == 'None' else max_retries
    _request_url = None if request_url == 'None' else request_url
    _data = None if data == 'None' else context.data
    _method = None if method == 'None' else method
    _resp = None
    if resp == 'timeout':  # mock
        try:
            with patch('cores.utils.backend.RequestUtil.retry_until_die') as mock_exception:
                mock_exception.side_effect = requests.exceptions.RequestException("Request timeout!")
                context.resp_data = context.request.retry_until_die(int(_max_retries), _resp, _request_url, _data, _is_convert, _method)
        except Exception as e:
            context.error = e
    elif resp != 'None':
        _resp = Response()
        _resp.status_code = 200
        _resp._content = json.dumps(context.payload_data).encode()
        _resp.connection = HTTPAdapter()
        _resp.request = PreparedRequest()
        _resp.request.prepare(method=_method, url=_request_url)
        try:
            context.resp_data = context.request.retry_until_die(int(_max_retries), _resp, _request_url, _data, _is_convert, _method)
        except Exception as e:
            context.error = e
    else:
        try:
            context.resp_data = context.request.retry_until_die(int(_max_retries), _resp, _request_url, _data, _is_convert, _method)
        except Exception as e:
            context.error = e

    #########
    # ----- Then ----------
    #########


@Then('verify response is parsed completely')
def step_imp(context):
    verify = AssertUtil
    verify.true(context.parse_data)
    verify.equal(context.parse_data, context.expected_output)


@Then('verify response {status_code} is returned correctly after request')
def step_imp(context, status_code):
    _res = Response()
    _res.status_code = int(status_code)
    _res._content = json.dumps(context.data.body).encode()

    verify = AssertUtil
    if status_code == 200:
        verify.true(context.resp_data._content)
    else:
        pass
    verify.equal(_res, context.resp_data)


@Then('verify retry_until_die method response is returned error as {error_text}')
def step_imp(context, error_text):
    AssertUtil.equal(error_text, context.error)


@Then('verify retry_until_die method response is returned correctly as {status_code}')
def step_imp(context, status_code):
    verify = AssertUtil
    _res = ResponseObjModel(
        **{"status_code": int(status_code),
            "status_msg": "1",
            "message": "available",
            "response_data": {"id": 1},
            "meta_data": {"msg": "meta"}})
    if not context.is_convert:
        _res = context.payload_data
    else:
        verify.equal(context.resp_data.status_code, int(status_code))
    verify.equal(_res, context.resp_data)


@Then('verify ResponseObjModel is returned correctly')
def step_imp(context):
    verify = AssertUtil
    verify.equal(context.resp_data.status_code, 200)
    verify.equal(context.expected_output, context.resp_data)


@Then('verify request static method {url} {request_method} {is_convert} {is_locust} {error_msg}')
def step_imp(context, url, request_method, is_convert, is_locust, error_msg):
    _url = None if url == 'None' else context.default_url if url == 'default' else url
    _request_obj_model_data = None
    if request_method != 'None':
        _request_obj_model_data = context.request_obj_model_data
        _request_obj_model_data.method = request_method
    else:
        pass
    _is_convert = None if is_convert == 'None' else True if is_convert == 'True' else False
    _is_locust = None if is_locust == 'None' else True if is_locust == 'True' else False
    _error_msg = None if error_msg == 'None' else error_msg

    with patch('cores.utils.backend.RequestUtil.request') as mock_request:  # mock
        if url == 'default' and is_convert == 'None' and is_locust == 'None':
            context.resp_data = context.expected_output
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'True' and is_locust == 'None':
            context.resp_data = context.data
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'False' and is_locust == 'None':
            context.resp_data = context.expected_output
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'None' and is_locust == 'True':
            context.resp_data = context.expected_output
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'None' and is_locust == 'False':
            context.resp_data = context.expected_output
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'False' and is_locust == 'False':
            context.resp_data = context.expected_output
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        elif url == 'default' and is_convert == 'True' and is_locust == 'True':
            context.resp_data = context.data
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        else:
            pass

    if (url != 'default') or (request_method not in (RequestConst.Method.ATTACH, RequestConst.Method.DELETE, RequestConst.Method.GET, RequestConst.Method.PUT, RequestConst.Method.POST)):
        try:
            context.request.request(url=_url, data=_request_obj_model_data, is_convert=_is_convert, is_locust=_is_locust)
        except Exception as e:
            context.error = e
    else:
        pass

    verify = AssertUtil
    if _error_msg:
        verify.contain(_error_msg, str(context.error))
    else:
        expected_out = context.expected_output if is_convert != 'True' else context.data
        verify.equal(expected_out, context.resp_data)


@Then('verify _regular_request static method {url} {request_method} {is_convert} {error_msg}')
def step_imp(context, url, request_method, is_convert, error_msg):
    _url = None if url == 'None' else context.default_url if url == 'default' else url
    _request_obj_model_data = None
    if request_method != 'None':
        _request_obj_model_data = context.request_obj_model_data
        _request_obj_model_data.method = request_method
    else:
        pass
    _is_convert = None if is_convert == 'None' else True if is_convert == 'True' else False
    _error_msg = None if error_msg == 'None' else error_msg

    with patch('cores.utils.backend.RequestUtil._regular_request') as mock_request:  # mock
        if url == 'default' and is_convert == 'None':
            context.resp_data = context.expected_output
            context.request._regular_request(url=_url, data=_request_obj_model_data, is_convert=_is_convert)
        elif url == 'default' and is_convert == 'True':
            context.resp_data = context.data
            context.request._regular_request(url=_url, data=_request_obj_model_data, is_convert=_is_convert)
        elif url == 'default' and is_convert == 'False':
            context.resp_data = context.expected_output
            context.request._regular_request(url=_url, data=_request_obj_model_data, is_convert=_is_convert)
        else:
            pass

    if (url != 'default') or (request_method not in (RequestConst.Method.ATTACH, RequestConst.Method.DELETE, RequestConst.Method.GET, RequestConst.Method.PUT, RequestConst.Method.POST)):
        try:
            context.request._regular_request(url=_url, data=_request_obj_model_data, is_convert=_is_convert)
        except Exception as e:
            context.error = e
    else:
        pass

    verify = AssertUtil
    if _error_msg:
        verify.contain(_error_msg, str(context.error))
    else:
        expected_out = context.expected_output if is_convert != 'True' else context.data
        verify.equal(expected_out, context.resp_data)


@Then('verify _locust_request static method {url} {request_method} {client} {error_msg}')
def step_imp(context, url, request_method, client, error_msg):
    from locust.clients import HttpSession

    _url = None if url == 'None' else context.default_url if url == 'default' else url
    _client = None if client == 'None' else HttpSession(base_url=_url, request_event='', user='') if client == 'default' else client
    _request_obj_model_data = None
    if request_method != 'None':
        _request_obj_model_data = context.request_obj_model_data
        _request_obj_model_data.method = request_method
    else:
        pass
    _error_msg = None if error_msg == 'None' else error_msg

    with patch('cores.utils.backend.RequestUtil._locust_request') as mock_request:  # mock
        if url == 'default':
            context.resp_data = context.expected_output
            context.request._locust_request(url=_url, data=_request_obj_model_data, client=_client)
        else:
            pass

    if (url != 'default') or (request_method not in (RequestConst.Method.ATTACH, RequestConst.Method.DELETE, RequestConst.Method.GET, RequestConst.Method.PUT, RequestConst.Method.POST)):
        try:
            context.request._locust_request(url=_url, data=_request_obj_model_data, client=_client)
        except Exception as e:
            context.error = e
    else:
        pass

    verify = AssertUtil
    if _error_msg:
        verify.contain(_error_msg, str(context.error))
    else:
        verify.equal(context.expected_output, context.resp_data)
