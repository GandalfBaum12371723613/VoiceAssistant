import logging
from logging.handlers import RotatingFileHandler
import datetime
import colors
import sys

class ColorFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.levelno == logging.INFO:
            return f"{colors.blue}{msg}{colors.reset}"
        elif record.levelno == logging.WARNING:
            return f"{colors.yellow}{msg}{colors.reset}"
        elif record.levelno == logging.ERROR:
            return f"{colors.red}{msg}{colors.reset}"
        return msg

logger = logging.getLogger("VoiceAssistant")
logger.setLevel(logging.DEBUG)

# File handler (no color)
file_handler = RotatingFileHandler(
    f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-assistant.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console handler (with color)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColorFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Logging functions
def log_info(message):
    logger.info(f"      {message}")

def log_warning(message):
    logger.warning(f"      {message}")

def log_error(message):
    logger.error(f"      {message}")
