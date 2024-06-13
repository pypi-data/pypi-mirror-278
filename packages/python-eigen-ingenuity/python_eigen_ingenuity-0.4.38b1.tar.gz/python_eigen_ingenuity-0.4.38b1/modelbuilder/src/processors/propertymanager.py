import assetmodelutilities as amu


def remove_leading_chars(string, chars):
    if string:
        while string[0] in chars:
            string = string[1:]
    return string


def validate_property(formatted_property):
    # formatted_property might have a data type as a suffix e.g. name:str
    # If it does, we need to only validate the node_key name amd not the whole string
    # Return validated node_key, retaining the data type if provided
    # For example:
    #    name:str -> name:str
    #    full name -> `full name`
    #    full name:str -> `full name`:str
    validated = ''
    property_name = formatted_property.split(':')[0]
    if property_name:
        validated += amu.validate(property_name)
        # try to re-add the type prefix
        try:
            validated += ':' + formatted_property.split(':')[1]
        except:
            # but don't worry if it's missing
            pass
    else:
        # Return what we were given
        validated = formatted_property

    return validated


def validate_properties(properties):
    # We either get a string, or a list of strings.
    # Process as appropriate and return a string or list of strings to match input
    if properties:
        if isinstance(properties, str):
            return validate_property(properties)
        else:
            return [validate_property(i) for i in properties]
    else:
        return properties


def validate_property_keys(key_list):
    validated = []
    for key in key_list:
        validated += [*validate_properties(i.split(':')[0] for i in key.split(','))]
    return validated


def sort_properties(properties):
    validated = {}
    unwanted = []
    retain = []
    if properties:
        for property in properties:
            for prop in property.strip().split(','):
                # prop has the format key[[:format]:|=value]
                split_prop = prop.replace('=', ':').split(':')
                # Remove leading ! as they are not needed in the key
                valid_key = amu.validate(remove_leading_chars(split_prop[0], '!'))
                if split_prop[0].startswith('!!'):
                    retain.append(valid_key)
                else:
                    # If we have a format and/or value we have a new property to add
                    # ...unless it starts with ! in which case it belongs in the unwanted list (format/value are ignored)
                    if len(split_prop) > 1 and not split_prop[0].startswith('!'):
                        if len(split_prop) == 3:
                            # We have both format and value, so add format to the key so value is properly formatted later
                            validated[valid_key+':'+split_prop[1]] = split_prop[2]
                        else:
                            # Treat second item as the value, because key:format (without a :value) is not supported
                            validated[valid_key] = split_prop[1]
                    else:
                        # Add to the unwanted list
                        unwanted.append(valid_key)

    return validated, unwanted, retain


def combine_required_properties(config_properties, override_properties):
    valid_config_properties, unwanted_config_properties, retain_config_properties = sort_properties(config_properties)
    valid_override_properties, unwanted_override_properties, retain_override_properties = sort_properties(override_properties)

    config_properties = {i: valid_config_properties[i] for i in valid_config_properties if i not in unwanted_override_properties}
    override_properties = {i: valid_override_properties[i] for i in valid_override_properties}
    required_properties = {**config_properties, **override_properties}

    unwanted_properties = [i for i in unwanted_override_properties] + [i for i in unwanted_config_properties if i not in valid_override_properties.keys() and i not in retain_override_properties]

    return required_properties, unwanted_properties


def split_node_key(node):
    split_node = node.split(':')
    if len(split_node) == 1:
        name = node
        type = ''
    else:
        name = split_node[0]
        type = ':' + split_node[1]
    return name, type


def combine_properties(default_properties, actual_properties):
    combined_properties = default_properties.copy()
    for property, value in actual_properties.items():
        if value != '' or property not in default_properties.keys():
            # Either value has been specified in csv
            # or value is blank (can only happen if --allowblanks used) and the property is NOT in the config list
            # (if it is in the list, we use that rather than overriding config value with blank)
            combined_properties[property] = value

    return combined_properties
