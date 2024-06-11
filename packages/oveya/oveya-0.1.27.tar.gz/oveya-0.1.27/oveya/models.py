from __future__ import annotations

from .helpers import remove_keys_recursively
from .enums import RequestMethod

from pydantic import BaseModel, Extra, validate_arguments, create_model, ValidationError
from typing import Callable, Any, Dict, get_type_hints, Optional, Tuple
import inspect
import re


class BaseAction(BaseModel):
    class Config:
        extra = Extra.allow


class Action:
    def __init__(self, func: Callable, path: str, method: RequestMethod, preserve_output_types: bool = False):
        self.func = func
        self.validate_func = validate_arguments(func)
        self.method = method
        self.preserve_output_types = preserve_output_types
        self.path = self._normalize_path(path, func.__name__)
        self.openapi_schema = self._generate_openapi_schema()

    @staticmethod
    def _normalize_path(path: str, func_name: str) -> str:
        return path if path != '/' else f'/{func_name.strip("/").replace("/", "_").replace(" ", "_")}'

    def _generate_openapi_schema(self) -> Dict[str, Any]:
        model_fields, required_fields = self._get_model_fields_with_defaults()
        if model_fields:
            DynamicModel = create_model('DynamicModel', **model_fields)
            input_schema = self._clean_schema(DynamicModel.schema(), required_fields)
        else:
            input_schema = {}

        response_schema = self._create_output_schema()
        docstring_summary, param_descriptions, return_description = self._parse_docstring()

        operation = {
            "operationId": self.func.__name__,
            "summary": docstring_summary,
            "responses": {
                "200": {
                    "description": return_description or "Successful Response",
                    "content": {
                        "application/json": {"schema": response_schema}
                    }
                }
            }
        }

        if model_fields:
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {"schema": input_schema}
                }
            }

            for param, description in param_descriptions.items():
                if param in input_schema.get("properties", {}):
                    input_schema["properties"][param]["description"] = description

        return {
            self.path: {
                self.method.lower(): operation
            }
        }

    def _get_model_fields_with_defaults(self) -> Tuple[Dict[str, Any], list]:
        type_hints = get_type_hints(self.func)
        signature = inspect.signature(self.func)
        model_fields = {}
        required_fields = []

        for param in signature.parameters.values():
            param_type = type_hints.get(param.name, str)  # Default to str if type hint is not provided
            if param_type is Any and param.default is not param.empty:
                param_type = type(param.default)

            if param.default is param.empty:
                model_fields[param.name] = (param_type, ...)
                required_fields.append(param.name)
            else:
                model_fields[param.name] = (Optional[param_type], param.default)

        return model_fields, required_fields

    def _clean_schema(self, schema: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
        relevant_properties = {
            k: v for k, v in schema["properties"].items() if k not in {"v__duplicate_kwargs", "args", "kwargs"}
        }
        for key, value in relevant_properties.items():
            if key not in required_fields:
                value["nullable"] = True
                # Adjust the type definition to avoid "anyOf"
                if "anyOf" in value:
                    value["type"] = value["anyOf"][0].get("type", "string")
                    del value["anyOf"]

        schema["properties"] = relevant_properties
        schema["required"] = required_fields
        schema = remove_keys_recursively(schema, "additionalProperties")
        schema = remove_keys_recursively(schema, "title")
        return schema

    def _create_output_schema(self) -> Dict[str, Any]:
        if not self.preserve_output_types:
            return {"type": "string"}

        return_type = get_type_hints(self.func).get('return', Any)
        if return_type == Any:
            return {"type": "object", "additionalProperties": True}
        if return_type and issubclass(return_type, BaseModel):
            return return_type.schema()
        temp_model = create_model('TempModel', result=(return_type, ...))
        return temp_model.schema()["properties"]["result"]

    def _parse_docstring(self) -> Tuple[str, Dict[str, str], str]:
        docstring = self.func.__doc__ or ""
        summary = []
        param_descriptions = {}
        return_description = ""

        param_pattern = re.compile(r":param\s+(\w+):\s*(.+)")
        return_pattern = re.compile(r":return:\s*(.+)")
        params_pattern = re.compile(r":params\s+(\w+):\s*(.+)")

        lines = docstring.split('\n')
        for line in lines:
            line = line.strip()
            param_match = param_pattern.match(line)
            params_match = params_pattern.match(line)
            return_match = return_pattern.match(line)
            if param_match:
                param_descriptions[param_match.group(1)] = param_match.group(2)
            elif params_match:
                param_descriptions[params_match.group(1)] = params_match.group(2)
            elif return_match:
                return_description = return_match.group(1)
            else:
                summary.append(line)

        summary_text = " ".join(summary).strip()
        return summary_text, param_descriptions, return_description

    def run(self, arguments=None):
        if arguments is None:
            arguments = {}
        try:
            return self.validate_func(**arguments)
        except (ValidationError, TypeError) as e:
            raise ValueError(f"Invalid request body: {str(e)}")
