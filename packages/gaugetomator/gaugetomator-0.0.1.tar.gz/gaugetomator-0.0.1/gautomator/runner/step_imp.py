import os

from getgauge.python import data_store, before_scenario, before_suite, before_spec, after_suite, after_spec, \
    after_scenario, after_step

from gautomator.const.api import APIConst
from gautomator.const.common import CommonTypeUsageConst, EnvConst
from gautomator.const.mobile import CapabilitiesConst
from gautomator.factory.driver_factory.appium.appium_server import AppiumServer
from gautomator.factory.driver_factory.appium.virtual_device import VirtualDevice
from gautomator.model import EnvObjModel
from gautomator.utils.backend.data_setup_util import DataSetup
from gautomator.utils.backend.swagger_parser_util import SwaggerUtil
from gautomator.utils.common import logger, GetUtil, StoreUtil
from .helpers.driver_handler import DriverHandler
from .helpers.setup import CommonUsage
from ..factory.driver_factory import AppHelper


def __mapping_platform(key: str) -> int:
    _d = {
        'ios': 1,
        'android': 2,
        'web': 3,
        'api': 4,
        'integration': 5
    }
    return _d.get(key)


def suite_set_up():
    """
        This wrapper will run first and check all environments define in config file
        It will double-check the config and setup the env to execute test.
        e.g.
        if is_api:
            ==> We will execute api test
        if is_web:
            ==> We will execute web test
        if is_mobile:
          ==> execute mobile test: ios or android
        if is_e2e:
          ==> execute combination test on all platforms

    """
    env: str = os.getenv(EnvConst.Environment.ENV)
    is_api: bool = True if os.getenv(
        EnvConst.Configuration.IS_API) == CommonTypeUsageConst.TRUE else False
    is_web: bool = True if os.getenv(
        EnvConst.Configuration.IS_WEB) == CommonTypeUsageConst.TRUE else False
    is_e2e: bool = True if os.getenv(
        EnvConst.Configuration.IS_E2E) == CommonTypeUsageConst.TRUE else False
    is_mobile: bool = True if os.getenv(EnvConst.Configuration.IS_IOS) \
        or os.getenv(EnvConst.Configuration.IS_ANDROID) == CommonTypeUsageConst.TRUE else False

    is_headless: bool = True if os.getenv(
        EnvConst.Configuration.IS_HEADLESS) == CommonTypeUsageConst.TRUE else False
    is_testlink: bool = True if os.getenv(
        EnvConst.Configuration.IS_TEST_LINK) == CommonTypeUsageConst.TRUE else False
    api_key: str = None
    api_name: str = None
    browser: str = os.getenv(EnvConst.Environment.BROWSER)
    project_name: str = os.getenv(EnvConst.Environment.PROJECT_NAME)
    base_api_url = os.getenv(APIConst.API_URL)
    api_key = os.getenv(APIConst.API_KEY)
    api_name = os.getenv(APIConst.API_NAME)
    token: str = ''
    platform: str = ''
    version: str = ''
    url: str = ''
    base_domain: str = ''
    log_level: str = os.getenv(EnvConst.Environment.LOG_LEVEL).upper() \
        if os.getenv(EnvConst.Environment.LOG_LEVEL) else EnvConst.Logger.INFO
    platform_id = __mapping_platform(platform)
    # flag = True if (os.getenv(EnvironmentConst.Environment.TOKEN) != CommonTypeUsageConst.FALSE
    #                 or not os.getenv(EnvironmentConst.Environment.TOKEN)) else False
    # if is_api:
    #     token = CommonUsage.__generate_token()
    # else:
    #     pass
    if is_api:
        url = os.getenv(EnvConst.Environment.BASE_URL) % {'env': env} if os.getenv(EnvConst.Environment.BASE_URL) else None
    _d = dict(env=env,
              project_name=project_name,
              base_url=url,
              base_api_url=base_api_url,
              browser=browser,
              log_level=log_level,
              is_api=is_api,
              is_web=is_web,
              is_mobile=is_mobile,
              is_headless=is_headless,
              is_testlink=is_testlink,
              is_e2e=is_e2e,
              api_key=api_key,
              api_name=api_name,
              token=token,
              ms_projects=project_name,
              base_domain=base_domain,
              platform_id=platform_id)
    StoreUtil.suite_store(keyword=EnvConst.Environment.ENV_OBJ,
                          data=EnvObjModel(**_d))

    print("\t INFORMATION")
    print("\t -----------")
    print(f"\t * Test Environment: {env}")
    print(f"\t * Project Name: {project_name}")
    if url:
        print(f"\t * Test URL: {url}")
    if platform:
        print(f"\t * Platform: {platform}")
    if version:
        print(f"\t * Version: {version}")
    data_store.suite.dict_test_cases_result = []
    if not (is_api or is_web or is_mobile):
        logger.warning("Not Support!")
    else:
        if is_testlink:
            CommonUsage.test_link_generator()
        if is_api:  # api case
            _swagger_url = os.getenv(APIConst.SWAGGER_URL)
            if _swagger_url:
                SwaggerUtil.parsing_swagger(
                    url=_swagger_url, is_gitlab=True if os.getenv(APIConst.IS_GITLAB) == CommonTypeUsageConst.TRUE else False, prj_name=project_name)
        if is_web:  # Web test
            DataSetup.set_up_data()
            DriverHandler.open_browser(headless=is_headless, browser=browser)
        if is_mobile:  # Mobile test
            # DataSetup.set_up_data()
            DriverHandler.start_mobile_driver()  # Install and open application
        if is_e2e:
            pass


def suite_teardown():
    """
        This wrapper will help to clean all stored data withing suite level.
        if mobile or web testing, we will also close and quit all drivers
    """
    logger.debug("\n\t SUITE TEARDOWN")
    env_obj: EnvObjModel = GetUtil.suite_get(EnvConst.Environment.ENV_OBJ)
    drivers = list()
    if env_obj.is_web:
        if GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER):
            for driver in GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER).values():  # GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER) returned dict
                drivers.append(driver)
        else:
            logger.error('No driver created')
    else:
        pass
    if env_obj.is_mobile:
        drivers.append(GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER))
    else:
        pass

    if drivers:
        if env_obj.is_mobile:
            is_removed = False  # hard code for remove app before suite
            if not is_removed:
                VirtualDevice.uninstall_app(platform=os.getenv(CapabilitiesConst.PLATFORM_NAME))
        try:
            for d in drivers:
                d.quit()
        except Exception as e:
            logger.error(e)
        finally:
            if env_obj.is_mobile:
                AppiumServer.stop()
                VirtualDevice.stop(os.getenv(CapabilitiesConst.PLATFORM_NAME))
    rs: list = [i for i in data_store.suite.dict_test_cases_result]
    if len(rs):
        msg = '|'.join(','.join(sublist) for sublist in rs)
        logger.info(f"Running failed case ids: {msg}")
    data_store.suite.clear()


def spec_teardown():
    data_store.spec.clear()


def scenario_teardown():
    """
    This wrapper will help to clean all stored data withing scenario level
    """

    def __close_multi_tabs(driver):
        tabs = driver.window_handles
        if len(tabs) > 1:
            logger.info(f"\t SCENARIO: Close {len(tabs) - 1} tabs")
            for tab in tabs[1:]:
                driver.switch_to.window(tab)
                driver.close()
            driver.switch_to.window(tabs[0])

    if GetUtil.suite_get(keyword=EnvConst.Environment.ENV_OBJ).is_web:
        logger.info("\t SCENARIO: Reset browser")
        for driver in GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER).values():
            __close_multi_tabs(driver)
            driver.delete_all_cookies()
            driver.get(driver.current_url)

    if GetUtil.suite_get(keyword=EnvConst.Environment.ENV_OBJ).is_api:
        pass
    if GetUtil.suite_get(keyword=EnvConst.Environment.ENV_OBJ).is_mobile:
        app_package = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ).get(CapabilitiesConst.APP_PACKAGE)
        driver = GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER)
        app_helper = AppHelper(driver)

        app_helper.clear_app(app_id=app_package)
        app_helper.set_permission(permissions="all", app_id=app_package)
        app_helper.activate_app(app_id=app_package)
    data_store.scenario.clear()


@before_suite
def before_suite_hook():
    suite_set_up()


@after_suite
def after_suite_hook():
    suite_teardown()


@after_spec
@before_spec
def after_spec_hook():
    spec_teardown()


@after_step
def after_every_step(context):
    try:
        if context._ExecutionContext__step._Step__is_failing:
            pre = data_store.suite.error_message
            error_message = context._ExecutionContext__step._Step__error_message
            step_text = context._ExecutionContext__step._Step__text
            data_store.suite.error_message = f"{pre}\n{step_text}\n{error_message}"
            # You can now work with the error_message as needed, such as logging or reporting it
    except Exception as e:
        logger.error(e)


@after_scenario
def after_scenario_hook(context):
    """ Remove id is duplicated when retry by gauge command"""
    is_spec_failed = context._ExecutionContext__specification._Specification__is_failing
    is_failing = context._ExecutionContext__scenario._Scenario__is_failing
    test_id_tag = context.scenario.tags
    tcs_rs = data_store.suite.dict_test_cases_result
    """ Check tag id is valid"""
    # if test_id_tag[1:].isnumeric():
    """ If test case is failed, add to list else remove it if it retry success"""
    if is_failing and is_spec_failed:
        if test_id_tag not in tcs_rs:
            tcs_rs.append(test_id_tag)
    elif not is_failing and test_id_tag in tcs_rs:
        tcs_rs.remove(test_id_tag)
    data_store.suite.dict_test_cases_result = tcs_rs
    scenario_teardown()


@before_scenario
def before_scenario_hook(context):
    data_store.scenario.clear()
    # if GetUtil.suite_get(keyword=EnvironmentConst.Environment.ENV_OBJ).is_testlink:
    #     test_id_tag = context.scenario.tags[-1]

    #     if test_id_tag[1:].isnumeric() or test_id_tag[2:].isnumeric():
    #         try:
    #             test_case = AddRemoveTestCase(
    #                 project_id=data_store.suite.project_id, test_plan_id=data_store.suite.test_plan_id)
    #             test_case.add_all_test_cases_to_test_plan(
    #                 test_case_external_ids=[test_id_tag])
    #         except Exception as err:
    #             logger.warning(
    #                 TestLinkConst.ERROR_ADD_TC_EXECUTE_STATUS.format(err))
