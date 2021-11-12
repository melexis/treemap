=============
Configuration
=============

The *conf.py* file contains the documentation configuration for your project. This file needs to be equipped in order
to configure this Sphinx plugin.

The plugin needs to be added to the list of *extensions*:

.. code-block:: bash

    extensions = [
        'mlx.treemap',
    ]

--------------------------------------
Custom Colors for Coverage Percentages
--------------------------------------

The plugin allows customization of the colors for each range of coverage that you want to use. The key values shall be
numbers that signify the lower limit (inclusive). The default values below can be overridden by defining a
dictionary called `treemap_limits` in your *conf.py* file.

.. code-block:: python

    treemap_limits = {
        90: '#A7FC9D',  # green
        75: '#FFEA20',  # yellow
        0: '#FF0000',  # red
    }

---------------------------
HTML-Specific Configuration
---------------------------

You can choose to either embed the `plotly.js`_ graphing library for every treemap or to add it as a source file once
by defining a boolean variable called ``treemap_include_plotlyjs`` in your *conf.py* file.
This library is needed to render the interactive treemap.


If ``True``, the plotly.js library is embedded in each HTML elemenent generated for by a ``treemap`` directive.

.. code-block:: python

    treemap_include_plotlyjs = True

If ``False``, the plotly.js library shall be added to your documentation build in the ``setup`` function in your
*conf.py*. You can find the latest CDN link here_.

.. code-block:: python

    treemap_include_plotlyjs = False
    def setup(app):
        app.add_js_file('https://cdn.plot.ly/plotly-2.4.2.min.js')

The default value is ``True``.

.. _`plotly.js`: https://plotly.com/graphing-libraries/
.. _here: https://plotly.com/javascript/getting-started/
..
    --------------------------
    Other Format Configuration
    --------------------------

    The plugin generates treemaps in the SVG vector format. You can configure the location of these images
    relative to Sphinx' output directory by defining the ``treemap_image_dir`` variable in your *conf.py* file.
    The default configuration is the following:

    .. code-block:: python

        treemap_image_dir = 'images'
