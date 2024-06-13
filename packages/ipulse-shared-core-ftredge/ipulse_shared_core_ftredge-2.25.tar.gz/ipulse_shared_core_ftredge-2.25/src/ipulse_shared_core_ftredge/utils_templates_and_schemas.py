import datetime 
from google.cloud import bigquery

def create_bigquery_schema_from_json(json_schema):
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema

def update_check_with_dict_template(template, updates, logger):
    template_dict = template.copy()
    filtered_updates = {k: v for k, v in updates.items() if k in template}
    template_dict.update(filtered_updates)
    # Log warnings for any fields in the updates that are not in the template
    extra_fields = set(updates.keys()) - set(template.keys())
    if extra_fields:
        logger.warning(f"Fields in the updates extra to the template config: {extra_fields}. You probably forgot to update the Template Config. Do so now.")
    return template_dict

def update_check_with_schema_template(updates, schema, logger, dt_ts_to_str=True, check_max_length=True):
    """Ensure Update dict corresponds to the config schema, ensuring proper formats and lengths."""
    template_dict = {field["name"]: None for field in schema}
    schema_dict = {field["name"]: field for field in schema}
    
    for field_name, value in updates.items():
        if field_name in schema_dict:
            field_type = schema_dict[field_name]["type"]
            
            if dt_ts_to_str:
                if field_type == "DATE":
                    value = handle_date_fields(field_name, value, logger)
                elif field_type == "TIMESTAMP":
                    value = handle_timestamp_fields(field_name, value, logger)
            
            if check_max_length and "max_length" in schema_dict[field_name]:
                value = check_and_truncate_length(field_name, value, schema_dict[field_name]["max_length"], logger)
            
            # Set the value in the template dictionary based on the field type
            if field_type == "STRING" and not isinstance(value, str):
                logger.warning(f"Field {field_name} expected to be a string but got {type(value).__name__}.")
                value = str(value)
            elif field_type == "INT64" and not isinstance(value, int):
                logger.warning(f"Field {field_name} expected to be an int but got {type(value).__name__}.")
                try:
                    value = int(value)
                except ValueError:
                    logger.warning(f"Cannot convert value {value} of field {field_name} to int.")
                    value = None
            elif field_type == "FLOAT64" and not isinstance(value, float):
                logger.warning(f"Field {field_name} expected to be a float but got {type(value).__name__}.")
                try:
                    value = float(value)
                except ValueError:
                    logger.warning(f"Cannot convert value {value} of field {field_name} to float.")
                    value = None
            elif field_type == "BOOL" and not isinstance(value, bool):
                logger.warning(f"Field {field_name} expected to be a bool but got {type(value).__name__}.")
                value = bool(value)

            template_dict[field_name] = value
        else:
            logger.warning(f"Field {field_name} not in schema template, it will be ignored.You probably forgot to update the Schema Config. Do so now. "
            "And assess the manual work required to fix missed data.")
    
    return template_dict


def check_updates_formatting(updates, schema, logger, dt_ts_to_str, check_max_length):
    """Processes updates to ensure they match the schema, handling dates, timestamps, and lengths."""
    for field in schema:
        field_name = field["name"]
        field_type = field["type"]

        if field_name in updates:
            value = updates[field_name]

            if dt_ts_to_str:
                if field_type == "DATE":
                    updates[field_name] = handle_date_fields(field_name, value, logger)
                elif field_type == "TIMESTAMP":
                    updates[field_name] = handle_timestamp_fields(field_name, value, logger)

            if check_max_length and "max_length" in field:
                updates[field_name] = check_and_truncate_length(field_name, value, field["max_length"], logger)

    return updates


def handle_date_fields(field_name, value, logger):
    """Handles date fields, ensuring they are in the correct format."""
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, str):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            logger.warning(f"Invalid date format for field {field_name}, expected YYYY-MM-DD")
            return None
    else:
        logger.warning(f"Invalid date format for field {field_name}")
        return None
    

def handle_timestamp_fields(field_name, value, logger):
    """Handles timestamp fields, ensuring they are in the correct format."""
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    elif isinstance(value, str):
        try:
            datetime.datetime.fromisoformat(value)
            return value
        except ValueError:
            logger.warning(f"Invalid timestamp format for field {field_name}, expected ISO format")
            return None
    else:
        logger.warning(f"Invalid timestamp format for field {field_name}")
        return None

def check_and_truncate_length(field_name, value, max_length, logger):
    """Checks and truncates the length of string fields if they exceed the max length."""
    if isinstance(value, str) and len(value) > max_length:
        logger.warning(f"Field {field_name} exceeds max length of {max_length}. Truncating.")
        return value[:max_length]
    return value


