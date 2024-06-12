from getgauge.python import ExecutionContext, data_store
import os

from gautomator.utils.testlink import BaseTestLink, TestPlan, Build
from gautomator.utils.backend import SwaggerUtil
from gautomator.utils.common import logger,TimeUtil

from gautomator.factory.database_factory.database_conn_generator import PostgresQuery

from gautomator.const.common import EnvConst as const, CommonTypeUsageConst, TestLinkMsgConst, TimeConst


class CommonUsage:

    @staticmethod
    def generate_token(env: str, user_type: str, flag: bool, token_url: str, url: str, swagger_url: str,
                         project_name: str):
        if not env or env.lower() not in (const.Environment.PROD_ENV
                                          or const.Environment.UAT_ENV):
            env = const.Environment.SIT_ENV
        elif env == const.Environment.UAT_ENV:
            env = const.Environment.PROD_ENV
        elif env in const.Environment.PROD_ENV:
            env = const.Environment.PROD_ENV
        # if initialize_flow_url:
        #     initialize_flow_url = initialize_flow_url.format(env=env)
        SwaggerUtil.parsing_swagger(url=swagger_url, is_gitlab=flag, prj_name=project_name)
        # return GenerateToken(env=env, token_url=token_url, url=url).get_session_token(is_ignore=flag)
        return True

    @staticmethod
    def testlink_generator():
        test_link_test_plan_name = os.getenv(
            const.Testlink.TL_TEST_PLAN_NAME)
        test_link_project_name = os.getenv(
            const.Testlink.TL_PROJECT_NAME)
        data_store.suite.error_message = CommonTypeUsageConst.EMPTY
        test_plan_name = f"{test_link_test_plan_name}_{TimeUtil.get_current_date_time(datetime_format=TimeConst.Format.FORMAT_DD_MM_YYYY_H_M_S_FILE)}"

        # create test plan follow to sprint
        try:
            base_test_link = BaseTestLink()
            project_id = base_test_link.get_project_id_by_project_name(
                project_name=test_link_project_name)
            data_store.suite.project_id = project_id
        except Exception as err:
            logger.warning(TestLinkMsgConst.ERROR_GET_PROJECT_ID.format(
                test_link_project_name, err))

        try:
            TestPlan.create_new_test_plan(project_name=test_link_project_name,
                                          test_plan_name=test_plan_name)
            test_plan_id = TestPlan.get_test_plan_by_project_name(
                project_name=test_link_project_name, test_plan_name=test_plan_name)
            data_store.suite.test_plan_id = test_plan_id
            data_store.suite.test_plan_name = test_plan_name
        except Exception as err:
            test_plan_id = None
            logger.warning(TestLinkMsgConst.ERROR_GET_TESTPLAN_NAME.format(
                test_link_project_name, err))

        try:
            build_name = os.getenv(const.Environment.BUILD_NAME)
            if test_plan_id:
                build = Build(test_plan_id=test_plan_id)
                build_info = build.create_new_build_version(
                    build_name=build_name)
                data_store.suite.build_name = build_name
                data_store.suite.build_id = build_info[0]["id"]
        except Exception as err:
            logger.warning(err)
            # logger.warning(
            #     TestLinkConst.ERROR_CREATE_BUILD.format(test_plan_name, err))
