import json

def load_label_data(label_path: str) -> dict:
    """Load label data from a JSON file."""
    with open(label_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_id_to_text_map(nodes: list, normalize: bool = True) -> dict:
    """Create mapping from node ID to text (normalized if specified)."""
    from utils import normalize_string  # avoid circular import issues
    if normalize:
        return {node.get("id"): normalize_string(node.get("text")) for node in nodes}
    return {node.get("id"): node.get("text", "") for node in nodes}