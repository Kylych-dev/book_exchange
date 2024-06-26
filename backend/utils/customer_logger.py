import logging


class CustomJsonFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_fields = [
            "asctime",
            "levelname",
            "pathname",
            "message",
            "Exception",
            "Class",
        ]

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "Class": getattr(record, "Class"),
            "Exception": getattr(record, "Exception"),
        }

        formatted_record = "\n".join(
            [f"{key}: {value}" for key, value in log_record.items()]
        )
        return formatted_record
    
    @staticmethod
    def run():
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(CustomJsonFormatter())
            logger.addHandler(console_handler)
        return logger


def log_warning(view, ex=None):
    CustomJsonFormatter.run().warning(
        f"Продукт не найден",
        extra={
            "Exception": f"{ex}",
            "Class": f"{view.__class__.__name__}.{view.action}",
        }
    )


def log_error(view, ex=None):
    CustomJsonFormatter.run().error(
        f"Ошибка при обработке запроса",
        extra={
            "Exception": f"{ex}",
            "Class": f"{view.__class__.__name__}.{view.action}",
        }
    )