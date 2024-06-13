import datetime
from dataclasses import dataclass
from os import path

import pandas as pd
import pandas.testing as pd_testing
import uuid
import time

import pytz
from numpy import NaN

from ..kawa_base_e2e_test import KawaBaseTest

class TestPythonColumns(KawaBaseTest):

    def test_that_python_column_is_correctly_computed_case_with_no_pk_in_param_of_script(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_no_pk_in_params',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              sleep_time_before_checking_status=3)

    def test_that_python_column_is_correctly_computed_case_with_no_pk_in_param_of_script_with_a_date_pk(self):
        df_for_datasource = pd.DataFrame([
            {'pk': datetime.date(2024, 1, 1), 'measure1': 1.1, 'measure2': 2.2},
            {'pk': datetime.date(2024, 1, 2), 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': datetime.date(2024, 1, 1), 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': datetime.date(2024, 1, 2), 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_no_pk_in_params',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              sleep_time_before_checking_status=3)

    def test_that_python_column_is_correctly_computed_case_with_no_pk_in_param_of_script_with_a_datetime_pk(self):
        df_for_datasource = pd.DataFrame([
            {'pk': at_berlin(datetime.datetime(2024, 1, 1, 1)), 'measure1': 1.1, 'measure2': 2.2},
            {'pk': at_berlin(datetime.datetime(2024, 1, 1, 2)), 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': at_berlin(datetime.datetime(2024, 1, 1, 1)), 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': at_berlin(datetime.datetime(2024, 1, 1, 2)), 'measure1': 11.11, 'measure2': 22.22,
             'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_no_pk_in_params',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              sleep_time_before_checking_status=3)

    def test_that_python_column_using_all_types(self):
        df_for_datasource = pd.DataFrame([
            all_type_row(0, 1.1, 1, datetime.date(2024, 7, 14), datetime.datetime(2024, 7, 14, 14, 7, 0), True, 'true'),
            all_type_row(1, 2.2, 2, datetime.date(2024, 7, 15), datetime.datetime(2024, 7, 15, 14, 7, 0), False,
                         'false')
        ]
        )
        row1 = all_type_row(0, 1.1, 1, datetime.date(2024, 7, 14), datetime.datetime(2024, 7, 14, 14, 7, 0), True,
                            'true')
        row1.update(
            all_type_row_res(2.2, 2, datetime.date(2024, 7, 15),
                             datetime.datetime(2024, 7, 14, 15, 7, 0), False,
                             'True__T__'))
        row2 = all_type_row(1, 2.2, 2, datetime.date(2024, 7, 15), datetime.datetime(2024, 7, 15, 14, 7, 0), False,
                            'false')
        row2.update(
            all_type_row_res(3.3, 3, datetime.date(2024, 7, 16),
                             datetime.datetime(2024, 7, 15, 15, 7, 0), True,
                             'False__T__'))
        indicator_for_param_mapping = ['decimal', 'integer', 'date', 'date_time', 'boolean', 'text']
        expected_df = pd.DataFrame([row1, row2])
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_script_with_all_types',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              sleep_time_before_checking_status=3,
                                              secrets={'secret_name_in_kawa': '__T__'})

    def test_that_python_column_is_correctly_computed_case_with_pk_in_param_of_script(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['pk', 'measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_pk_in_params',
                                              indicator_for_param_mapping,
                                              expected_df)

    def test_that_logs_are_accessible_for_the_python_columns(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_no_pk_in_params_with_logging',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              logs='Computing the df hahahahahahahahah')

    def test_that_python_column_is_correctly_computed_case_with_two_pk__only_one_in_param_of_script(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'pk2': 0, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'pk2': 1, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['pk', 'measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'pk2': 0, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': 2, 'pk2': 1, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk', 'pk2'],
                                              'test_python_columns_with_pk_in_params',
                                              indicator_for_param_mapping,
                                              expected_df)

    def test_multi_user_python_column_usage(self):
        # First user 1 create DS, sheet, layout, script and compute it.
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 3.3},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 33.33}]
        )
        test_result = self.run_test_python_column_execution(df_for_datasource,
                                                            ['pk'],
                                                            'test_python_columns_with_no_pk_in_params',
                                                            indicator_for_param_mapping,
                                                            expected_df)

        # Now user 2 computes the shared layout, he should see the 'measure3' column, but with no values
        second_user_computation_res = self.kawa_second_user.sheet().view_id(test_result.default_layout_id).compute()
        expected_df_second_user = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': NaN},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': NaN}]
        )
        pd_testing.assert_frame_equal(second_user_computation_res, expected_df_second_user)

        # When: User 2 launches a script compute
        self.commands_second_user.start_python_private_join(test_result.python_private_join['id'])
        time.sleep(2)
        second_user_computation_res_after_script_execution = self.kawa_second_user.sheet() \
            .view_id(test_result.default_layout_id).compute()

        # Then user 2 should see the expected df with the 'measure3' computed values
        pd_testing.assert_frame_equal(second_user_computation_res_after_script_execution, expected_df)

    def test_script_execution_with_secret(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': 11.1},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': 21.11}]
        )

        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_secret',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              {'delta_in_letters': '10_letters'})

    def test_script_with_error(self):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        indicator_for_param_mapping = ['measure1', 'measure2']
        expected_df = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2, 'measure3': None},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22, 'measure3': None}]
        )

        self.run_test_python_column_execution(df_for_datasource,
                                              ['pk'],
                                              'test_python_columns_with_error_when_executing',
                                              indicator_for_param_mapping,
                                              expected_df,
                                              expected_end_status='FAILURE',
                                              expected_end_error='Test error hohoho',
                                              sleep_time_before_checking_status=40,
                                              logs='Test error hohoho')

    def test_should_throw_when_creating_script_with_two_functions_with_input_defined(self):
        self.assertRaisesRegex(Exception,
                               'The python script provided contain more than one function with defined inputs',
                               self.create_script_test, 'test_script_with_two_functions_will_throw_error')

    def test_should_throw_when_creating_script_with_missing_arguments(self):
        self.assertRaisesRegex(Exception,
                               'Some arguments defined in the main function: execute are not defined. The list :'
                               ' {\'missing_param\'}.',
                               self.create_script_test, 'test_script_with_missing_arguments_will_throw_error')

    def test_should_throw_when_creating_script_without_any_function_with_defined_inputs(self):
        self.assertRaisesRegex(Exception,
                               'The python script provided does not contain any function with inputs defined with the'
                               ' @inputs decorator',
                               self.create_script_test, 'test_script_without_any_function_with_inputs')

    def add_private_join_indicators_to_sheet(self, layout_id, link_id, outputs: list):
        return self.kawa.commands._run_command(command_name='AddFieldsToLayout',
                                               command_parameters={
                                                   'layoutId': layout_id,
                                                   'fieldList': [
                                                       {
                                                           'aggregationMethod': 'FIRST',
                                                           'columnId': '{}⟶{}'.format(link_id, output),
                                                           'displayInformation': {
                                                               'displayName': output
                                                           }
                                                       }
                                                       for output in outputs
                                                   ]
                                               })

    def create_script_test(self,
                           script_file_name):
        df_for_datasource = pd.DataFrame([
            {'pk': 1, 'measure1': 1.1, 'measure2': 2.2},
            {'pk': 2, 'measure1': 11.11, 'measure2': 22.22}]
        )
        pks = ['pk']
        ref = uuid.uuid4()
        ds_unique_name = 'python_columns_test_{}'.format(ref)

        loader = self.kawa.new_data_loader(df=df_for_datasource, datasource_name=ds_unique_name)
        ds = loader.create_datasource(primary_keys=pks)
        loader.load_data(reset_before_insert=True, create_sheet=True)

        sheet = self.kawa.entities.sheets().get_entity(ds_unique_name)
        sheet_id = sheet['id']
        default_layout_id = sheet['defaultLayoutId']
        status = self.get_private_join_sheet_statuses(sheet_id)
        self.assertTrue(len(status) == 0)

        # share sheet and layout
        self.commands.share_sheet_and_layouts(sheet_id, [default_layout_id])

        # setup script
        script_name = 'script_{}'.format(ref)

        current_file_path = path.dirname(__file__)
        rel_path = 'resources/{}.py'.format(script_file_name)
        abs_file_path = path.join(current_file_path, rel_path)

        text_file = open(abs_file_path, 'r')
        script_content = text_file.read()
        text_file.close()
        self.commands.create_script(script_name, script_content)

    def run_test_python_column_execution(self,
                                         df_for_datasource,
                                         pks,
                                         script_file_name,
                                         indicator_for_param_mapping,
                                         expected_df,
                                         secrets=None,
                                         expected_end_status='SUCCESS',
                                         expected_end_error='',
                                         sleep_time_before_checking_status=5,
                                         logs=None):
        # setup datasource / sheet / grid
        ref = uuid.uuid4()
        if secrets is None:
            secrets = {}
        ds_unique_name = 'python_columns_test_{}'.format(ref)

        loader = self.kawa.new_data_loader(df=df_for_datasource, datasource_name=ds_unique_name)
        ds = loader.create_datasource(primary_keys=pks)
        datasource_id = ds['id']
        loader.load_data(reset_before_insert=True, create_sheet=True)

        sheet = self.kawa.entities.sheets().get_entity(ds_unique_name)
        sheet_id = sheet['id']
        default_layout_id = sheet['defaultLayoutId']
        status = self.get_private_join_sheet_statuses(sheet_id)
        self.assertTrue(len(status) == 0)

        # share sheet and layout
        self.commands.share_sheet_and_layouts(sheet_id, [default_layout_id])

        # setup script
        script_name = 'script_{}'.format(ref)
        current_file_path = path.dirname(__file__)
        rel_path = 'resources/{}.py'.format(script_file_name)
        abs_file_path = path.join(current_file_path, rel_path)

        text_file = open(abs_file_path, 'r')
        script_content = text_file.read()
        text_file.close()
        script = self.commands.create_script(script_name, script_content)

        # add secrets
        if secrets:
            for k, v in secrets.items():
                self.commands.create_secret_if_not_exist(k, v, k)

        # setup private join
        script_id = script.get('id')

        python_private_join_name = 'private_join_{}'.format(ref)
        param_mapping = ['{}⟶{}'.format(datasource_id, indicator) for indicator in indicator_for_param_mapping]
        python_private_join = self.commands.create_python_private_join(python_private_join_name,
                                                                       sheet_id,
                                                                       default_layout_id,
                                                                       script_id,
                                                                       param_mapping)

        # add output from script to view
        join_datasource_id = python_private_join['joinDatasourceId']
        sheet_with_private_join = self.kawa.entities.sheets().get_entity(ds_unique_name)
        status = self.get_private_join_sheet_statuses(sheet_id)
        self.assertTrue(len(status) == 1)
        self.assertTrue(status[0]['pythonPrivateJoinJobStatus'] == 'MISSING_EVENT')

        script_run_histo = self.get_script_run_history(script_id)
        self.assertTrue(len(script_run_histo) == 0)

        private_join_datasource_link = [link for link in sheet_with_private_join['dataSourceLinks'] if
                                        link['targetDataSourceId'] == join_datasource_id][0]

        outputs = [output['name'] for output in script['scriptMetadata']['outputs']]
        self.add_private_join_indicators_to_sheet(default_layout_id,
                                                  private_join_datasource_link['uniqueId'],
                                                  outputs)

        self.commands.save_layout(default_layout_id)

        # when executing script
        self.commands.start_python_private_join(python_private_join['id'])

        time.sleep(sleep_time_before_checking_status)

        # then
        status = self.get_private_join_sheet_statuses(sheet_id)
        self.assertTrue(len(status) == 1)
        self.assertTrue(status[0]['pythonPrivateJoinJobStatus'] == expected_end_status)
        self.assertTrue(expected_end_error in status[0].get('errorMessage', ''))

        script_run_histo_end = self.get_script_run_history(script_id)
        self.assertTrue(len(script_run_histo_end) == 1)
        self.assertTrue(script_run_histo_end[0]['status'] == expected_end_status)
        self.assertTrue(expected_end_error in script_run_histo_end[0].get('errorMessage', ''))

        # if not FAILURE check the script data
        if expected_end_status != 'FAILURE':
            computed_with_script_executed_df = self.kawa.sheet(force_tz='Europe/Berlin').view_id(
                default_layout_id).compute()
            pd_testing.assert_frame_equal(computed_with_script_executed_df.sort_index(axis=1),
                                          expected_df.sort_index(axis=1),
                                          check_dtype=False)

        if logs:
            job_execution_id = script_run_histo_end[0].get('jobExecutionId')
            logs_from_server = self.get_job_log(job_execution_id['relatedEntityId'], job_execution_id['contextId'])
            self.assertTrue(logs in logs_from_server)

        return TestResult(python_private_join, ref, datasource_id, default_layout_id, sheet_id)

    def get_private_join_sheet_statuses(self, sheet_id: str) -> list:
        return self.kawa.get(
            '{}/backoffice/sheets/{}/python-private-joins-current-status'.format(self.kawa.kawa_api_url, sheet_id))

    def get_script_run_history(self, script_id: str) -> list:
        return self.kawa.get(
            '{}/backoffice/scripts/{}/run-history'.format(self.kawa.kawa_api_url, script_id))

    def get_job_log(self, entity_id: str, execution_id: str) -> str:
        return self.kawa.get(
            '{}/backoffice/joblog/{}/{}'.format(self.kawa.kawa_api_url, entity_id, execution_id)).get('log', '')


@dataclass
class TestResult:
    """Class for keeping track of an item in inventory."""
    python_private_join: dict
    ref: uuid.UUID
    datasource_id: str
    default_layout_id: str
    sheet_id: str


def all_type_row(pk: int, f: float, i: int, d: datetime.date, dt: datetime.datetime, b: bool, s: str) -> dict:
    return {'pk': pk, 'decimal': f, 'integer': i, 'date': d, 'date_time': pytz.timezone('Europe/Berlin').localize(dt),
            'boolean': b, 'text': s}


def all_type_row_res(f: float, i: int, d: datetime.date, dt: datetime.datetime, b: bool, s: str) -> dict:
    return {'decimal_res': f, 'integer_res': i, 'date_res': d,
            'datetime_res': pytz.timezone('Europe/Berlin').localize(dt), 'boolean_res': b, 'text_res': s}


def at_berlin(dt: datetime.datetime):
    return pytz.timezone('Europe/Berlin').localize(dt)
