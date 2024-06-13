"""formatter.py"""

import typing as t

from http.cookies import SimpleCookie

from pythonjsonlogger import jsonlogger


class DrFormatter(jsonlogger.JsonFormatter):
    """
    DrFormatter extends JsonFormatter and add custom filtering on log data

    NOTE: flatten_headers is introduced to handle '-' in header and replace it with "_"
    """

    def __init__(
        self,
        *args,
        parameter_filter: t.Optional[t.List[str]] = None,
        header_filter: t.Optional[t.List[str]] = None,
        has_flask_app: bool = False,
        flatten_headers: bool = False,
        **kwargs
    ):
        self.has_flask_app = has_flask_app
        self.parameter_filter = parameter_filter
        self.header_filter = header_filter
        self.flatten_headers = flatten_headers
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):

        super().add_fields(log_record, record, message_dict)

        log_record["levelname"] = record.levelname
        if record.exc_info:
            log_record["exception_class"] = record.exc_info[0]
            log_record["exception_message"] = repr(record.exc_info[1])

        if self.has_flask_app:
            from flask import has_request_context, request  # pylint: disable=C0415

            if has_request_context():
                log_record.update(self.__get_request_data(request))

    def __get_request_data(self, request_context):
        """
        Get request data.
        """
        # Getting request data
        return_data = {}
        # for GET/ DELETE, request.args is used to get query data
        parameters = {}

        # User's IP address
        parameters["remote_ip"] = (
            request_context.headers.get("X-Real-Ip") or request_context.remote_addr
        )
        # it contains whole host + path + query params path
        # request.url -> http://localhost:8000/v3.1/course_config/i/base_config?a=1&b=1
        # parameters["url"] = request_context.url

        # it contains only path (no host/ no query params)
        # request.path ->  (/v3.1/course_config/i/base_config)
        parameters["path"] = request_context.path

        # Request method
        parameters["request_method"] = request_context.method

        # Action
        parameters["action"] = (
            request_context.endpoint.split(".", 1)[-1]
            if request_context.endpoint
            else None
        )
        parameters["controller"] = (
            request_context.blueprint
            if hasattr(request_context, "blueprint")
            else request_context.module
        )

        try:
            parameters.update(request_context.args.to_dict(flat=False))
        except Exception as err:
            parameters["EXCEPTION_request_args"] = str(err)

        # for POST / PUT, request.json or request.data will be used to get data
        if request_context.method in ["POST", "PUT"]:
            try:
                if request_context.json:
                    parameters.update(request_context.json)
            except Exception as err:
                parameters["req_data"] = str(request_context.data)
                parameters["EXCEPTION_request_json"] = str(err)

        form = request_context.form.to_dict(flat=False)

        for key, value in list(form.items()):
            if len(value) == 1:
                parameters[key] = value[0]
            else:
                parameters[key] = value

        files = request_context.files.to_dict(flat=False)

        for key, value in list(files.items()):
            if len(value) == 1:
                parameters[key] = value[0].filename
            else:
                parameters[key] = [file.filename for file in value]

        headers = dict(request_context.headers.items())
        headers = self.convert_hyphen_to_underscore_headers(headers)

        if request_context.cookies:
            cookies = self.__filter(
                request_context.cookies, "EXCEPTIONAL_COOKIE_FILTER"
            )
            cookie = SimpleCookie()

            for key, value in list(cookies.items()):
                cookie[key] = value

            headers["Cookie"] = cookie.output(header="", sep=";").strip()

        return_data.update(self.__filter(parameters, self.parameter_filter))
        return_data.update(self.__filter(headers, self.header_filter))

        return return_data

    def convert_hyphen_to_underscore_headers(self, headers):
        """
        Replace all header keys having '-' to '_' and create a copy
        """
        if not self.flatten_headers:
            return headers

        modified_header = {}
        for key, value in headers.items():
            modified_header[key.replace("-", "_")] = value
        return modified_header

    def __filter(self, data, filter_name):
        """
        Filter sensitive data.
        """
        _filter = filter_name

        if _filter:
            ret_val = {}

            for key, value in list(data.items()):
                for item in _filter:
                    if item == key:
                        value = "[FILTERED]"
                        break

                ret_val[key] = value
        else:
            ret_val = dict(data)

        return ret_val
