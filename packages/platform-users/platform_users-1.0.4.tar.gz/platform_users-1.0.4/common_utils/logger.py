import logging

# def get_logger(name):
#     """This function creates a logger object with the given name and sets the logging level to INFO.
#     It also adds a file handler to the logger which will log messages to the 'logs/clm.log' file.
#     The formatter is set to include the time, name, level, filename, line number, function name and message in the log output.

#     Args:
#         name (str): Name of the logger.

#     Returns:
#         Logger: Logger object.
#     """
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
#     file_handler = logging.FileHandler('logs/clm.log')
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)
#     return logger


import os

def get_logger(name):
    """This function creates a logger object with the given name and sets the logging level to INFO.
    It also adds a file handler to the logger which will log messages to the 'logs/clm.log' file.
    The formatter is set to include the time, name, level, filename, line number, function name and message in the log output.

    Args:
        name (str): Name of the logger.

    Returns:
        Logger: Logger object.
    """
    # Check if the 'logs' directory exists, create it if not
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Define the log file path
    log_file_path = os.path.join(logs_dir, 'core.log')

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if the log file exists, create it if not
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()

    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger



import logging

class CRUDLogger:
    def __init__(self, logger_name, log_level=logging.INFO):
        self.logger = get_logger(logger_name)

    def _log_message(self, template, *args):
        log_message = template.format(*args)
        self.logger.info(log_message)

    def log_get_details(self, entity_name, entity_id):
        self._log_message('Getting {} details for ID {}.', entity_name, entity_id)

    def log_get_all(self, entity_name):
        self._log_message('Getting all {} data.', entity_name)

    def log_retrieved(self, entity_name, entity_id):
        self._log_message('{} with ID {} retrieved successfully.', entity_name, entity_id)

    def log_error(self, exception_message):
        self._log_message('An exception occurred: {}', exception_message)

    def log_object_not_found(self, entity_name, entity_id):
        self._log_message('No {} details found for ID {}', entity_name, entity_id)

    def log_creating(self, entity_name):
        self._log_message('Creating a {}.', entity_name)

    def log_created(self, entity_name, data):
        self._log_message('{} created successfully with data {}.', entity_name, data)

    def log_updating(self, entity_name, entity_id):
        self._log_message('Updating {} with ID {}', entity_name, entity_id)

    def log_updated(self, entity_name, entity_id):
        self._log_message('{} with ID {} updated successfully.', entity_name, entity_id)

    def log_partially_updated(self, entity_name, entity_id):
        self._log_message('{} with ID {} partially updated successfully.', entity_name, entity_id)

    def log_deleting(self, entity_name, entity_id):
        self._log_message('Deleting user with ID {}.', entity_id)

    def log_deleted(self, entity_name, entity_id):
        self._log_message('{} with ID {} deleted successfully.', entity_name, entity_id)

    def log_delete_failed(self, entity_name):
        self._log_message('Unable to delete {}.', entity_name)

    def log_data_retrieved(self, entity_name):
        self._log_message('{} data retrieved successfully.', entity_name)

    def log_data_not_found(self, entity_name):
        self._log_message('No {} data found.', entity_name)

# # Example of how to use the CRUDLogger in your update view
# class YourClass:
#     def __init__(self):
#         # Initialize your logger
#         self.logger = CRUDLogger(__name__)

#     def update_subscription_plan_mapping(self, request):
#         try:
#             # Your update logic here...

#             # Log the update operation
#             self.logger.log_updating(self.object_name, entity_id)

#             return generate_response(
#                 status=status.HTTP_201_CREATED,
#                 message=FeatureServicePlanMappingMessages().feature_service_plan_mapping_added_message(),
#             )

#         except ValidationError as validation_error:
#             self.logger.log_error('Validation error: {}', validation_error)
#             return handle_exception(validation_error)

#         except Exception as e:
#             self.logger.log_error('Unexpected error: {}', e)
#             return handle_exception(e)
