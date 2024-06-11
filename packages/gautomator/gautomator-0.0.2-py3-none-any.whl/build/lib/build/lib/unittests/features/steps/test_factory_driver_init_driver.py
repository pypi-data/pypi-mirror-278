from gautomator.factory.driver_factory.selenium.selenium_driver import InitDriver
from gautomator.utils.common import AssertUtil
from gautomator.const.web.browsers_const import BrowserConst

from unittests import catch_all
from behave import * 


#########
#----- Given ----------
#########
@Given('Driver factory')
def step_imp(context):
    context.factory = InitDriver
    
#########
#----- Then ----------
#########
@then('new WebDriver object will be generated')
def step_imp(context):
    AssertUtil.true(context.driver)
    AssertUtil.equal(context.driver.__class__.__name__, 'WebDriver')
    context.driver.quit()
    
@then('It should throw an exception for browser: {browser}')
def step(context, browser):
    verify = AssertUtil
    verify.false(context.driver, f'{browser} should be banned.')
    
    
@then('new headless WebDriver object {browser} {headless} will be generated')
def step(context, browser, headless):
    verify = AssertUtil
    if browser == BrowserConst.CHROME:
        expected_result = context.driver.capabilities.get('browserName')
    elif browser == BrowserConst.FIREFOX:
        expected_result = context.driver.capabilities.get('moz:headless')
    if headless.lower() == 'true':
        verify.true('headless' in expected_result) if browser == BrowserConst.CHROME else verify.true(expected_result)
    else:
        verify.true(browser in expected_result) if browser == BrowserConst.CHROME else verify.false(expected_result)
    context.driver.quit()
    
@then('the {browser} driver created with expected capabilities')
def step_imp(context, browser):
    verify = AssertUtil
    actual_result: dict = context.driver.capabilities
    verify.equal(actual_result.get('pageLoadStrategy'),'normal', message=f'pageLoadStrategy of {browser} is wrong.')
    if browser == BrowserConst.CHROME:
        verify.true(actual_result.get(f'{browser}'), message=f'{actual_result}')
    else:
        AssertionError(f'Only support {BrowserConst.CHROME} or {BrowserConst.FIREFOX}')
    context.driver.quit()
    
#########
#----- When ----------
#########
@When('creating a new driver with default params')
@catch_all
def step_imp(context):
    context.driver = context.factory.create_driver()
    
@When('creating a new driver with headless option {browser} {headless}')
@catch_all
def step_imp(context, browser, headless):
    context.driver = context.factory.create_driver(headless=False if headless.lower() == 'false' else True, browser=browser)
    
@When('creating a new driver with unsupport browser {browser}')
def step_imp(context, browser):
    context.driver = context.factory.create_driver(browser=browser)
    