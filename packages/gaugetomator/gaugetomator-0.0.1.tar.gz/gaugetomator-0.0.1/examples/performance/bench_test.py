from gautomator.utils.common import AssertUtil, logger
from gautomator.utils.backend import RequestUtil
from gautomator.const.api.request import RequestConst
from gautomator.factory.request_factory import RequestFactory

from locust import task, HttpUser, between

class BenchTest(HttpUser):
    wait_time = between(1, 5)
    is_perf = True
    
    @task
    def bench_create_pet(self):
        data = RequestFactory().create_request(request_type=RequestConst.Method.GET)
        r = RequestUtil.request(url='https://petstore.swagger.io/v2/user/login?username=dale&password=dale', data=data, is_locust=self.is_perf, client=self.client)
        AssertUtil.equal(r.status_code, RequestConst.StatusCode.OK)
    