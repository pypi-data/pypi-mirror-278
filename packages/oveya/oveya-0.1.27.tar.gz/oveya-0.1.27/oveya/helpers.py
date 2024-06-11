import argparse
import json
import shlex
from collections import OrderedDict, namedtuple
from typing import Any, Dict, List, Union
from urllib.parse import urlparse, parse_qs


def remove_keys_recursively(d: Dict[Any, Any], keys_to_remove: Union[str, List[str]]) -> Dict[Any, Any]:
    """ Recursively removes specified keys from a dictionary.

    Parameters:
    - d (Dict[Any, Any]): The dictionary from which keys should be removed.
    - keys_to_remove (str | List[str]): The key or list of keys to remove.

    Returns:
    Dict[Any, Any]: The dictionary with keys removed.

    Raises:
    - ValueError: If the input dictionary is empty.
    - TypeError: If the input is not a dictionary.
    """

    if not isinstance(d, dict):
        raise TypeError("Input should be a dictionary.")

    if not d:
        raise ValueError("The input dictionary should not be empty.")

    if isinstance(keys_to_remove, str):
        keys_to_remove = [keys_to_remove]

    new_dict = {}
    for k, v in d.items():
        if k not in keys_to_remove:
            new_dict[k] = remove_keys_recursively(v, keys_to_remove) if isinstance(v, dict) else v

    return new_dict


class CurlCommandParser:
    ParsedCommand = namedtuple(
        "ParsedCommand",
        [
            "method",
            "url",
            "auth",
            "cookies",
            "data",
            "json",
            "header",
            "verify",
        ],
    )

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._setup_parser()

    def _setup_parser(self):
        self.parser.add_argument("command")
        self.parser.add_argument("url")
        self.parser.add_argument("-A", "--user-agent")
        self.parser.add_argument("-I", "--head")
        self.parser.add_argument("-H", "--header", action="append", default=[])
        self.parser.add_argument("-b", "--cookie", action="append", default=[])
        self.parser.add_argument("-d", "--data", "--data-ascii", "--data-binary", "--data-raw", default=None)
        self.parser.add_argument("-k", "--insecure", action="store_false")
        self.parser.add_argument("-u", "--user", default=())
        self.parser.add_argument("-X", "--request", default="")

    @staticmethod
    def is_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def parse(self, curl_command: str) -> ParsedCommand:
        cookies = OrderedDict()
        header = OrderedDict()
        body = None
        method = "GET"

        curl_command = curl_command.replace("\\\n", " ")

        tokens = shlex.split(curl_command)
        parsed_args = self.parser.parse_args(tokens)

        if parsed_args.command != "curl":
            raise ValueError("Not a valid cURL command")

        if not self.is_url(parsed_args.url):
            raise ValueError("Not a valid URL for cURL command")

        data = parsed_args.data
        if data:
            method = "POST"

        if data:
            try:
                body = json.loads(data)
            except json.JSONDecodeError:
                header["Content-Type"] = "application/x-www-form-urlencoded"
            else:
                header["Content-Type"] = "application/json"

        if parsed_args.request:
            method = parsed_args.request

        for arg in parsed_args.cookie:
            try:
                key, value = arg.split("=", 1)
            except ValueError:
                pass
            else:
                cookies[key] = value

        for arg in parsed_args.header:
            try:
                key, value = arg.split(":", 1)
            except ValueError:
                pass
            else:
                header[key.strip()] = value.strip()

        user = parsed_args.user
        if user:
            user = tuple(user.split(":"))

        return self.ParsedCommand(
            method=method,
            url=parsed_args.url,
            auth=user,
            cookies=cookies,
            data=data,
            json=body,
            header=header,
            verify=parsed_args.insecure,
        )

    def parse_to_event(self, curl_command: str) -> Dict[str, Any]:
        parser = CurlCommandParser()
        parsed_command = parser.parse(curl_command)

        method = parsed_command.method
        url = parsed_command.url
        headers = parsed_command.header
        body = parsed_command.data

        # Validate URL
        if not url:
            raise ValueError("Invalid cURL command: URL not found.")

        # Parse the URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        query_string = parsed_url.query
        query_params = parse_qs(query_string)

        body_content = json.dumps(body) if body else ""

        # Construct the event
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": path,
            "rawQueryString": query_string,
            "headers": dict(headers),
            "queryStringParameters": {k: v[0] for k, v in query_params.items()},
            "requestContext": {
                "accountId": "anonymous",
                "apiId": "xxxxx",
                "domainName": parsed_url.hostname,
                "domainPrefix": "xxxxx",
                "http": {
                    "method": method,
                    "path": path,
                    "protocol": "HTTP/1.1",
                    "sourceIp": headers.get("X-Forwarded-For", "127.0.0.1"),
                    "userAgent": headers.get("User-Agent", "")
                },
                "requestId": "13f3120a-9dc8-4f3c-95aa-d51227737286",
                "routeKey": "$default",
                "stage": "$default",
                "time": "08/May/2024:19:56:34 +0000",
                "timeEpoch": 1715198194358
            },
            "body": body_content,
            "isBase64Encoded": False
        }

        return event
