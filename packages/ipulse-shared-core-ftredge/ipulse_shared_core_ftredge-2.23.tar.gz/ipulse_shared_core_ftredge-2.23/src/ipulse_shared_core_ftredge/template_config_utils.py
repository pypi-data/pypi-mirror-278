def full_update_template(template, updates, logger):
    template_dict = template.copy()
    filtered_updates = {k: v for k, v in updates.items() if k in template}
    template_dict.update(filtered_updates)
    
    # Log warnings for any fields in the template that are not updated
    missing_fields = set(template.keys()) - set(filtered_updates.keys())
    if missing_fields:
        logger.warning(f"Fields in the  template config but not updated: {missing_fields}")
    # Log warnings for any fields in the updates that are not in the template
    extra_fields = set(updates.keys()) - set(template.keys())
    if extra_fields:
        logger.warning(f"Fields in the updates extea to the template config: {extra_fields}. You probably forgot to update the Template Config. Do so now.")
    if extra_fields:
        raise ValueError(f"Updates contain fields not present in the template: {extra_fields}")
    
    return template_dict

def partial_update_template(template, updates, logger):
    template_dict = template.copy()
    filtered_updates = {k: v for k, v in updates.items() if k in template}
    template_dict.update(filtered_updates)

    # Log warnings for any fields in the updates that are not in the template
    extra_fields = set(updates.keys()) - set(template.keys())
    if extra_fields:
        logger.warning(f"Fields in the updates not in the template: {extra_fields}")
    
    if extra_fields:
        raise ValueError(f"Updates contain fields not present in the template: {extra_fields}")
    
    return template_dict