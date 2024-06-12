#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from argparse import ArgumentError
import json
import logging

import requests  # pylint: disable=requests-import

from ngcbpc.data.api.RequestStatus import RequestStatus

logger = logging.getLogger(__name__)


class NgcException(Exception):
    """A base class for NGC SDK exceptions."""


class ConfigFileException(NgcException):
    pass


class ValidationException(NgcException):
    pass


class MissingConfigFileException(ConfigFileException):
    def __init__(self, message="Config file is missing."):  # pylint: disable=useless-super-delegation
        super().__init__(message)


class PollingTimeoutException(NgcException):
    pass


class NgcAPIError(requests.exceptions.HTTPError, NgcException):
    """An HTTP error from the API."""

    def __init__(self, message, response=None, explanation=None, status_code=None):
        super().__init__(message)
        self.response = response
        self.explanation = explanation
        self.status_code = status_code or getattr(response, "status_code", "")

    def __str__(self):
        message = super().__str__()
        status_description = ""
        request_id = ""

        if self.response is None:
            message = "Error: {}".format(message)
            return message

        url = self.response.url

        if self.explanation and "requestStatus" in self.explanation:
            o = json.loads(self.explanation)
            try:
                request_status = RequestStatus(o["requestStatus"])
                status_description = request_status.statusDescription
                request_id = request_status.requestId
            except TypeError as e:
                logger.error(str(e))

        if self.is_client_error():
            message = "Client Error: {0} Response: {1} - Request Id: {2} Url: {3}".format(
                self.status_code, status_description, request_id, url
            )
        elif self.is_server_error():
            message = "Server Error: {0} Response: {1} - Request Id: {2} Url: {3}".format(
                self.status_code, status_description, request_id, url
            )
        else:
            if self.explanation:
                message = "Error {} Response: {} - Request Id: {}".format(
                    self.status_code, status_description, request_id
                )
        return message

    def is_client_error(self):
        if self.status_code is None:
            return False
        return 400 <= self.status_code < 500

    def is_server_error(self):
        if self.status_code is None:
            return False
        return 500 <= self.status_code < 600


class BadRequestException(NgcAPIError):
    pass


class AuthenticationException(NgcAPIError):
    pass


class AccessDeniedException(NgcAPIError):
    pass


class ResourceNotFoundException(NgcAPIError):
    pass


class ResourceFilesNotFoundException(NgcAPIError):
    pass


class ResourceAlreadyExistsException(NgcAPIError):
    pass


class TooManyRequestsException(NgcAPIError):
    pass


class InternalServerException(NgcAPIError):
    pass


class NotImplementedException(NgcAPIError):
    pass


class BadGatewayException(NgcAPIError):
    pass


class ServiceUnavailableException(NgcAPIError):
    pass


class GatewayTimeoutException(NgcAPIError):
    pass


class InsufficientStorageException(NgcAPIError):
    pass


class NgcAPIRetryableError(NgcAPIError):
    pass


class InvalidArgumentError(ArgumentError):
    def __init__(self, arg_name, message=None):
        if message is None:
            super().__init__(None, "Invalid {arg_name}.".format(arg_name=arg_name))
        else:
            super().__init__(None, message)


class UnsupportedPlatformException(NgcException):
    def __init__(self, platform=None, hostname=None, token=None, port=None):
        message = f"{platform if platform else 'Your operating system'} is not supported."
        self.hostname = hostname
        self.token = token
        self.port = port
        super().__init__(message)


class DownloadFileSizeMismatch(NgcException):
    pass
