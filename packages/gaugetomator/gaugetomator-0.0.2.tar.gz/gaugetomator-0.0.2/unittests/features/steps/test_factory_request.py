from gautomator.factory.request_factory import RequestFactory
from gautomator.utils.common import AssertUtil
from unittests import catch_all

from behave import * 

#########
#----- Given ----------
#########

@Given('a request factory')
def step_imp(context):
    context.factory = RequestFactory()
    
#########
#----- Then ----------
#########
@then('new object will be generated')
def step_imp(context):
    AssertUtil.true(context.request)
    
@then('new request will be generated as RequestObjectModel')
def step_imp(context):
    AssertUtil.equal('RequestObjModel', context.request.__str__())
    
@then('new request will have content {content}')
def step_imp(context, content):
    AssertUtil.equal(context.request.header, content)
    
@then('It should throw an exception for {request}')
def step(context, request):
    verify = AssertUtil
    verify.equal(context.exc, f'Do not support this method {request}')


#########
#----- When ----------
#########
@When('sending a {request} to factory')
@catch_all
def step_imp(context, request):
    context.request = context.factory.create_request(request)
    