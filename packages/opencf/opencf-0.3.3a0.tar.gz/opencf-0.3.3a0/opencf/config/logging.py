import logging

from opencf_core.logging_config import LoggerConfig

# Create an instance of LoggerConfig
logger_config: LoggerConfig = LoggerConfig()

# Set up logger with default log file location and level
logger_config.setup_logger("opencf", log_file="default", level=logging.INFO)

# Define the logger to log messages
logger: logging.Logger = logger_config.logger
