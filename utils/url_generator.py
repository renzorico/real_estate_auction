from config import BASE_URL, START_RANGE, END_RANGE, STEP


def generate_property_urls(BASE_URL, START_RANGE, END_RANGE, STEP):
    """
    Generate a list of property URLs based on the specified range.
    """
    property_urls = [
        BASE_URL.format(start, start + STEP)
        for start in range(START_RANGE, END_RANGE, STEP)
    ]
    return property_urls
