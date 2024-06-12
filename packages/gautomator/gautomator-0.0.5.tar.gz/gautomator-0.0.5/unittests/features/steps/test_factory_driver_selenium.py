from gautomator.factory.driver_factory import SeleniumDriver
from gautomator.factory.driver_factory.selenium.selenium_driver import InitDriver
from gautomator.utils.common import AssertUtil
from unittests import catch_all

from behave import * 

#########
#----- Given ----------
#########

@Given('a Selenium Driver')
def step_imp(context):
    context.init_driver = InitDriver.create_driver()
    context.driver = SeleniumDriver(context.init_driver)


#########
#----- When ----------
#########
@when('adding selenium driver to Driver Factory')
def step_imp(context):
    context.sel_driver = SeleniumDriver(context.driver)
    
@when('closing the browser')
def step_imp(context):
    context.sel_driver.close_driver()
    

#########
#----- Then ----------
#########

@then('New Selenium Driver will be generated')
def step_imp(context):
    verify = AssertUtil
    verify.true(context.sel_driver)
    # context.init_driver.quit()

@then('It should throw an exception for invalid Sel Driver')
@catch_all
def step_imp(context):
    verify = AssertUtil
    verify.equal(context.exc, f'Invalid Sel Driver')

@then('Defautl driver timeout will be 10')
@catch_all
def step_imp(context):
    verify = AssertUtil
    verify.equal(context.sel_driver.TIMEOUT, 10)
    context.init_driver.quit()
    
@then('modify_pom_locator function will be accessible')
def step_imp(context):
    verify = AssertUtil
    verify.true(context.sel_driver.modify_pom_locator())
    context.init_driver.quit()

@then('browser should be closed')
def step_imp(context):
    pass
    # verify = AssertUtil
    # verify.false(context.sel_driver.current_url)