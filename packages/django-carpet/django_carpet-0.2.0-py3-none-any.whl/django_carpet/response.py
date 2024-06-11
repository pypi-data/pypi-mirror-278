# Python
import json
from typing import Union, Callable

# Django
from django.http.response import HttpResponse

# Third Party
from typing import Optional, Any

# Project
from .choices import ResponseChoices


class NotLoggedResponse(HttpResponse):

    def __init__(self):
        super().__init__(json.dumps({'result': 'not logged'}), status=401)


class APIResponse(HttpResponse):

    def __init__(self, response, request, status=200):
        if request.token is not None and request.token != '':
            super().__init__(json.dumps(response, default=str), content_type='application/json', status=status)
        else:
            super().__init__(json.dumps(response, default=str), status=status)


class NotAllowedResponse(HttpResponse):

    def __init__(self, reason: Optional[str] = None):
        super().__init__(json.dumps({'result': 'not allowed', 'reason': reason or ""}), status=405)


class VieoloResponse:

    def __init__(
        self, 
        result: str, 
        object_key: str = "",
        obj: str | None = None, 
        type_of_object: str | None = None, 
        operation: str | None = None, 
        reason: str | None = None, 
        message: str | None = None, 
        status_code: int | None = None,
    ):
        self.result = result
        self.obj = obj
        self.type_of_object = type_of_object
        self.operation = operation
        self.reason = reason
        self.message = message
        self.response_object = {}
        self.status_code = status_code
        self.object_key = object_key

    def __str__(self) -> str:
        return str(self.response_object)

    def is_successful(self) -> bool:
        return self.result == ResponseChoices.success
    
    def is_does_not_exist(self) -> bool:
        return self.result == ResponseChoices.does_not_exist

    def is_already_exists(self) -> bool:
        return self.result == ResponseChoices.already_exists

    def is_invalid(self) -> bool:
        return self.result == ResponseChoices.not_valid

    def is_not_allowed(self) -> bool:
        return self.result == ResponseChoices.not_allowed
    
    def get_id(self) -> int:
        return self.response_object[self.object_key]["id"]

    def filter(self, func: Callable[[dict], bool]) -> list[dict]:
        return list(filter(func, self.data))

    @property 
    def data(self):
        return self.response_object[self.object_key]

    @property 
    def data_len(self) -> int:
        return len(self.response_object[self.object_key])

    @staticmethod 
    def parse(raw: Union[str, HttpResponse], object_key = "") -> 'VieoloResponse':
        if isinstance(raw, HttpResponse):
            parsed = json.loads(raw.content)
            status_code = raw.status_code
        else:
            parsed = json.loads(raw)
            status_code = None

        response = VieoloResponse(
            result=parsed['result'],
            status_code=status_code,
            object_key=object_key,
        )

        for k, v in parsed.items():
            if k == 'operation':
                response.operation = v
            elif k == 'object':
                response.obj = v
            elif k == 'type':
                response.type_of_object = v
            elif k == 'reason':
                response.reason = v
            elif k == 'message':
                response.message = v

            response.response_object[k] = v

        return response


def generate_response(
    result: str, 
    *,
    obj: Optional[str]=None, 
    type_of_object: Optional[str]=None, 
    operation: Optional[str]=None, 
    reason: Optional[str]=None, 
    message: Optional[str]=None,
    data: Optional[dict]=None,
) -> dict[str, Any]:
    """Generates a dict following the Vieolo's response convention

    Args:
        result: The result of the response. Use `ResponseChoices`
        obj: The `object` key of response. Defaults to None.
        type_of_object: the `type` key of response. Defaults to None.
        operation: the `operation` key of response. Defaults to None.
        reason: the `reason` key of response. Defaults to None.
        message: the `message` key of response. Defaults to None.
        data: The data to be merged with the response containing the response data. Defaults to None.
    """
    response = {
        "result": result
    }
    if obj is not None:
        response["object"] = obj
    if type_of_object is not None:
        response["type"] = type_of_object
    if operation is not None:
        response["operation"] = operation
    if reason is not None:
        response["reason"] = reason
    if message is not None:
        response["message"] = message
    
    if data is not None:
        response = response | data

    return response
