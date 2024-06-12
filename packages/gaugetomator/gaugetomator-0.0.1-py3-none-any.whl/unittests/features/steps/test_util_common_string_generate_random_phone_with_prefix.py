from gautomator.utils.common import StringUtil, AssertUtil

from behave import *
import random

#########
#----- Given ----------
#########

@Given('a StringUtil func')
def step_imp(context):
    context.string_util = StringUtil
    
#########
#----- When ----------
#########
@When('generating new phone number with {prefix}')
def step_imp(context, prefix):
    context.output = context.string_util.generate_random_phone_with_prefix(prefix)

#########
#----- Then ----------
#########
@Then('verify phone generated successfully with correct length format = {length}')
def step_imp(context, length):
    verify = AssertUtil
    verify.true(context.output)
    verify.equal(len(context.output), length , context.output)

@Then('Run the init script 1k times and make sure the length format still equal 10')
def step_imp(context):
    verify=AssertUtil
    prefix = ['090','093', '091','098', '097']
    for _ in range(1000):
        context.output = context.string_util.generate_random_phone_with_prefix(prefix=random.choice(prefix))
        verify.equal(len(context.output), 10, context.output)