import logging
from pythonjsonlogger import jsonlogger
from sys import stdout

from ..config.singleton import singleton
from ..dig_ass.db import make_session_id


class JsonFormatter(jsonlogger.JsonFormatter):
    pass
    ####
    # additional json formatting possible
    ####

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json_ensure_ascii = False


@singleton
class LoggerSingleton:
    def __init__(self, loggerConfig) -> None:
        self.logger = logging.getLogger(name=loggerConfig['name'])
        self.logger.setLevel(loggerConfig['level_common'])

        stdoutHandler = logging.StreamHandler(stdout)

        # configure logging to stdout
        # stdout_json == True -> set json Formatter
        stdoutJsonFlag = False
        try:
            stdoutJsonFlag = loggerConfig['stdout_json']  # optional config field
        except:
            pass

        if stdoutJsonFlag:
            stdoutFormatter = JsonFormatter(loggerConfig['format_stdout'])
        else:
            stdoutFormatter = logging.Formatter(loggerConfig['format_stdout'])

        stdoutHandler.setFormatter(stdoutFormatter)
        stdoutHandler.setLevel(loggerConfig['level_stdout_handler'])
        self.logger.addHandler(stdoutHandler)

        # configure logging to file
        writeToFileFlag = False
        try:
            writeToFileFlag = loggerConfig['write_to_file']  # optional config field
        except:
            pass

        if writeToFileFlag:
            logFilePath = f'{loggerConfig["file_dir"]}/{loggerConfig["name"]}_{make_session_id()}.json'
            fileHandler = logging.FileHandler(logFilePath, mode='a')
            jsonFormatter = JsonFormatter(loggerConfig['format_file'])
            fileHandler.setFormatter(jsonFormatter)
            fileHandler.setLevel(loggerConfig['level_file_handler'])
            self.logger.addHandler(fileHandler)

    def get(self):
        return self.logger
