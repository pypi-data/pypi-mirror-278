from gautomator.utils.common.time_util import TimeUtil
from gautomator.utils.common.assertion_util import AssertUtil

from gautomator.const.common.times_const import TimeConst

import calendar
import datetime
from behave import *
#########
#----- Given ----------
#########

@Given('a TimeUtil func')
def step_imp(context):
    context.time_util = TimeUtil
    
#########
#----- When ----------
#########
@When('generating begining and last day of a month {month} with current year')
def step_imp(context, month: int):
    context.output = context.time_util.get_begin_and_last_date_of_month(month=int(month))

@When('generating begining and last day of a month {month} and year {year}')
def step_imp(context, month: int, year: int):
    context.output = context.time_util.get_begin_and_last_date_of_month(month=int(month), year=int(year))

#########
#----- Then ----------
#########

@Then('verify output will be as formatted with {month} and {year}')
def step_imp(context, month, year):
    verify = AssertUtil
    verify.true(context.output)
    verify.equal(actual_value=context.output[0], 
                 expected_value=datetime.date(int(year), int(month), 1).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY))
    verify.equal(actual_value=context.output[1], 
                expected_value=datetime.date(int(year), int(month),  calendar.monthrange(int(year), int(month))[1]).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY))
    
@Then('verify output will be as formatted with {month} in current year')
def step_imp(context, month):
    year = datetime.datetime.now().year
    verify = AssertUtil
    verify.true(context.output)
    verify.equal(actual_value=context.output[0], 
                 expected_value=datetime.date(int(year), int(month), 1).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY))
    verify.equal(actual_value=context.output[1], 
                expected_value=datetime.date(int(year), int(month),  calendar.monthrange(int(year), int(month))[1]).strftime(TimeConst.Format.FORMAT_DD_MM_YYYY))