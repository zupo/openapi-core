"""OpenAPI core contrib flask requests module"""
import re

from openapi_core.validation.request.datatypes import (
    RequestParameters, OpenAPIRequest,
)

# http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules
PATH_PARAMETER_PATTERN = r'<(?:(?:string|int|float|path|uuid):)?(\w+)>'


class FlaskOpenAPIRequestFactory(object):

    path_regex = re.compile(PATH_PARAMETER_PATTERN)

    @classmethod
    def create(cls, request):
        method = request.method.lower()

        if request.url_rule is None:
            path_pattern = request.path
        else:
            path_pattern = cls.path_regex.sub(r'{\1}', request.url_rule.rule)

        parameters = RequestParameters(
            path=request.view_args,
            query=request.args,
            header=request.headers,
            cookie=request.cookies,
        )
        return OpenAPIRequest(
            host_url=request.host_url,
            path=request.path,
            path_pattern=path_pattern,
            method=method,
            parameters=parameters,
            body=request.data,
            mimetype=request.mimetype,
        )
