from datetime import datetime

from nimbletl.log_drive.log_drive_common import check_etl_is_running_and_warning, set_log_success
from nimbletl.log_drive.time_windows import get_sorted_unexecuted_for_time_window_2_param, save_log_for_time_window_2_param

etl_name = 'flask_test_etl'
start_datetime = datetime(2024, 6, 10, 0, 0, 0)
time_interval = 1440
target_table_name = 'test_table_name'
drive_type = 'time_window_2_param'

if __name__ == '__main__':
    # check数据是否正在运行中
    check_etl_is_running_and_warning(etl_name)

    # 获取待执行的datatime tuple list
    datetime_list = get_sorted_unexecuted_for_time_window_2_param(etl_name, start_datetime, time_interval)

    for datetime_tmp in datetime_list:
        log_id = save_log_for_time_window_2_param(etl_name, datetime_tmp, target_table_name, drive_type)
        print('etl process ...')
        set_log_success(log_id)


