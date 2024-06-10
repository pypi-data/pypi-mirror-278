import logging
import os
import traceback
from google.cloud import error_reporting, logging as cloud_logging


############################################################################
##################### SETTING UP LOGGER ####################################

####DEPCREACATED: THIS APPROACH WAS GOOD, BUT ERRORS WERE NOT REPORTED TO ERROR REPORTING

# logging.basicConfig(level=logging.INFO)
# logging_client = google.cloud.logging.Client()
# # Retrieves a Cloud Logging handler based on the environment
# # you're running in and integrates the handler with the
# # Python logging module. By default this captures all logs
# # at INFO level and higher
# logging_client.setup_logging()
###################################

##### THIS APPROACH IS USED NOW ########
## TODO Fix the issue with POST 0B Nan.... printed in Cloud Logging , which is referring to posting to Cloud Logging probably.

ENV = os.getenv('ENV', 'LOCAL').strip("'")

def setup_gcp_logger_and_error_reporting(logger_name):
    """Sets up a logger with Error Reporting and Cloud Logging handlers.

    Args:
        logger_name: The name of the logger.

    Returns:
        logging.Logger: The configured logger instance.
    """

    class ErrorReportingHandler(logging.Handler):
        def __init__(self, level=logging.ERROR):
            super().__init__(level)
            self.error_client = error_reporting.Client()
            self.propagate = True

        def emit(self, record):
            try:
                if record.levelno >= logging.ERROR:
                    message = self.format(record)
                    if record.exc_info:
                        message += "\n" + ''.join(traceback.format_exception(*record.exc_info))
                    if hasattr(record, 'pathname') and hasattr(record, 'lineno'):
                        message += f"\nFile: {record.pathname}, Line: {record.lineno}"
                    self.error_client.report(message)
            except Exception as e:
                # Ensure no exceptions are raised during logging
                self.handleError(record)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create Error Reporting handler
    error_reporting_handler = ErrorReportingHandler()

    # Create Google Cloud Logging handler
    cloud_logging_client = cloud_logging.Client()
    cloud_logging_handler = cloud_logging_client.get_default_handler()

    # Add handlers to the logger
    logger.addHandler(error_reporting_handler)
    logger.addHandler(cloud_logging_handler)

    # Add a console handler for local development
    if ENV == "LOCAL":
        formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s : %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
