import logging
import pathlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast

from .filters import CustomExcludeFilter, IgnoreRootFilter
from .formatters import ConsoleFormatter
from .loggers import CustomLogger


@dataclass
class ItakelloLogging:

    debug_mode: bool = field(init=False)
    handlers: list[logging.Handler] = field(init=False)
    folder: pathlib.Path = field(init=False)

    def __init__(
        self,
        excluded_modules: list[str] = [],
        debug: bool = False,
        exclude_root: bool = False,
    ) -> None:
        logging.setLoggerClass(CustomLogger)
        self.debug_mode = debug
        self.folder = self._create_folder("logs")
        handlers = self._get_handlers(excluded_modules, exclude_root)
        logging.basicConfig(level=logging.DEBUG, handlers=handlers, force=True)

    @staticmethod
    def get_logger(name: str) -> CustomLogger:
        return cast(CustomLogger, logging.getLogger(name))

    def _create_folder(self, f_name: str) -> pathlib.Path:
        folder = pathlib.Path(f_name)
        folder.mkdir(exist_ok=True, parents=True)
        return folder

    def _get_handlers(
        self, excluded_loggers: list[str], exclude_root: bool
    ) -> list[logging.Handler]:
        handlers: list[logging.Handler] = [
            self._get_stream_handler(),
            self._get_file_handler(),
        ]
        filters = self._get_filters(excluded_loggers, exclude_root)
        for handler in handlers:
            for filter in filters:
                handler.addFilter(filter)
        return handlers

    def _get_filters(
        self, excluded_loggers: list[str], exclude_root: bool
    ) -> list[logging.Filter]:
        filters: list[logging.Filter] = []
        filters.append(CustomExcludeFilter(modules=excluded_loggers))
        if exclude_root:
            filters.append(IgnoreRootFilter())
        return filters

    def _get_stream_handler(self) -> logging.StreamHandler:
        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        console_formatter = ConsoleFormatter("%(message)s")
        s_handler.setFormatter(console_formatter)
        return s_handler

    def _get_file_handler(self) -> logging.FileHandler:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        f_handler = logging.FileHandler(self.folder / f"{current_time}.log")
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        return f_handler


if __name__ == "__main__":
    ItakelloLogging(debug=True, excluded_modules=[], exclude_root=False)
    logging.debug("Test debug message from core.py with root logger")
    logging.info("Test info message from core.py with root logger")
    logging.warning("Test warning message from core.py with root logger")
    logging.error("Test error message from core.py with root logger")
    logging.critical("Test critical message from core.py with root logger")
    logger = ItakelloLogging.get_logger(__name__)
    logger.debug("Test debug message from core.py with custom logger")
    logger.info("Test info message from core.py with custom logger")
    logger.confirmation("Test confirmation message from core.py with custom logger")
    logger.warning("Test warning message from core.py with custom logger")
    logger.error("Test error message from core.py with custom logger")
    logger.critical("Test critical message from core.py with custom logger")
