import json
import csv
from io import StringIO
import logging
import os
import traceback
from google.cloud import error_reporting, logging as cloud_logging
from google.api_core.exceptions import NotFound


############################################################################
##################### SETTING UP LOGGER ##########################

####DEPCREACATED: THIS APPROACH WAS GOOD, BUT ERRORS WERE NOT REPORTED TO ERROR REPORTING
# logging.basicConfig(level=logging.INFO)
# logging_client = google.cloud.logging.Client()
# logging_client.setup_logging()
###################################


##### THIS APPROACH IS USED NOW ########
## TODO Fix the issue with POST 0B Nan.... printed in Cloud Logging , which is referring to posting to Cloud Logging probably.
ENV = os.getenv('ENV', 'LOCAL').strip("'")

def setup_gcp_logger_and_error_report(logger_name):
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
############################################################################


############################################################################
##################### GOOGLE CLOUD STORAGE UTILS ##########################

def read_json_from_gcs(bucket_name, file_name, stor_client, logger):
    """ Helper function to read a JSON file from Google Cloud Storage """
    try:
        bucket = stor_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        return data
    except NotFound:
        logger.error(f"Error: The file {file_name} was not found in the bucket {bucket_name}.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error: The file {file_name} could not be decoded as JSON.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return None

def read_csv_from_gcs(bucket_name, file_name, storage_client, logger):
    """ Helper function to read a CSV file from Google Cloud Storage """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data_file = StringIO(data_string)
        reader = csv.DictReader(data_file)
        return list(reader)
    except NotFound:
        logger.error(f"Error: The file {file_name} was not found in the bucket {bucket_name}.")
        return None
    except csv.Error:
        logger.error(f"Error: The file {file_name} could not be read as CSV.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return None

def write_json_to_gcs(bucket_name, file_name, data, stor_client, logger, log_info_verbose=True):
    """ Helper function to write a JSON file to Google Cloud Storage """
    try:
        bucket = stor_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        # Check if data is already a JSON string
        if isinstance(data, str):
            data_string = data
        else:
            data_string = json.dumps(data)
        blob.upload_from_string(data_string, content_type='application/json')
        if log_info_verbose:
            logger.info(f"Successfully wrote JSON to {file_name} in bucket {bucket_name}.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while writing JSON to GCS: {e}", exc_info=True)

def write_csv_to_gcs(bucket_name, file_name, data, storage_client, logger,log_info_verbose=True):
    """ Helper function to write a CSV file to Google Cloud Storage """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_file = StringIO()
        if data and isinstance(data, list) and isinstance(data[0], dict):
            fieldnames = data[0].keys()
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        else:
            raise ValueError("Data should be a list of dictionaries")
        blob.upload_from_string(data_file.getvalue(), content_type='text/csv')
        if log_info_verbose:
            logger.info(f"Successfully wrote CSV to {file_name} in bucket {bucket_name}.")
    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while writing CSV to GCS: {e}", exc_info=True)