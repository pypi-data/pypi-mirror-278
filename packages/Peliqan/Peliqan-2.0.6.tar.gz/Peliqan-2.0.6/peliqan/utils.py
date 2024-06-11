import time
from json import JSONEncoder

from peliqan.exceptions import PeliqanJsonSerializerException, PeliqanClientException


class Empty:
    pass


empty = Empty()


def _serialize_dict(obj):
    for k in obj:
        obj[k] = _serialize_data(obj[k])

    return obj


def _serialize_array(obj):
    obj_len = len(obj)
    for i in range(obj_len):
        obj[i] = _serialize_data(obj[i])

    return obj


def _serialize_primitives(obj):
    formatted_obj = obj
    if isinstance(obj, float) and str(obj) == 'nan':
        formatted_obj = None

    return formatted_obj


def _serialize_others(obj):
    try:
        formatted_obj = JSONEncoder().encode(obj)
    except Exception as e:
        try:
            formatted_obj = str(obj)
        except Exception:
            raise PeliqanJsonSerializerException(
                f"Could not serialize {obj.__class__.__name__} with value {obj}. "
                f"Original error is {e}"
            )

    return formatted_obj


def _serialize_data(obj):
    if isinstance(obj, dict):
        formatted_obj = _serialize_dict(obj)

    elif type(obj) in (list, tuple):
        formatted_obj = _serialize_array(obj)

    elif isinstance(obj, (int, float, str)):
        formatted_obj = _serialize_primitives(obj)

    elif isinstance(obj, type(None)):
        formatted_obj = None

    else:
        formatted_obj = _serialize_others(obj)

    return formatted_obj


ONE_MB = 1024 * 1024
MAX_BATCH_BYTE_SIZE = ONE_MB * 10  # MB


def _check_record_byte_size(records):
    bytes_used = len(repr(records).encode('utf-8'))
    if bytes_used > MAX_BATCH_BYTE_SIZE:
        raise PeliqanClientException(
            f"Total size of all records, {int(bytes_used / ONE_MB)}MB, "
            f"exceeds max allowed size of {int(MAX_BATCH_BYTE_SIZE / ONE_MB)}MB."
        )


def _retry_get_resource_status(refresh_func):
    interval = 5  # seconds
    count = 0
    running = True
    while running:
        if count > 10:
            interval = 20

        elif count > 5:
            interval = 10

        response = refresh_func()
        running = response.get('running', True)
        if not running:
            return {
                'task_id': response['task_id'],
                'run_id': response.get('run_id'),
                'detail': 'The sync task has completed.',
                'syncing': False
            }

        time.sleep(interval)
        count += 1
