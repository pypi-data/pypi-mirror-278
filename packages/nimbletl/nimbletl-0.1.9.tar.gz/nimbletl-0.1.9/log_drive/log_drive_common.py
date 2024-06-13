from common.nimbletl_db import get_dataframe
from common.nimble_exception import EtlIsRunningException


def check_etl_is_running_and_warning(etl_name: str):
    if _check_etl_is_running(etl_name):
        raise EtlIsRunningException(f'[etl_name] ETL正在执行中...')


def _check_etl_is_running(etl_name: str) -> bool:
    """
    判断当前对应的ETL是否有在执行中
    :return:
    """
    last_etl_job_result_str = f'''
        SELECT top 1 etl_result
        FROM log_drive_table
        WHERE etl_name = '{etl_name}'
        order by id desc;
    '''
    result_df = get_dataframe(last_etl_job_result_str)
    if result_df.empty:
        return False
    return result_df['etl_result'][0] == 2


def save_log():
    pass


def set_log_success():
    pass


def set_log_failed():
    pass
