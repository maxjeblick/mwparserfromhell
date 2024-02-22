import re


def parse_val_string(s: str):
    """
    Parse string from wikipedia page and return a string in a more readable format.
    For simplcity, in the second example below, we ignore the minus part in the uncertainty value.

    >>> parse_val_string("{{val|3.7|e=10}}")
    '3.7e10'
    >>> parse_val_string("{{val|877.75|0.50|0.44|u=[[second|s]]}}")
    '877.75±0.50 s'
    >>> parse_val_string("{{val|879.6|0.8|u=s}}")
    '879.6±0.8 s'
    >>> parse_val_string("{{val|4|ul=m2}}")
    '4 m2'
    >>> parse_val_string("{{val|5.4|u=[[kg]]&sdot;[[meter|m]]/s<sup>2</sup>}}")
    '5.4 kg·m/s²'
    >>> parse_val_string("{{val|11|x|33}}")
    '11×33'
    >>> parse_val_string("{{val|e=5|ul=m}}")
    '10e5 m'
    """
    try:
        # Matches strings of the format "{{val|value1|value2|value3|u=[[value4|value5]]}}"
        # and returns a string in the format "value1±value2 value5"
        match = re.match(r'{{val\|(.+?)\|(.+?)\|(.+?)\|u=\[\[(.+?)\|(.+?)\]\]\}\}', s)
        if match:
            return f"{match.group(1)}±{match.group(2)} {match.group(5)}"

        # Matches strings of the format "{{val|e=value1|ul=value2}}"
        # and returns a string in the format "10evalue1 value2"
        match = re.match(r'{{val\|e=(.+?)\|ul=(.+?)\}\}', s)
        if match:
            return f"10e{match.group(1)} {match.group(2)}"

        # Matches strings of the format "{{val|value1|e=value2}}"
        # and returns a string in the format "value1evalue2"
        match = re.match(r'{{val\|(.+?)\|e=(.+?)\}\}', s)
        if match:
            return f"{match.group(1)}e{match.group(2)}"

        # Matches strings of the format "{{val|value1|ul=value2}}"
        # and returns a string in the format "value1 value2"
        match = re.match(r'{{val\|(.+?)\|ul=(.+?)\}\}', s)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        # Matches strings of the format "{{val|value1|x|value2}}"
        # and returns a string in the format "value1×value2"
        match = re.match(r'{{val\|(.+?)\|x\|(.+?)\}\}', s)
        if match:
            return f"{match.group(1)}×{match.group(2)}"

        # Matches strings of the format "{{val|value1|fmt=commas}}"
        # and returns a string in the format "value1"
        match = re.match(r'{{val\|(.+?)\|fmt=commas\}\}', s)
        if match:
            return f"{match.group(1)}"

        # Matches strings of the format "{{val|value1|value2|u=value3}}"
        # and returns a string in the format "value1±value2 value3"
        match = re.match(r'{{val\|(.+?)\|(.+?)\|u=(.+?)\}\}', s)
        if match:
            return f"{match.group(1)}±{match.group(2)} {match.group(3)}"

        # Matches strings of the format "{{val|value1|u=[[value2]]&sdot;[[value3|value4]]/s<sup>2</sup>}}"
        # and returns a string in the format "value1 value2·value4/s²"
        match = re.match(r'{{val\|(.+?)\|u=\[\[(.+?)\]\]&sdot;\[\[(.+?)\|(.+?)\]\]/s<sup>2</sup>\}\}', s)
        if match:
            return f"{match.group(1)} {match.group(2)}·{match.group(4)}/s²"

        # If no match is found, return the original string
        return s
    except Exception:
        return s
