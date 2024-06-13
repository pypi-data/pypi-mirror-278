import os

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as PyEnum
from datetime import datetime

def _get_drive_db_url():
    db_user = os.getenv('LOG_DRIVE_DB_USER', 'root')
    db_password = os.getenv('LOG_DRIVE_DB_PASSWORD', '')
    db_host = os.getenv('LOG_DRIVE_DB_HOST', 'localhost')
    db_port = os.getenv('LOG_DRIVE_DB_PORT', '3306')
    db_name = os.getenv('LOG_DRIVE_DB_NAME', 'nimbletl')
    return f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# 创建数据库连接
DATABASE_URI = _get_drive_db_url()
print(DATABASE_URI)
engine = create_engine(DATABASE_URI, echo=True)

# 创建一个基础类
Base = declarative_base()

# 定义一个枚举类，表示日志驱动类型
class LogDriveType(PyEnum):
    TIME_WINDOW_1_PARAM_DAY = "time_window_1_param_day"
    TIME_WINDOW_2_PARAM = "time_window_2_param"
    UPSTREAM = "upstream"
    FILES = "files"

# 定义日志表
class LogDriveTable(Base):
    __tablename__ = 'log_drive_table'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='日志唯一标识')
    etl_name = Column(String(255), nullable=False, comment='ETL 任务名称')
    target_table_name = Column(String(255), nullable=False, comment='ETL 目标表名称')
    drive_type = Column(String(255), nullable=False, comment='日志驱动类型，'
                                                             '目前枚举值包括：'
                                                             'time_window_1_param_day,'
                                                             'time_window_2_param,'
                                                             'upstream, '
                                                             'files')
    drive_value = Column(String(255), nullable=False, comment='日志驱动值')
    process_start_time = Column(DateTime, nullable=False, comment='ETL 处理开始时间')
    process_end_time = Column(DateTime, nullable=False, comment='ETL 处理结束时间')
    etl_result = Column(Integer, nullable=False, comment='ETL 处理结果,目前枚举值包括：0-执行失败；1-执行成功；2-执行中')
    business_time = Column(String(255), comment='本批次数据涉及到的业务日期，逗号分割')


# 创建一个会话工厂
Session = sessionmaker(bind=engine)


# 定义日志保存函数
def save_log(etl_name, target_table_name, drive_type, drive_value, process_start_time, process_end_time, etl_result, business_time=None):
    session = Session()
    try:
        new_log = LogDriveTable(
            etl_name=etl_name,
            target_table_name=target_table_name,
            drive_type=drive_type,
            drive_value=drive_value,
            process_start_time=process_start_time,
            process_end_time=process_end_time,
            etl_result=etl_result,
            business_time=business_time
        )
        session.add(new_log)
        session.commit()
        print(f"Inserted log with id: {new_log.id}")
    except Exception as e:
        session.rollback()
        print(f"Error inserting log: {e}")
    finally:
        session.close()

# 示例使用
if __name__ == "__main__":
    save_log(
        etl_name="ETL Process 1",
        target_table_name="target_table_1",
        drive_type=LogDriveType.TIME_WINDOW_1_PARAM_DAY,
        drive_value="2024-06-01",
        process_start_time=datetime(2024, 6, 1, 0, 0, 0),
        process_end_time=datetime(2024, 6, 11, 1, 0, 0),
        etl_result=1,
        business_time="2024-06-01"
    )
