=====
Usage
=====

A treemap can be generated using the ``treemap`` directive:

.. code-block:: rest

    .. treemap:: parent_name parent_color
        :input: <<outdir>>/coverage_data.xml
        :limits: 90 80 70 0
        :colors: lightgreen orange yellow darkred


:parent_name:

    Mandatory name for the parent group.

:parent_color: *optional*

    Optional color for the parent group, lightgrey by default.

:input: *single argument*

    Path to the input file, relative to your documentation's source directory.
    To make it relative to the output directory instead, use ``<<outdir>>``
    at the start.

:limits: *optional*, *multiple arguments (space-separated)*

    Limits (integers) to use for each range of limits. These are the lower limits and they are inclusive. The last
    value shall be 0 to avoid any issues.
    If this option is unused, the limits from ``treemap_limits`` will be used.

:colors: *optional*, *multiple arguments (space-separated)*

    Colors to use for the groups.
    If this option is unused, the colors from ``treemap_limits`` will be used.
    Note that the number of arguments shall be the same as the number of limits.
