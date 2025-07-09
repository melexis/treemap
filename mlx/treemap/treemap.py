from mlx.treemap._version import version
from mlx.treemap.treemap_directive import Treemap, TreemapDirective


def process_item_nodes(app, doctree, fromdocname):
    """This function should be triggered upon ``doctree-resolved`` event.

    Replaces all Treemap nodes with a treemap visualization.
    """
    for i, node in enumerate(doctree.traverse(Treemap)):
        node.perform_replacement(app)


def setup(app):
    """Extension setup."""
    app.add_config_value(
        'treemap_limits',
        {
            90: '#A7FC9D',  # green
            75: '#FFEA20',  # yellow
            0: '#FF0000',  # red
        },
        'env',
    )
    app.add_config_value(
        'treemap_include_plotlyjs',
        False,
        'env',
    )

    app.add_node(Treemap)
    app.add_directive('treemap', TreemapDirective)
    app.connect('doctree-resolved', process_item_nodes)

    return {'version': version}
