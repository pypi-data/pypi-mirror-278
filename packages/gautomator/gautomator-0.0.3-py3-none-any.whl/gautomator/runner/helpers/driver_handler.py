import json
import os

from gautomator.const.common import EnvConst, CommonTypeUsageConst
from gautomator.const.mobile import DeviceConst, CapabilitiesConst
from gautomator.decorators import parse_driver_config, parse_app_config
from gautomator.factory.driver_factory.appium.appium_server import AppiumServer
from gautomator.factory.driver_factory.appium.mobile_driver import MobileDriver
from gautomator.factory.driver_factory.appium.virtual_device import VirtualDevice
from gautomator.factory.driver_factory.selenium.selenium_driver import InitDriver
from gautomator.model import EnvObjModel
from gautomator.utils.common.store_util import GetUtil, StoreUtil, logger
from gautomator.const.custom_exception import DriverAppError


class DriverHandler:

    @staticmethod
    def open_browser(headless: bool = True, browser: str = None) -> dict:
        """
        open a web browser for next step
        :return: driver
        """
        env_obj: EnvObjModel = GetUtil.suite_get(
            EnvConst.Environment.ENV_OBJ)
        _driver_pool: dict = {}
        try:
            _env_urls = os.getenv(EnvConst.Environment.URLS)
            _env_roles = os.getenv(EnvConst.Environment.ROLES)
            _urls = _env_urls.split(',')
            _roles = _env_roles.split(',')
        except AttributeError:
            if not _env_urls:
                raise AttributeError(f'URLS = {_env_urls} - Need "URLS" in properties file. Please re-check')
            else:
                logger.warning(f'ROLES = {_env_roles} - Need "ROLES" in properties file for multiple driver. Please re-check')

        headless = env_obj.is_headless if not headless else headless
        browser = env_obj.browser if not browser else browser
        num_of_urls = len(_urls)
        
        if not (num_of_urls > 1):
            # 1 driver handling
            driver = InitDriver.create_driver(headless, browser)
            driver.get(_urls[0] % {'env': env_obj.env})
            _driver_pool[_roles[0] if _env_roles else EnvConst.Driver.WEB_DRIVER] = driver
        else:
            # multiple driver handling
            for r, u in list(zip(_roles, _urls)):
                driver = InitDriver.create_driver(headless, browser)
                driver.get(u % {'env': env_obj.env})
                _driver_pool[r] = driver
        StoreUtil.suite_store(EnvConst.Driver.WEB_DRIVER, _driver_pool)  # for closing web drivers
        return _driver_pool

    @staticmethod
    def close_browsers():
        """
        close_browsers will close all active browsers
        """
        for driver in GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER).values():
            driver.quit()
        StoreUtil.scenario_store(EnvConst.Environment.ENV_OBJ.is_web, None)

    @staticmethod
    @parse_driver_config(os.getenv(CapabilitiesConst.PLATFORM_NAME))
    @parse_app_config(os.getenv(EnvConst.Environment.PROJECT_NAME))
    def start_mobile_driver():
        app_conf: dict = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ)
        platform_name = os.getenv(CapabilitiesConst.PLATFORM_NAME)

        if AppiumServer.start() and VirtualDevice.start(platform_name):
            if app_conf.get(DeviceConst.APP_REQUIRED).upper() == CommonTypeUsageConst.TRUE.upper():
                VirtualDevice.install_app(platform=platform_name,
                                          is_cloud_app=json.loads(app_conf.get(DeviceConst.IS_CLOUD_APP).lower()))

            driver = MobileDriver.mobile_driver_factory(platform_name=platform_name,
                                                        platform_version=os.getenv(CapabilitiesConst.PLATFORM_VERSION),
                                                        custom_opts=MobileDriver.gen_capabilities())
            StoreUtil.suite_store(EnvConst.Driver.MOBILE_DRIVER, driver)
        else:
            raise DriverAppError("Can't start driver!")
