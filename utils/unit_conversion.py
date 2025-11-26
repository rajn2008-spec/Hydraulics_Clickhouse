# app/utils/unit_conversion.py

# Input unit conversions
INPUT_CONVERSIONS = {
    ('ft', 'm'): 0.3048,
    ('in', 'm'): 0.0254,
    ('cm', 'm'): 0.01,
    ('gal/min', 'm3/min'): 0.003785,
    ('ft3/min', 'm3/min'): 0.0283168,
    ('l/min', 'm3/min'): 0.001,
    ('lb/gal', 'kg/m3'): 119.83,
    ('lb/ft3', 'kg/m3'): 16.0185,
    ('kg/l', 'kg/m3'): 1000,
    ('min', 's'): 60,
    ('ft/hr', 'm/hr'): 0.3048,
    ('lbf/100ft2', 'n/m2'): 4.788,
    ('in/32', 'm'): 0.00079375,
}

# Output unit conversions
OUTPUT_CONVERSIONS = {
    ('pa', 'psi'): 0.000145,
    ('pa', 'ppg'): 0.000145 * 19.25,
    ('w', 'hp'): 1 / 745.7,
    ('n', 'lbf'): 1 / 4.448,
    ('m/min', 'ft/min'): 3.2808,
    ('kg/m3', 'lb/gal'): 1 / 119.83,
    ('decimal', '%'): 100,
    ('m2', 'in2'): 1550.0031,
    ('m2', 'ft2'): 10.7639,
    ('m2', 'cm2'): 10000,
    ('n/m2', 'lbf/100ft2'): 0.20885,
    ('s^-1', 'min^-1'): 1 / 60,
}

def convert_input_unit(value, from_unit, to_unit):
    """
    Convert input units safely. Returns 0.0 if conversion not found or value invalid.
    """
    if value is None:
        return 0.0
    key = (from_unit.lower(), to_unit.lower())
    factor = INPUT_CONVERSIONS.get(key)
    if factor is None:
        return 0.0
    return value * factor

def convert_output_unit(value, from_unit, to_unit):
    """
    Convert output units safely. Returns 0.0 if conversion not found or value invalid.
    """
    if value is None:
        return 0.0
    key = (from_unit.lower(), to_unit.lower())
    factor = OUTPUT_CONVERSIONS.get(key)
    if factor is None:
        return 0.0
    return value * factor

def mm_to_inches(value):
    return (value or 0.0) / 25.4

def kg_per_m3_to_lb_per_gal(value):
    return (value or 0.0) / 119.83

def m_per_s_to_ft_per_min(value):
    return (value or 0.0) * 196.8504  # 1 m/s = 196.8504 ft/min

def m_s_to_ft_hr(value):
    return (value or 0.0) * 11811.0236  # 1 m/s = 11811.0236 ft/hr

def l_s_to_gal_min(value):
    return (value or 0.0) * 15.8503  # 1 L/s = 15.8503 gal/min
