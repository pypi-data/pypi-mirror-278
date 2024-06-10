from datetime import datetime, timezone

from fastapi import status
from fastapi.exceptions import HTTPException
from lapa_database_helper.main import LAPADatabaseHelper
from lapa_database_structure.lapa.file_storage.tables import (
    local_string_database_name,
    local_string_schema_name,
    File,
)

from lapa_file_store.configuration import (
    global_object_square_logger,
    config_str_lapa_database_protocol,
    config_str_lapa_database_ip,
    config_int_lapa_database_port,
)

local_object_lapa_database_helper = LAPADatabaseHelper(
    param_str_lapa_database_ip=config_str_lapa_database_ip,
    param_str_lapa_database_protocol=config_str_lapa_database_protocol,
    param_int_lapa_database_port=config_int_lapa_database_port,
)


def create_entry_in_file_store(
    file_name_with_extention: str,
    content_type: str,
    system_file_name_with_extension: str,
    file_storage_token: str,
    file_purpose: str,
    system_relative_path: str,
):
    try:

        data = [
            {
                File.file_name_with_extension.name: file_name_with_extention,
                File.file_content_type.name: content_type,
                File.file_system_file_name_with_extension.name: system_file_name_with_extension,
                File.file_system_relative_path.name: system_relative_path,
                File.file_storage_token.name: file_storage_token,
                File.file_purpose.name: file_purpose,
            }
        ]

        response = local_object_lapa_database_helper.insert_rows(
            data,
            local_string_database_name,
            local_string_schema_name,
            File.__tablename__,
        )

        return response
    except Exception as e:
        raise e


def get_file_row(file_storage_token):
    try:

        filters = {File.file_storage_token.name: file_storage_token}

        response = local_object_lapa_database_helper.get_rows(
            filters,
            local_string_database_name,
            local_string_schema_name,
            File.__tablename__,
            ignore_filters_and_get_all=False,
        )
        if isinstance(response, list) and len(response) == 1 and response[0]:
            return response[0]
        elif len(response) > 1:
            global_object_square_logger.logger.warning(
                f"Multiple files with same file_storage_token: {file_storage_token}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"incorrect file_storage_token:{file_storage_token}",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"incorrect file_storage_token:{file_storage_token}",
            )

    except Exception as e:
        raise e


def edit_file_delete_status(file_storage_token):
    try:
        filters = {File.file_storage_token.name: file_storage_token}

        # Get the current timestamp
        timestamp = datetime.now(timezone.utc)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f+00")

        data = {File.file_is_deleted.name: True, File.file_date_deleted.name: formatted_timestamp}

        response = local_object_lapa_database_helper.edit_rows(
            filters=filters,
            data=data,
            database_name=local_string_database_name,
            schema_name=local_string_schema_name,
            table_name=File.__tablename__,
            ignore_filters_and_edit_all=False
        )

        if isinstance(response, list) and len(response) == 1 and response[0]:
            file_data = response[0]
            if File.file_storage_token.name in file_data and file_data[
                File.file_storage_token.name] == file_storage_token:
                return file_data
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"incorrect file_storage_token:{file_storage_token}",
                )
        elif len(response) > 1:
            global_object_square_logger.logger.warning(
                f"Multiple files with same file_storage_token: {file_storage_token}"
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"incorrect file_storage_token:{file_storage_token}",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"incorrect file_storage_token:{file_storage_token}",
            )
    except Exception as e:
        raise e
