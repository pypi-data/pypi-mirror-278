import igraph as ig
from packaging import version


def _get_vertex_color(diseases_tree, vertex):
    if vertex["is_diagnosed"]:
        return "green"

    # Check if all children are diagnosed
    children = diseases_tree.tree.es.select(_source=vertex["name"])
    all_children_diagnosed = True
    for child in children:
        if not diseases_tree.tree.vs[child.target]["is_diagnosed"]:
            all_children_diagnosed = False
            break
    if all_children_diagnosed and children:
        return "blue"

    return "red"


def plot_tree(diseases_tree, path: str = "diseases_tree.png"):
    try:
        import cairo  # noqa
    except ImportError:
        raise ImportError(
            "The pycairo package is required for plotting the tree. "
            "It will be installed automatically when you install the "
            "label_tree package with the 'viz' extra."
            "You may also install it using 'pip install pycairo'."
            "Note: pycairo requires the cairo library (not pip installable) "
            "to be installed."
        )

    visual_style = {}
    visual_style["layout"] = diseases_tree.tree.layout("auto")
    visual_style["bbox"] = (12000, 12000)
    visual_style["vertex_label"] = diseases_tree.tree.vs["orig_name"]
    visual_style["vertex_color"] = [
        _get_vertex_color(diseases_tree, vertex) for vertex in diseases_tree.tree.vs
    ]
    visual_style["vertex_shape"] = [
        "rectangle" if is_morphology else "circle"
        for is_morphology in diseases_tree.tree.vs["is_morphology"]
    ]
    visual_style["vertex_label_size"] = 70
    visual_style["vertex_size"] = 50
    visual_style["margin"] = 400
    visual_style["edge_color"] = [
        "red" if m2d else "black"
        for m2d in diseases_tree.tree.es["morphology_to_disease"]
    ]
    visual_style["edge_size"] = [
        2 if m2d else 1 for m2d in diseases_tree.tree.es["morphology_to_disease"]
    ]
    visual_style["keep_aspect_ratio"] = True

    ig.plot(diseases_tree.tree, target=path, **visual_style)


def get_lateset_yaml_version(s3_bucket):
    return max(version.parse(obj.key.split("/")[0]) for obj in s3_bucket.objects.all())
