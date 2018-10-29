import math

# Get property type


def getPropertyType(arg):
    get_property_type = {
        'APARTMENT': 'Apartment',
        'CONDO': 'Condo',
        'MULTI_FAMILY': 'Multi Family',
        'SINGLE_FAMILY': 'Single Family',
        'TOWNHOUSE': 'Townhouse'
    }

    return get_property_type.get(arg, "Invalid type")

# Get cluster group based on neighborhood


def getGroup(arg):
    group = 'Invalid neighborhood'

    get_group = {
        ('Allston', 'Bay Village', 'Beacon Hill', 'Chinatown', 'Downtown',
         'Downtown Crossing', 'Fenway', 'Kenmore', 'Leather District',
         'Mission Hill', 'North End', 'West End', 'Winthrop'): 'low_freq',
        ('Brighton', 'Charlestown', 'East Boston', 'Hyde Park', 'Jamaica Plain',
         'Mattapan', 'North Dorchester', 'Roslindale', 'Roxbury', 'South Boston',
         'South Dorchester', 'West Roxbury'): 'low_price_high_freq',
        ('Back Bay', 'South End'): 'high_price_high_freq'
    }

    for k, v in get_group.items():
        if arg in k:
            group = v

    return group


def abbrNumber(number):
    SI_SYMBOL = ['', 'k', 'M']
    # what tier? (determines SI symbol)
    tier = math.log10(number) // 3

    # if zero, we don't need a suffix
    if(tier == 0):
        return "{}".format(number)

    # get suffix and determine scale
    suffix = SI_SYMBOL[int(tier)]
    scale = math.pow(10, tier * 3)

    # scale the number
    scaled = number / scale

    # format number and add suffix
    return "{:.2f} {}".format(scaled, suffix)
