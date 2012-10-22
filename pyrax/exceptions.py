#!/usr/bin/env python
# -*- coding: utf-8 -*-


class AuthenticationFailed(Exception):
     pass

class AuthorizationFailure(Exception):
     pass

class AuthSystemNotFound(Exception):
     pass

class CDNFailed(Exception):
     pass

class EndpointNotFound(Exception):
     pass

class FlavorNotFound(Exception):
     pass

class FileNotFound(Exception):
     pass

class FolderNotFound(Exception):
     pass

class InvalidCDNMetada(Exception):
     pass

class InvalidConfigurationFile(Exception):
     pass

class InvalidCredentialFile(Exception):
     pass

class InvalidUploadID(Exception):
     pass

class InvalidVolumeResize(Exception):
     pass

class MissingName(Exception):
     pass

class NoSuchContainer(Exception):
     pass

class NoSuchObject(Exception):
     pass

class NotAuthenticated(Exception):
     pass

class NotCDNEnabled(Exception):
     pass

class NoTokenLookupException(Exception):
     pass

class Unauthorized(Exception):
     pass

class UploadFailed(Exception):
     pass


class AmbiguousEndpoints(Exception):
    """Found more than one matching endpoint in Service Catalog."""
    def __init__(self, endpoints=None):
        self.endpoints = endpoints

    def __str__(self):
        return "AmbiguousEndpoints: %s" % repr(self.endpoints)


class ClientException(Exception):
    """
    The base exception class for all exceptions this library raises.
    """
    def __init__(self, code, message=None, details=None, request_id=None):
        self.code = code
        self.message = message or self.__class__.message
        self.details = details
        self.request_id = request_id

    def __str__(self):
        formatted_string = "%s (HTTP %s)" % (self.message, self.code)
        if self.request_id:
            formatted_string += " (Request-ID: %s)" % self.request_id

        return formatted_string

class BadRequest(ClientException):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """
    http_status = 400
    message = "Bad request"


class Unauthorized(ClientException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = 401
    message = "Unauthorized"


class Forbidden(ClientException):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(ClientException):
    """
    HTTP 404 - Not found
    """
    http_status = 404
    message = "Not found"


class OverLimit(ClientException):
    """
    HTTP 413 - Over limit: you're over the API limits for this time period.
    """
    http_status = 413
    message = "Over limit"


# NotImplemented is a python keyword.
class HTTPNotImplemented(ClientException):
    """
    HTTP 501 - Not Implemented: the server does not support this operation.
    """
    http_status = 501
    message = "Not Implemented"



# In Python 2.4 Exception is old-style and thus doesn't have a __subclasses__()
# so we can do this:
#     _code_map = dict((c.http_status, c)
#                      for c in ClientException.__subclasses__())
#
# Instead, we have to hardcode it:
_code_map = dict((c.http_status, c) for c in [BadRequest, Unauthorized,
                   Forbidden, NotFound, OverLimit, HTTPNotImplemented])


def from_response(response, body):
    """ 
    Return an instance of a ClientException or subclass
    based on an httplib2 response.

    Usage::

        resp, body = http.request(...)
        if resp.status != 200:
            raise exception_from_response(resp, body)
    """
    cls = _code_map.get(response.status, ClientException)
    request_id = response.get('x-compute-request-id')
    if body:
        message = "n/a"
        details = "n/a"
        if hasattr(body, 'keys'):
            error = body[body.keys()[0]]
            message = error.get('message', None)
            details = error.get('details', None)
        return cls(code=response.status, message=message, details=details,
                   request_id=request_id)
    else:
        return cls(code=response.status, request_id=request_id)
