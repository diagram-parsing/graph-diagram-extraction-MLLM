from utils import normalize_string
from data_loader import build_id_to_text_map

def count_field_matches(label_items, model_items, field, normalize=True):
    """
    Count exact matches (normalized) between label and model items for a given field.
    """
    matches = 0
    model_values = [normalize_string(item.get(field)) if normalize else item.get(field, "") for item in model_items]
    used_indices = set()

    for label_item in label_items:
        label_value = normalize_string(label_item.get(field)) if normalize else label_item.get(field, "")
        for i, model_value in enumerate(model_values):
            if i in used_indices:
                continue

            if label_value == "" and model_value == "":
                matches += 1
                used_indices.add(i)
                break

            if label_value == model_value:
                matches += 1
                used_indices.add(i)
                break

    return matches


def count_arrow_path_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True):
    """
    Count matches for arrow paths (head and tail nodes) between label and model relations.
    Matching is done by exact equality of normalized node texts.
    """
    label_id_to_text = build_id_to_text_map(label_nodes, normalize=normalize)
    model_id_to_text = build_id_to_text_map(model_nodes, normalize=normalize)

    matches = 0
    used = set()

    for l in label_rels:
        label_head = normalize_string(label_id_to_text.get(l.get("head"), "")) if normalize else label_id_to_text.get(l.get("head"), "")
        label_tail = normalize_string(label_id_to_text.get(l.get("tail"), "")) if normalize else label_id_to_text.get(l.get("tail"), "")

        for i, m in enumerate(model_rels):
            if i in used:
                continue

            model_head = normalize_string(model_id_to_text.get(m.get("head"), "")) if normalize else model_id_to_text.get(m.get("head"), "")
            model_tail = normalize_string(model_id_to_text.get(m.get("tail"), "")) if normalize else model_id_to_text.get(m.get("tail"), "")

            if label_head == model_head and label_tail == model_tail:
                matches += 1
                used.add(i)
                break

    return matches

def match_node_text_sets(label_list, model_list):
    """
    Compare two lists of node texts to check if they contain the same values (unordered).
    Each label text must match one distinct model text.
    """
    if not label_list and not model_list:
        return True

    if len(label_list) != len(model_list):
        return False

    used_indices = set()
    for l_text in label_list:
        found = False
        for i, m_text in enumerate(model_list):
            if i in used_indices:
                continue
            if l_text == m_text:
                used_indices.add(i)
                found = True
                break
        if not found:
            return False

    return True


def count_group_node_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=False):
    """
    Count how many label groups have a matching group in the model
    with the same set of node texts (unordered exact match).
    """
    label_text_map = build_id_to_text_map(label_nodes, normalize=normalize)
    model_text_map = build_id_to_text_map(model_nodes, normalize=normalize)
    matches = 0
    used = set()

    for lg in label_groups:
        label_node_ids = lg.get("nodes", [])
        label_node_texts = [label_text_map.get(nid, "") for nid in label_node_ids]

        for j, mg in enumerate(model_groups):
            if j in used:
                continue

            model_node_ids = mg.get("nodes", [])
            model_node_texts = [model_text_map.get(nid, "") for nid in model_node_ids]

            if not label_node_texts and not model_node_texts:
                matches += 1
                used.add(j)
                break

            if match_node_text_sets(label_node_texts, model_node_texts):
                matches += 1
                used.add(j)
                break

    return matches

def match_node_text_class_sets(label_nodes, model_nodes, normalize=True):
    """
    Compare two sets of (text, class) node pairs for an exact normalized match.
    """
    def norm(val):
        return normalize_string(val) if normalize else val or ""

    label_set = {(norm(n.get("text")), norm(n.get("class"))) for n in label_nodes}
    model_set = {(norm(n.get("text")), norm(n.get("class"))) for n in model_nodes}

    return label_set == model_set


def count_node_text_class_matches(label_nodes, model_nodes, normalize=True):
    """
    Count how many (text, class) pairs in label_nodes match with distinct pairs in model_nodes.
    """
    matches = 0
    used_indices = set()

    def norm(val):
        return normalize_string(val) if normalize else val or ""

    model_pairs = [(norm(n.get("text")), norm(n.get("class"))) for n in model_nodes]

    for label_node in label_nodes:
        label_pair = (norm(label_node.get("text")), norm(label_node.get("class")))
        for i, model_pair in enumerate(model_pairs):
            if i in used_indices:
                continue
            if label_pair == model_pair:
                matches += 1
                used_indices.add(i)
                break

    return matches


def count_arrow_path_and_label_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True):
    """
    Count matches for arrow paths (head, tail) and relation labels 
    between label and model relations, using normalized exact matching.
    """
    label_id_to_text = build_id_to_text_map(label_nodes, normalize=normalize)
    model_id_to_text = build_id_to_text_map(model_nodes, normalize=normalize)

    matches = 0
    used = set()

    for l in label_rels:
        label_head = normalize_string(label_id_to_text.get(l.get("head"), "")) if normalize else label_id_to_text.get(l.get("head"), "")
        label_tail = normalize_string(label_id_to_text.get(l.get("tail"), "")) if normalize else label_id_to_text.get(l.get("tail"), "")
        label_label = normalize_string(l.get("label", "")) if normalize else l.get("label", "")

        for i, m in enumerate(model_rels):
            if i in used:
                continue

            model_head = normalize_string(model_id_to_text.get(m.get("head"), "")) if normalize else model_id_to_text.get(m.get("head"), "")
            model_tail = normalize_string(model_id_to_text.get(m.get("tail"), "")) if normalize else model_id_to_text.get(m.get("tail"), "")
            model_label = normalize_string(m.get("label", "")) if normalize else m.get("label", "")

            if label_head == model_head and label_tail == model_tail and label_label == model_label:
                matches += 1
                used.add(i)
                break

    return matches


def count_full_group_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=True):
    """
    Count label groups that match model groups exactly on name, class, and node texts (all normalized).
    """
    matches = 0
    used = set()

    label_text_map = build_id_to_text_map(label_nodes, normalize=normalize)
    model_text_map = build_id_to_text_map(model_nodes, normalize=normalize)

    for lg in label_groups:
        lname = normalize_string(lg.get("name", "")) if normalize else lg.get("name", "")
        lclass = normalize_string(lg.get("class", "")) if normalize else lg.get("class", "")
        ltexts = [label_text_map.get(nid, "") for nid in lg.get("nodes", [])]

        for j, mg in enumerate(model_groups):
            if j in used:
                continue

            mname = normalize_string(mg.get("name", "")) if normalize else mg.get("name", "")
            mclass = normalize_string(mg.get("class", "")) if normalize else mg.get("class", "")
            mtexts = [model_text_map.get(nid, "") for nid in mg.get("nodes", [])]

            if not ltexts and not mtexts and lname == mname and lclass == mclass:
                matches += 1
                used.add(j)
                break

            if lname == mname and lclass == mclass and match_node_text_sets(ltexts, mtexts):
                matches += 1
                used.add(j)
                break

    return matches

def count_node_attribute_matches(label_nodes, model_nodes, normalize=True):
    """Count label nodes whose attribute lists exactly match a model node's, after normalization."""
    matches = 0
    used = set()

    def norm(val):
        return normalize_string(val) if normalize else val or ""

    def norm_list(lst):
        return sorted([norm(x) for x in lst or []])

    for lnode in label_nodes:
        lattrs = norm_list(lnode.get("attributes", []))

        for j, mnode in enumerate(model_nodes):
            if j in used:
                continue

            mattrs = norm_list(mnode.get("attributes", []))

            if lattrs == mattrs:
                matches += 1
                used.add(j)
                break

    return matches


def count_node_method_matches(label_nodes, model_nodes, normalize=True):
    """Count label nodes whose method lists exactly match a model node's, after normalization."""
    matches = 0
    used = set()

    def norm(val):
        return normalize_string(val) if normalize else val or ""

    def norm_list(lst):
        return sorted([norm(x) for x in lst or []])

    for lnode in label_nodes:
        lmeths = norm_list(lnode.get("methods", []))

        for j, mnode in enumerate(model_nodes):
            if j in used:
                continue

            mmeths = norm_list(mnode.get("methods", []))

            if lmeths == mmeths:
                matches += 1
                used.add(j)
                break

    return matches


def count_node_attribute_method_matches(label_nodes, model_nodes, normalize=True):
    """
    Count label nodes that match model nodes exactly on:
    - text
    - class
    - attributes (list)
    - methods (list)
    All normalized before comparison.
    """
    matches = 0
    used = set()

    def norm(val):
        return normalize_string(val) if normalize else val or ""

    def norm_list(lst):
        return sorted([norm(x) for x in lst or []])

    for lnode in label_nodes:
        ltext = norm(lnode.get("text"))
        lclass = norm(lnode.get("class"))
        lattrs = norm_list(lnode.get("attributes", []))
        lmeths = norm_list(lnode.get("methods", []))

        for j, mnode in enumerate(model_nodes):
            if j in used:
                continue

            mtext = norm(mnode.get("text"))
            mclass = norm(mnode.get("class"))
            mattrs = norm_list(mnode.get("attributes", []))
            mmeths = norm_list(mnode.get("methods", []))

            if ltext == mtext and lclass == mclass and lattrs == mattrs and lmeths == mmeths:
                matches += 1
                used.add(j)
                break

    return matches

def count_cardinality_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True):
    """Count matches where only cardinality_start and cardinality_end match between label and model relations."""
    label_id_to_text = build_id_to_text_map(label_nodes, normalize=normalize)
    model_id_to_text = build_id_to_text_map(model_nodes, normalize=normalize)

    matches = 0
    used = set()

    for l in label_rels:
        label_start = normalize_string(l.get("cardinality_start", "")) if normalize else l.get("cardinality_start", "")
        label_end = normalize_string(l.get("cardinality_end", "")) if normalize else l.get("cardinality_end", "")

        for i, m in enumerate(model_rels):
            if i in used:
                continue

            model_start = normalize_string(m.get("cardinality_start", "")) if normalize else m.get("cardinality_start", "")
            model_end = normalize_string(m.get("cardinality_end", "")) if normalize else m.get("cardinality_end", "")

            if label_start == model_start and label_end == model_end:
                matches += 1
                used.add(i)
                break

    return matches

def count_arrow_path_label_class_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True):
    """
    Count matches for arrow paths (head/tail), labels, and class values.
    Includes cardinality fields if present.
    """
    label_id_to_text = build_id_to_text_map(label_nodes, normalize=normalize)
    model_id_to_text = build_id_to_text_map(model_nodes, normalize=normalize)

    matches = 0
    used = set()

    has_arrow_classes = any("class" in rel and rel["class"] for rel in label_rels)
    has_cardinality = any("cardinality_start" in rel and rel["cardinality_start"] for rel in label_rels)

    for l in label_rels:
        label_head = normalize_string(label_id_to_text.get(l.get("head"), "")) if normalize else label_id_to_text.get(l.get("head"), "")
        label_tail = normalize_string(label_id_to_text.get(l.get("tail"), "")) if normalize else label_id_to_text.get(l.get("tail"), "")
        label_label = normalize_string(l.get("label", "")) if normalize else l.get("label", "")
        label_class = normalize_string(l.get("class", "")) if normalize else l.get("class", "")
        label_start = normalize_string(l.get("cardinality_start", "")) if normalize else l.get("cardinality_start", "")
        label_end = normalize_string(l.get("cardinality_end", "")) if normalize else l.get("cardinality_end", "")

        for i, m in enumerate(model_rels):
            if i in used:
                continue

            model_head = normalize_string(model_id_to_text.get(m.get("head"), "")) if normalize else model_id_to_text.get(m.get("head"), "")
            model_tail = normalize_string(model_id_to_text.get(m.get("tail"), "")) if normalize else model_id_to_text.get(m.get("tail"), "")
            model_label = normalize_string(m.get("label", "")) if normalize else m.get("label", "")
            model_class = normalize_string(m.get("class", "")) if normalize else m.get("class", "")
            model_start = normalize_string(m.get("cardinality_start", "")) if normalize else m.get("cardinality_start", "")
            model_end = normalize_string(m.get("cardinality_end", "")) if normalize else m.get("cardinality_end", "")

            head_match = label_head == model_head
            tail_match = label_tail == model_tail
            label_match = label_label == model_label
            class_match = label_class == model_class
            start_match = label_start == model_start
            end_match = label_end == model_end

            if has_cardinality:
                if head_match and tail_match and label_match and class_match and start_match and end_match:
                    matches += 1
                    used.add(i)
                    break
            elif has_arrow_classes:
                if head_match and tail_match and label_match and class_match:
                    matches += 1
                    used.add(i)
                    break
            else:
                if head_match and tail_match and label_match:
                    matches += 1
                    used.add(i)
                    break

    return matches