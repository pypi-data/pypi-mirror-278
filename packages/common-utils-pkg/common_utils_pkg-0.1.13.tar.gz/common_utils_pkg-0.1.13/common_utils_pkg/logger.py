import logging.handlers
from .notifications import NotificationHandler

from datetime import datetime


MAX_ROWS_FOR_FILE = 300_000


class Logger:
    Logger = None
    NotificationHandler = None

    def __init__(
        self,
        logging_service,
        telegram_api_key=None,
        telegram_chat_ids=None,
        enable_notifications=True,
        enable_console_log=True,
        enable_file_log=True,
        max_rows_for_file=MAX_ROWS_FOR_FILE,
    ):
        if not logging_service:
            raise Exception("logging_service parameter is not specified")

        self.service_name = logging_service
        self.enable_file_log = enable_file_log
        self.enable_console_log = enable_console_log
        self.max_rows_for_file = max_rows_for_file

        self.Logger = self.create_new_logger(self.service_name, self.enable_file_log, self.enable_console_log)
        self.written_rows = 0

        # notification handler
        self.NotificationHandler = NotificationHandler(
            telegram_api_key=telegram_api_key,
            telegram_chat_ids=telegram_chat_ids,
            enabled=enable_notifications,
        )

        self.info(f"----------------- Starting logger: {self.service_name} -----------------")

    def create_new_logger(self, service_name, enable_file_log=True, enable_console_log=True):
        date_str = datetime.now().isoformat("_").replace(":", "-").replace(".", "-")
        logger_name = f"{service_name}_{date_str}"

        Logger = logging.getLogger(logger_name)
        Logger.setLevel(logging.DEBUG)
        Logger.propagate = False
        formatter = logging.Formatter(
            "{asctime} [{levelname:7}] {threadName} {service}: {message}",
            # {filename}.{funcName}({lineno})
            # TODO: create custom handler to use file
            # https://habr.com/ru/articles/513966/
            style="{",
        )

        if enable_file_log:
            fh = logging.FileHandler(f"logs/{logger_name}.log")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            Logger.addHandler(fh)

        # logging to console
        if enable_console_log:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            Logger.addHandler(ch)

        Logger = logging.LoggerAdapter(Logger, {"service": service_name})

        return Logger

    def log(self, message, level="info", notify=False):
        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

        if notify and self.NotificationHandler.enabled:
            emoji = ""
            if level == "info":
                emoji = "ℹ️"
            elif level == "warning":
                emoji = "⚠️"
            elif level == "error":
                emoji = "❌"

            self.NotificationHandler.send_notification(f"{emoji} {self.service_name}: {message}")

        self.written_rows += 1

        if self.written_rows >= self.max_rows_for_file:
            self.Logger = self.create_new_logger(self.service_name, self.enable_file_log, self.enable_console_log)
            self.written_rows = 0

    def info(self, message, notify=False):
        self.log(message, "info", notify)

    def warning(self, message, notify=False):
        self.log(message, "warning", notify)

    def error(self, message, notify=False):
        self.log(message, "error", notify)

    def debug(self, message, notify=False):
        self.log(message, "debug", notify)

    def create_prefix(self, prefix):
        return Prefixer(logger=self, prefix=prefix)


class Prefixer(Logger):
    def __init__(self, logger: Logger, prefix):
        self.prefix = prefix
        self.logger = logger

    def info(self, message, notify=False):
        self.logger.info(message=f"{self.prefix}: {message}", notify=notify)

    def warning(self, message, notify=False):
        self.logger.warning(message=f"{self.prefix}: {message}", notify=notify)

    def error(self, message, notify=False):
        self.logger.error(message=f"{self.prefix}: {message}", notify=notify)

    def debug(self, message, notify=False):
        self.logger.debug(message=f"{self.prefix}: {message}", notify=notify)
