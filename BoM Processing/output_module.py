
def get_output(capacity, irradiance):
    if capacity > 99999: return 0
    if irradiance > 99999: return 0
    return capacity * irradiance * (1.0/5.5)
