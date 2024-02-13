from logging import Handler, LogRecord

class LogCaptureHandler(Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record: LogRecord):
        self.records.append(record)