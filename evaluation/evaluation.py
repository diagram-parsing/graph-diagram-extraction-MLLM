import copy

from matching import (
    count_field_matches,
    count_node_text_class_matches,
    count_arrow_path_matches,
    count_arrow_path_and_label_matches,
    count_arrow_path_label_class_matches,
    count_group_node_matches,
    count_full_group_matches,
    count_node_attribute_method_matches,
    count_node_method_matches,
    count_node_attribute_matches,
    count_cardinality_matches,
)

def evaluate_output(label_data, model_output, dataset_name=None, image_key=None, mapping_dictionary=None):
    """Compare model output to label data using exact and normalized matching."""

    # Extract label nodes, relations, groups and their attributes/methods
    label_nodes = label_data.get("nodes") or []
    label_rels = label_data.get("relations") or []
    label_groups = label_data.get("groups") or []

    label_attributes = []
    for node in label_nodes:
        node["attributes"] = node.get("attributes") or []
        label_attributes.extend(node["attributes"])

    label_methods = []
    for node in label_nodes:
        node["methods"] = node.get("methods") or []
        label_methods.extend(node["methods"])

    label_cardinalities = []
    for rel in label_rels:
        rel["cardinality_start"] = rel.get("cardinality_start") or ""
        label_cardinalities.append(rel["cardinality_start"])

    model_output = model_output if isinstance(model_output, dict) else None
    if model_output is None:
        print("Model output is None")
        return None

    original_model_nodes = model_output.get("nodes") or []
    model_rels = model_output.get("relations") or []
    model_groups = model_output.get("groups") or []

    if dataset_name and image_key:
        mapping_key = f"{dataset_name}__{image_key}"
        mapping_for_image = mapping_dictionary.get(mapping_key, {})

        if mapping_for_image:
            model_nodes = copy.deepcopy(original_model_nodes)

            for node in model_nodes:
                original_text = node["text"].lower() if node["text"] else node["text"]
                if original_text in mapping_for_image:
                    corrected_text = mapping_for_image[original_text]
                    node["text"] = corrected_text
        else:
            model_nodes = original_model_nodes
    else:
        model_nodes = original_model_nodes

    model_attributes = []
    for node in model_nodes:
        node["attributes"] = node.get("attributes") or []
        model_attributes.extend(node["attributes"])

    model_methods = []
    for node in model_nodes:
        node["methods"] = node.get("methods") or []
        model_methods.extend(node["methods"])

    model_cardinalities = []
    for rel in model_rels:
        rel["cardinality_start"] = rel.get("cardinality_start") or ""
        model_cardinalities.append(rel["cardinality_start"])

    try:
        result = {
            "label": {
                "nodes": len(label_nodes),
                "relations": len(label_rels),
                "groups": len(label_groups),
                "attributes": len(label_attributes),
                "methods": len(label_methods),
                "cardinalities": len(label_cardinalities),
            },
            "model": {
                "nodes": len(model_nodes),
                "relations": len(model_rels),
                "groups": len(model_groups),
                "attributes": len(model_attributes),
                "methods": len(model_methods),
                "cardinalities": len(model_cardinalities),
            },
            "exact_matches": {
                "node_texts": count_field_matches(label_nodes, model_nodes, "text", normalize=False),
                "node_classes": count_field_matches(label_nodes, model_nodes, "class", normalize=False),
                "node_text_and_class": count_node_text_class_matches(label_nodes, model_nodes, normalize=False),
                "arrow_labels": count_field_matches(label_rels, model_rels, "label", normalize=False),
                "arrow_classes": count_field_matches(label_rels, model_rels, "class", normalize=False),
                "group_names": count_field_matches(label_groups, model_groups, "name", normalize=False),
                "group_classes": count_field_matches(label_groups, model_groups, "class", normalize=False),
                "arrow_path": count_arrow_path_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=False),
                "arrow_path_and_label": count_arrow_path_and_label_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=False),
                "arrow_path_label_class": count_arrow_path_label_class_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=False),
                "group_texts": count_group_node_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=False),
                "group_name_class_texts": count_full_group_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=False),
                "attribute_method_text_class": count_node_attribute_method_matches(label_nodes, model_nodes, normalize=False),
            },
            "normalized_matches": {
                "node_texts": count_field_matches(label_nodes, model_nodes, "text", normalize=True),
                "node_classes": count_field_matches(label_nodes, model_nodes, "class", normalize=True),
                "node_text_and_class": count_node_text_class_matches(label_nodes, model_nodes, normalize=True),
                "arrow_labels": count_field_matches(label_rels, model_rels, "label", normalize=True),
                "arrow_classes": count_field_matches(label_rels, model_rels, "class", normalize=True),
                "group_names": count_field_matches(label_groups, model_groups, "name", normalize=True),
                "group_classes": count_field_matches(label_groups, model_groups, "class", normalize=True),
                "arrow_path": count_arrow_path_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True),
                "arrow_path_and_label": count_arrow_path_and_label_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True),
                "arrow_path_label_class": count_arrow_path_label_class_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True),
                "group_texts": count_group_node_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=True),
                "group_name_class_texts": count_full_group_matches(label_groups, model_groups, label_nodes, model_nodes, normalize=True),
                "attribute_method_text_class": count_node_attribute_method_matches(label_nodes, model_nodes, normalize=True),
                "node_methods": count_node_method_matches(label_nodes, model_nodes, normalize=True),
                "node_attributes": count_node_attribute_matches(label_nodes, model_nodes, normalize=True),
                "arrow_cardinalities": count_cardinality_matches(label_rels, model_rels, label_nodes, model_nodes, normalize=True),
            },
        }

    except Exception as e:
        print(f"Error in evaluate_output: {e}")
        raise

    return result