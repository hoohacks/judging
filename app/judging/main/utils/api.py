import datetime
from typing import Any, Dict

from django.http import JsonResponse, QueryDict
from django.utils.dateparse import parse_date, parse_time


class ApiException(Exception):
    def __init__(self, reason, status=400, payload={}):
        Exception.__init__(self)
        self.reason = reason
        self.status = status
        self.payload = payload

    def to_json_response(self):
        return JsonResponse(data={'payload': self.payload},
                            status=self.status,
                            reason=self.reason)

    def __str__(self):
        return self.reason


def extract_fields(fields: Dict[str, Dict[str, Any]], params: QueryDict) -> Dict[str, Any]:
    kwargs = {}
    for _attr, _info in fields.items():
        if params.get(_attr):
            if _info['type'] == datetime.date:
                kwargs[_attr] = parse_date(params.get(_attr))
            elif _info['type'] == datetime.time:
                kwargs[_attr] = parse_time(params.get(_attr))
            elif _info['type'] == bool:
                kwargs[_attr] = bool(params.get(_attr, False))
            else:
                kwargs[_attr] = _info['type'](params.get(_attr))
        elif not params.get(_attr) and _info['required']:
            raise ApiException(reason="{} field is required".format(_attr))
    return kwargs


def check_method(request, correct_method):
    if request.method != correct_method:
        raise ApiException(reason="Received {}, must be {}".format(request.method, correct_method),
                           status=405)
