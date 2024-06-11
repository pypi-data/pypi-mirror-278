from .datetime_pomes import (
    DATE_FORMAT_STD, DATE_FORMAT_COMPACT, DATE_FORMAT_INV,
    DATETIME_FORMAT_STD, DATETIME_FORMAT_COMPACT, DATETIME_FORMAT_INV,
    TIMEZONE_LOCAL, TIMEZONE_UTC,
    date_reformat, date_parse, datetime_parse,
)
from .dict_pomes import (
    dict_has_key_chain, dict_get_value, dict_set_value, dict_reduce,
    dict_listify, dict_transform, dict_merge, dict_coalesce, dict_clone,
    dict_get_key, dict_get_keys, dict_from_object, dict_from_list,
    dict_replace_value, dict_pop_value,
)
from .email_pomes import (
    EMAIL_ACCOUNT, EMAIL_PWD, EMAIL_PORT, EMAIL_SERVER,
    email_send,
)
from .encoding_pomes import (
    encode_ascii_hex, decode_ascii_hex,
)
from .env_pomes import (
    APP_PREFIX,
    env_get_str, env_get_int, env_get_bool, env_get_float, env_get_path,
)
from .exception_pomes import (
    exc_format,
)
from .file_pomes import (
    TEMP_FOLDER,
    file_from_request, file_get_data
)
from .json_pomes import (
    json_normalize_dict, json_normalize_iterable,
)
from .list_pomes import (
    list_compare, list_flatten, list_unflatten,
    list_find_coupled, list_elem_starting_with,
    list_transform, list_prune_in, list_prune_not_in
)
from .str_pomes import (
    str_as_list, str_sanitize, str_split_on_mark,
    str_find_whitespace, str_get_between, str_get_positional, str_rreplace,
)
from .validation_msgs import (
    validate_set_msgs, validate_update_msgs,
)
from .validation_pomes import (
    VALIDATION_MSG_LANGUAGE, VALIDATION_MSG_PREFIX,
    validate_value, validate_bool, validate_int, validate_float, validate_str,
    validate_date, validate_datetime, validate_ints, validate_strs,
    validate_format_error, validate_format_errors, validate_unformat_errors,
)
from .xml_pomes import (
    XML_FILE_HEADER,
    xml_to_dict, xml_normalize_keys,
)

__all__ = [
    # __init__
    "get_versions",
    # datetime_pomes
    "DATE_FORMAT_STD", "DATE_FORMAT_COMPACT", "DATE_FORMAT_INV",
    "DATETIME_FORMAT_STD", "DATETIME_FORMAT_COMPACT", "DATETIME_FORMAT_INV",
    "TIMEZONE_LOCAL", "TIMEZONE_UTC",
    "date_reformat", "date_parse", "datetime_parse",
    # dict_pomes
    "dict_has_key_chain", "dict_get_value", "dict_set_value", "dict_reduce",
    "dict_listify", "dict_transform", "dict_merge", "dict_coalesce", "dict_clone",
    "dict_get_key", "dict_get_keys", "dict_from_object", "dict_from_list",
    "dict_replace_value", "dict_pop_value",
    # email_pomes
    "EMAIL_ACCOUNT", "EMAIL_PWD", "EMAIL_PORT", "EMAIL_SERVER",
    "email_send",
    # encoding_pomes
    "encode_ascii_hex", "decode_ascii_hex",
    # env_pomes
    "APP_PREFIX",
    "env_get_str", "env_get_int", "env_get_bool", "env_get_float", "env_get_path",
    # exception_pomes
    "exc_format",
    # file_pomes
    "TEMP_FOLDER",
    "file_from_request", "file_get_data",
    # json_pomes
    "json_normalize_dict", "json_normalize_iterable",
    # list_pomes
    "list_compare", "list_flatten", "list_unflatten",
    "list_find_coupled", "list_elem_starting_with",
    "list_transform", "list_prune_in", "list_prune_not_in",
    # str_pomes
    "str_as_list", "str_sanitize", "str_split_on_mark",
    "str_find_whitespace", "str_get_between", "str_get_positional", "str_rreplace",
    # validation_msgs
    "validate_set_msgs", "validate_update_msgs",
    # validation_pomes
    "VALIDATION_MSG_LANGUAGE", "VALIDATION_MSG_PREFIX",
    "validate_value", "validate_bool", "validate_int", "validate_float", "validate_str",
    "validate_date", "validate_datetime", "validate_ints", "validate_strs",
    "validate_format_error", "validate_format_errors", "validate_unformat_errors",
    # xml_pomes
    "XML_FILE_HEADER",
    "xml_to_dict", "xml_normalize_keys",
]

from importlib.metadata import version
__version__ = version("pypomes_core")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())


from contextlib import suppress
from importlib import import_module
def get_versions() -> dict:
    """
    Retrieve and return the versions of the *Pypomes* packages in use.

    :return: the versions of the Pypomes packages in use
    """
    result: dict = {
        "PyPomes-Core": __version__
    }

    with suppress(Exception):
        result["PyPomes-Cloud"] =  import_module(name="pypomes_cloud").__version__

    with suppress(Exception):
        result["PyPomes-Crypto"] =  import_module(name="pypomes_crypto").__version__

    with suppress(Exception):
        result["PyPomes-DB"] =  import_module(name="pypomes_db").__version__

    with suppress(Exception):
        result["PyPomes-HTTP"] =  import_module(name="pypomes_http").__version__

    with suppress(Exception):
        result["PyPomes-LDAP"] =  import_module(name="pypomes_ldap").__version__

    with suppress(Exception):
        result["PyPomes-Logging"] =  import_module(name="pypomes_logging").__version__

    with suppress(Exception):
        result["PyPomes-Messaging"] =  import_module(name="pypomes_messaging").__version__

    with suppress(Exception):
        result["PyPomes-S3"] =  import_module(name="pypomes_s3").__version__

    with suppress(Exception):
        result["PyPomes-Scheduling"] =  import_module(name="pypomes_scheduling").__version__

    with suppress(Exception):
        result["PyPomes-Security"] =  import_module(name="pypomes_security").__version__

    with suppress(Exception):
        result["PyPomes-SOAP"] =  import_module(name="pypomes_soap").__version__

    return result
