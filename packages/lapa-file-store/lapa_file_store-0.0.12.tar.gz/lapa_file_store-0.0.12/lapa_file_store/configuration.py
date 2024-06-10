import os
import sys

from lapa_commons.main import read_configuration_from_file_path
from square_logger.main import SquareLogger

try:

    config_file_path = (
        os.path.dirname(os.path.abspath(__file__))
        + os.sep
        + "data"
        + os.sep
        + "config.ini"
    )
    ldict_configuration = read_configuration_from_file_path(config_file_path)

    # get all vars and typecast
    # ===========================================
    # general
    config_str_module_name = ldict_configuration["GENERAL"]["MODULE_NAME"]
    # ===========================================

    # ===========================================
    # environment
    config_str_host_ip = ldict_configuration["ENVIRONMENT"]["HOST_IP"]
    config_int_host_port = int(ldict_configuration["ENVIRONMENT"]["HOST_PORT"])

    config_str_log_file_name = ldict_configuration["ENVIRONMENT"]["LOG_FILE_NAME"]
    config_str_local_storage_folder_path = ldict_configuration["ENVIRONMENT"][
        "LOCAL_STORAGE_PATH"
    ]
    # ===========================================

    # ===========================================
    # square_logger
    config_int_log_level = int(ldict_configuration["SQUARE_LOGGER"]["LOG_LEVEL"])
    config_str_log_path = ldict_configuration["SQUARE_LOGGER"]["LOG_PATH"]
    config_int_log_backup_count = int(
        ldict_configuration["SQUARE_LOGGER"]["LOG_BACKUP_COUNT"]
    )
    # ===========================================
    # ===========================================
    # lapa_database_helper

    config_str_lapa_database_protocol = ldict_configuration["LAPA_DATABASE_HELPER"][
        "LAPA_DATABASE_PROTOCOL"
    ]
    config_str_lapa_database_ip = ldict_configuration["LAPA_DATABASE_HELPER"][
        "LAPA_DATABASE_IP"
    ]
    config_int_lapa_database_port = int(
        ldict_configuration["LAPA_DATABASE_HELPER"]["LAPA_DATABASE_PORT"]
    )
    # ===========================================
    # initialize logger

    global_object_square_logger = SquareLogger(
        pstr_log_file_name=config_str_log_file_name,
        pint_log_level=config_int_log_level,
        pstr_log_path=config_str_log_path,
        pint_log_backup_count=config_int_log_backup_count,
    )
except Exception as e:
    print(
        "\033[91mMissing or incorrect config.ini file.\n"
        "Error details: " + str(e) + "\033[0m"
    )
    sys.exit()

# extra logic for this module

try:
    global_absolute_path_local_storage = os.path.abspath(
        config_str_local_storage_folder_path
    )
    if not os.path.exists(global_absolute_path_local_storage):
        os.makedirs(global_absolute_path_local_storage)
except Exception as e:
    print(
        "\033[91mIncorrect value for LOCAL_STORAGE_PATH in config.ini file.\n"
        "Error details: " + str(e) + "\033[0m"
    )
    sys.exit()
