from typing import Required, Union, TypedDict, Literal


_CheckStatus = Union[Literal['success'], Literal['failure'], Literal['missed_window']]
""" The status of the check """
_CHECKSTATUS_SUCCESS: Literal['success'] = "success"
"""The values for the 'The status of the check' enum"""
_CHECKSTATUS_FAILURE: Literal['failure'] = "failure"
"""The values for the 'The status of the check' enum"""
_CHECKSTATUS_MISSED_WINDOW: Literal['missed_window'] = "missed_window"
"""The values for the 'The status of the check' enum"""



_CheckStatusReason = Union["_CheckStatusReasonObject", None]
""" Reason for the status, primairly used for failure """



class _CheckStatusReasonObject(TypedDict, total=False):
    """ Reason for the status, primairly used for failure """

    type: Required["_CheckStatusReasonType"]
    """
    The type of the status reason

    Required property
    """

    description: Required[str]
    """
    A human readable description of the status reason

    Required property
    """



_CheckStatusReasonType = Union[Literal['timeout'], Literal['dns_error'], Literal['failure']]
""" The type of the status reason """
_CHECKSTATUSREASONTYPE_TIMEOUT: Literal['timeout'] = "timeout"
"""The values for the 'The type of the status reason' enum"""
_CHECKSTATUSREASONTYPE_DNS_ERROR: Literal['dns_error'] = "dns_error"
"""The values for the 'The type of the status reason' enum"""
_CHECKSTATUSREASONTYPE_FAILURE: Literal['failure'] = "failure"
"""The values for the 'The type of the status reason' enum"""



_RequestInfo = Union["_RequestInfoObject", None]
""" Additional information about the request made """



class _RequestInfoObject(TypedDict, total=False):
    """ Additional information about the request made """

    request_type: Required["_RequestType"]
    """
    The type of HTTP method used for the check

    Required property
    """

    http_status_code: Required[Union[Union[int, float], None]]
    """
    Status code of the successful check-in

    Required property
    """



_RequestType = Union[Literal['HEAD'], Literal['GET']]
""" The type of HTTP method used for the check """
_REQUESTTYPE_HEAD: Literal['HEAD'] = "HEAD"
"""The values for the 'The type of HTTP method used for the check' enum"""
_REQUESTTYPE_GET: Literal['GET'] = "GET"
"""The values for the 'The type of HTTP method used for the check' enum"""



class _Root(TypedDict, total=False):
    """ A message containing the result of the uptime check. """

    guid: Required[str]
    """
    Unique identifier of the uptime check

    Required property
    """

    monitor_id: Required[int]
    """
    The identifier of the uptime monitor

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    monitor_environment_id: Required[int]
    """
    The identifier of the uptime monitors environment

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    status: Required["_CheckStatus"]
    """
    The status of the check

    Required property
    """

    status_reason: Required["_CheckStatusReason"]
    """
    Reason for the status, primairly used for failure

    Required property
    """

    trace_id: Required[str]
    """
    Trace ID associated with the check-in made

    Required property
    """

    scheduled_check_time: Required[Union[int, float]]
    """
    Timestamp in milliseconds of when the check was schedule to run

    Required property
    """

    actual_check_time: Required[Union[int, float]]
    """
    Timestamp in milliseconds of when the check was actually ran

    Required property
    """

    duration_ms: Required[Union[Union[int, float], None]]
    """
    Duration of the check in ms. Will be null when the status is missed_window

    Required property
    """

    request_info: Required["_RequestInfo"]
    """
    Additional information about the request made

    Required property
    """

