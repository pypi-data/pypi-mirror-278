from __future__ import annotations
import json
from pydantic import ValidationError
from typing import Callable

from .ctx import RequestContextMiddleware, get_request
from .enums import RequestMethod
from .logging import create_logger
from .models import Action
from .helpers import remove_keys_recursively
from .errors import VaulError, InvalidRequestError, InternalServerError

import logging


class Vaul:
    instance = None

    @staticmethod
    def get_instance():
        if Vaul.instance is None:
            Vaul.instance = Vaul()
        return Vaul.instance

    def __init__(
            self,
            name='Vaul',
            title='Vaul Cloud API',
            description='Vaul Cloud API',
            log_level='INFO',
            debug=False,
            preserve_output_types=False
    ):
        self.title = title
        self.description = description
        self.middleware = RequestContextMiddleware(self._handler)
        self.name = name
        self.routes = {}
        self.log_level = self.validate_log_level(log_level)
        self.debug = debug
        self.logger = create_logger(self)
        self.preserve_output_types = preserve_output_types

    @staticmethod
    def validate_log_level(log_level: str) -> int:
        level = logging.getLevelName(log_level.upper())
        if not isinstance(level, int):
            raise ValueError(f"Invalid log level: {log_level} - Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        return level

    def action(self, path: str = '/', method: RequestMethod | str = RequestMethod.POST):
        if isinstance(method, str):
            method = method.upper()
            if method not in RequestMethod.to_list():
                raise ValueError(f"Invalid method: {method}")
            method = getattr(RequestMethod, method)

        def decorator(func: Callable):
            action = Action(func, path, method, self.preserve_output_types)
            self._register_action(action)
            return action
        return decorator

    def _register_action(self, action):
        self.routes.setdefault(action.path, {})[action.method] = action

    def _handler(self, event):
        request = get_request()
        if request is None:
            return self._response(500, {'error': 'Internal server error', 'details': 'Request context is missing'}, RequestMethod.GET)

        path, method = request.path, request.method
        route_handler = self._get_route_handler(path, method, event.get('requestContext', {}).get('domainName'))

        if not route_handler:
            return self._response(404, {'error': f"Path or method not found: {path}, {method}"}, method)

        return route_handler(request)

    def _get_route_handler(self, path, method, domain_name):
        if path == '/' and method == RequestMethod.GET:
            return lambda _: self._response(200, self.handle_base_path(), method)
        if path == '/openapi.json' and method == RequestMethod.GET:
            return lambda _: self._response(200, self.handle_openapi_request(domain_name), method)
        if method == RequestMethod.OPTIONS:
            return lambda _: self._response(200, self.handle_options_request(), method)
        if path in self.routes and method in self.routes[path]:
            return lambda request: self._run_action(request, path, method)
        return None

    def _run_action(self, request, path, method):
        try:
            body = self.routes[path][method].run(request.json())
            return self._response(200, body, method)
        except ValidationError as e:
            return self._response(400, InvalidRequestError(str(e)).to_dict(), method)
        except VaulError as e:
            return self._response(e.status_code, e.to_dict(), method)
        except Exception as e:
            self.logger.error(f"Exception occurred: {e}", exc_info=True)  # Log the exception
            return self._response(500, InternalServerError(str(e)).to_dict(), method)

    def _response(self, status_code, body, method, content_type='application/json', is_base64_encoded=False):
        headers = {
            'Content-Type': content_type,
        }

        if method == RequestMethod.OPTIONS:
            headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            })

        return {
            'statusCode': status_code,
            'body': json.dumps(body) if isinstance(body, (dict, list)) else body,
            'headers': headers,
            'isBase64Encoded': is_base64_encoded
        }

    def handler(self, event):
        return self.middleware(event)

    def _generate_openapi_schema(self, url: str):
        openapi_paths = {}
        for path, methods in self.routes.items():
            for method, action in methods.items():
                openapi_paths.setdefault(path, {})[method.lower()] = action.openapi_schema[path][method.lower()]

        return {
            "openapi": "3.0.0",
            "info": {"title": "Vaul Cloud API", "version": "1.0.0", "description": "Vaul Cloud API"},
            "servers": [{"url": url}],
            "paths": openapi_paths,
        }

    @staticmethod
    def handle_options_request():
        return {
            'statusCode': 200,
            'body': '',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'isBase64Encoded': False
        }

    def handle_openapi_request(self, domain_name):
        return self._generate_openapi_schema(url=f'https://{domain_name}')

    @staticmethod
    def handle_base_path():
        return {'message': 'Vaul Cloud Action API Base Path'}
