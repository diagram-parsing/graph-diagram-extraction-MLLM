import re

def simplify_filename(filename: str) -> str:
    if "__" in filename:
        return filename.split("__", 1)[1]
    return filename

def normalize_string(value: str, filename: str = None, mapping_dict: dict = None) -> str:
    """Normalize string by removing underscores, dots, whitespace, lowering case.
    Optionally apply mapping_dict if given."""
    if value is None or value.lower() in ("null", "none"):
        return ""

    if mapping_dict and filename:
        filename = simplify_filename(filename)
        file_map = mapping_dict.get(filename, {})
        if value in file_map:
            mapped_value = file_map[value]
            return re.sub(r"[_\s]+", "", mapped_value.strip()).lower()

    return re.sub(r"[_\s]+", "", value.strip()).lower()
