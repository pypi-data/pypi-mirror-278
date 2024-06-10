import configparser
import sys

import psutil

from .exceptions.empty_config_value import EmptyConfigValue
from .exceptions.invalid_config_value import InvalidConfigValue
from .singleton_meta import SingletonMeta


class Config(metaclass=SingletonMeta):
    __config: configparser.ConfigParser | None = None

    __user_files_root_dir: str = ''

    __app_log_file_name: str = ''

    __task_1_first_input_file_name: str = ''

    __task_1_second_input_file_name: str = ''

    __task_1_output_file_name: str = ''

    __task_1_max_input_data_size_in_bytes: int = 0

    __task_3_input_file_name: str = ''

    __task_3_output_file_name: str = ''

    def __init__(self, config_file_path: str) -> None:
        self.__config = self.__get(config_file_path)

        self.__user_files_root_dir = self.__get_value(
            'DEFAULT', 'UserFilesRootDir')
        self.__app_log_file_name = self.__get_value(
            'DEFAULT', 'AppLogFileName')
        self.__task_1_first_input_file_name = self.__get_value(
            'first.task', 'FirstInputFileName')
        self.__task_1_second_input_file_name = self.__get_value(
            'first.task', 'SecondInputFileName')
        self.__task_1_output_file_name = self.__get_value(
            'first.task', 'OutputFileName')
        self.__task_1_max_input_data_size_in_bytes = self.__get_task_1_max_input_data_size_in_bytes(
            'first.task', 'MaxInputDataSizeInBytes')
        self.__task_3_input_file_name = self.__get_value(
            'third.task', 'InputFileName')
        self.__task_3_output_file_name = self.__get_value(
            'third.task', 'OutputFileName')

    def __get(self, config_file_path: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()

        with open(config_file_path, 'r') as file:
            config.read_file(file)

        return config

    def __get_task_1_max_input_data_size_in_bytes(self, section: str, key: str) -> int:
        value: int = 0

        try:
            value = int(self.__get_value(section, key))

            if value == 0:
                value = psutil.virtual_memory().available

        except ValueError as e:
            raise InvalidConfigValue(section, key, e)

        return value

    def __get_value(self, section: str, key: str) -> str:
        if self.__config is None:
            sys.exit(0)

        if self.__config[section][key] == '':
            raise EmptyConfigValue(section, key)

        value: str = self.__config[section][key]

        return value

    @property
    def user_files_root_dir(self) -> str:
        return self.__user_files_root_dir

    @property
    def app_log_file_name(self) -> str:
        return self.__app_log_file_name

    @property
    def task_1_first_input_file_name(self) -> str:
        return self.__task_1_first_input_file_name

    @property
    def task_1_second_input_file_name(self) -> str:
        return self.__task_1_second_input_file_name

    @property
    def task_1_output_file_name(self) -> str:
        return self.__task_1_output_file_name

    @property
    def task_1_max_input_data_size_in_bytes(self) -> int:
        return self.__task_1_max_input_data_size_in_bytes

    @property
    def task_3_input_file_name(self) -> str:
        return self.__task_3_input_file_name

    @property
    def task_3_output_file_name(self) -> str:
        return self.__task_3_output_file_name
