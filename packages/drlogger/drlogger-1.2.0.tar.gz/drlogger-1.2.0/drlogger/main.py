"""main.py contain DrLogger"""

import logging
import typing as t

import graypy

from drlogger.formatter import DrFormatter


class DrLogger:
    """DrLogger initialize Graylog Handler and create structured logs"""

    def __init__(
        self,
        name: str,
        *,
        graylog_host: t.Optional[str] = None,
        graylog_port: t.Optional[int] = None,
        parameter_filter: t.Optional[t.List[str]] = None,
        header_filter: t.Optional[t.List[str]] = None,
        flatten_headers: bool = False,
        flask_app=None,
        handler=None,
    ) -> None:
        """
        DrLogger - create a custom logger

        Args:
            name (str): name of the logger, this can be used as an identifier while filtering logs.
            graylog_host (str): graylog host. Defaults to None.
            graylog_port (int): graylog post for sending logs using UDP. Defaults to None.
            parameter_filter (List[str]): parameters to be excluded from logs. Defaults to None.
            header_filter (List[str]): request header to be excluded from logs. Defaults to None.
            handler: custom handler
        """
        self.logger_name: str = name

        if not handler:
            handler = logging.StreamHandler()
            if graylog_host and graylog_port:
                handler = graypy.GELFUDPHandler(graylog_host, graylog_port)

        formatter = DrFormatter(
            parameter_filter=parameter_filter or [],
            header_filter=header_filter or [],
            flatten_headers=flatten_headers,
            has_flask_app=bool(flask_app),
        )
        handler.setFormatter(formatter)

        self.handler = handler

        if flask_app:
            flask_app.logger.addHandler(self.handler)

    def get_logger(
        self,
        logger_name: t.Optional[str] = None,
        level=logging.INFO,
    ):
        """
        get_logger - instance of Logger

        Args:
            logger_name (Union[str, None], optional): name of the logger,
                this can be used as an identifier while filtering logs. Defaults to None.
            level (str, optional): logging level. Defaults to logging.DEBUG.

        Returns:
            Logger:
        """
        logger: logging.Logger = logging.getLogger(logger_name or self.logger_name)
        logger.setLevel(level)

        logger.addHandler(self.handler)

        return logger
