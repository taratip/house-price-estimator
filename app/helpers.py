def getPropertyType(arg):
    get_property_type = {
        'CONDO': 'Condo',
        'MULTI_FAMILY': 'Multi-Family',
        'SINGLE_FAMILY': 'Single-Family',
        'TOWNHOUSE': 'Townhouse'
    }

    return get_property_type.get(arg, "Invalid type")
