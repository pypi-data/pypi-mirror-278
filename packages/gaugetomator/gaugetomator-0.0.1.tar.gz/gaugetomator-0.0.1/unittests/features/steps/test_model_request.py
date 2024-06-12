from gautomator.model.request import RequestObjModel
from gautomator.utils.common.assertion_util import AssertUtil

from behave import *

#########
#----- Given ----------
#########

@Given('a Request Model Object')
def step_imp(context):
    context.request = RequestObjModel()

#########
#----- Then ----------
#########
@Then('verify {key} {value} created')
def step_imp(context, key, value):
    AssertUtil.equal(getattr(context.request, key), value)

#########
#----- When ----------
#########
@When('init {key} {value} to object')
def step_imp(context, key, value):
    setattr(context.request, key, value)