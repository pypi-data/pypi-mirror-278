.. _plotting_user_guide:

Plotting User Guide
===================

The user guide provides helpful tips about the different plotting utilities, as well as notes about how to export the plots to common formats.

Statistical Plots
-----------------

Statistical plots are plotted using the `Plotly <https://plotly.com>`_ Python library, which creates interactive plots. These plots can be displayed inline in Jupyter or opened directly in your browser when using the interpreter. The interactive plots allow you to analyze your results without losing any detail by using the hovering, zoom and region selection functionalities. Moreover, it is possible to save the files as images, e.g. ``.png``, ``pdf``, ``webp``, or for display on the web as either ``.json`` or ``.html``.

Some statistical plots are combined to create simple dash boards using the  `Dash <https://dash.plotly.com/>`_ Python library. Dash is written on top of Plotly and allows the creation of highly interactive plots. Dash apps are rendered in the browser and can also be displayed inline in Jupyter.


Color selection
^^^^^^^^^^^^^^^^
Plotly has a number of built-in color scales that can be specified on some plots of the plots. The most common color scales used are `Sequential Color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Cyclical Color scales <https://plotly.com/python/builtin-colorscales/#builtin-cyclical-color-scales>`_ .

For plots with a single color, you can use `CSS named colors <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_ or RGB values identifiers to specify the color used.

Both Dash and Plotly use the above mentioned color scales and CSS named colors.


Plotly plots
^^^^^^^^^^^^
When working with Plotly plots, the following can be done:


Exporting and displaying Plotly figures
"""""""""""""""""""""""""""""""""""""""

The different Plotly figures can be exported and/or displayed in the following formats according to your necessities. Once you have the figure object or dictionary representing the figure ("fig"), the following methods can be used:

* :py:meth:`.show() <plotly:plotly.basedatatypes.BaseFigure.show>`
  For launching directly the plots in the browser, or display inline in Jupyter.
  As an example, assuming that you have a :py:class:`Figure <plotly:plotly.graph_objects.Figure>` object saved in "fig", when you call ``fig.show()`` from the interactive python environment it will open the plot in your browser. Once in the browser, you get an interactive plot, where you can hover to get relevant information of the plot, zoom in and zoom out, select different regions to look in with more detail, and even download the plot as a .png image by using the upper right corner options. After zooming, you can return to the full plot by double clicking anywhere on the plot.

* :py:meth:`.to_json() <plotly:plotly.basedatatypes.BaseFigure.to_json>` and :py:meth:`.write_json() <plotly:plotly.basedatatypes.BaseFigure.write_json>`:

  Converts the figure to a JSON string representation or saves the JSON as a text file. This allows you to use plotly's JavaScript library to display the image on a website.

  If you are doing a lot of encoding, particularly if you are sending via an API, you may want to look at installing `orjson <https://github.com/ijl/orjson>`_, and using the ``engine="orjson"`` argument.

* :py:meth:`.to_html() <plotly:plotly.basedatatypes.BaseFigure.to_html>` and :py:meth:`.write_html() <plotly:plotly.basedatatypes.BaseFigure.write_html>`:

  Convert the figure to a single HTML page. By default this will create a stand-alone HTML page with the entire plotlyJS code embedded in the file, so that you can send the page to anyone for display.

  Some useful options include:

  * ``include_plotlyjs="CDN"``: This can be used if you are sure that whoever will view the HTML page is connected to the internet when viewing. It will reduce the size of the file by about 3MB, as the plotlyJS script will be downloaded from the web rather than embedded inside of the file itself.

  * ``full_html=False``: This will remove the ``<html>`` and ``<body>`` tags, producing a single ``<div>`` that contains the plotlyJS script and the JSON representation of the figure. This allows it to be embedded inside an existing HTML document.

* :py:meth:`.to_image() <plotly:plotly.basedatatypes.BaseFigure.to_image>` and :py:meth:`.write_image() <plotly:plotly.basedatatypes.BaseFigure.write_image>`:

  Outputs the figure as an image, ``to_image`` converts the figure to a static image bytes object, while ``write_image`` saves it to a file. Common file formats are supported, and most often you will use ``"png"`` or ``"pdf"``.

  In order to use those two functions all you need to do is install the `Kaleido package <https://github.com/plotly/Kaleido>`_ and use the ``plotly.io.write_image`` and ``plotly.io.to_image`` function directly.


Showing Plotly figures in Jupyter Notebook and Lab
""""""""""""""""""""""""""""""""""""""""""""""""""

As Jupyter Notebook and Lab are web based, plotly plots can be viewed directly in your notebook. The process to follow is the same as displaying the plots in the browser, calling the ``.show()`` function of the figure object. It is also possible to export/display the figure object in the previously presented formats.


Dash apps
^^^^^^^^^
By default, Dash apps run in a ``localhost`` Python server which needs to be activated and deactivated manually. To share a Dash app, you need to "deploy" it to a server. For the moment, the Dash app sharing is not operative.

When working with Dash apps, the following can be done:


Exporting and displaying Dash apps
""""""""""""""""""""""""""""""""""

Dash apps cannot be exported, but can only be displayed through running the code to and activating the server.

Thus, once you get the ``dash.Dash`` object (e.g. "app") it can be displayed into the browser by running the server using the following command: ``app.run_server(debug=False)``. Once the server is running, the interactive app can be used from your browser.

For closing the server you just need to press ``CTRL+C`` to quit.


Running Dash apps in Jupyter Notebook and Lab
""""""""""""""""""""""""""""""""""""""""""""""""""

As Jupyter Notebook and Lab are web based, Dash apps can be used directly from your Notebook by installing the `JupyterDash Python package <https://pypi.org/project/jupyter-dash/>`_ which will enable you to work interactively with the apps within Jupyter environments.

When working the Jupyter Notebook or Lab it is possible to display the app inline in the Notebook or launching it to the browser; this option is chosen when starting the server.

For starting the server use ``app.run_server(debug = False, mode = "inline", port = 8050)`` where:

  * ``debug`` defines the activation or deactivation of the Dev Tools features. It is recommended to turn them off.
  * ``mode`` defines where the app is displayed: "inline" displays it directly in your Notebook and "external" creates the link for launching the app to the browser.
  * ``port`` defines the server port. By defining it here, you will be able to close the server easily later.

For the server deactivation use ``app._terminate_server_for_port("localhost", port = 8050)``. Make sure that the ``port`` is the same as the one used in the server activation.


Maps
----

Map plots are plotted using `geopandas <https://geopandas.org/>`_ and `xarray <http://xarray.pydata.org>`_ functions directly to show an overview of an area. Both provide a high level interface to the popular `matplotlib <https://matplotlib.org/>`_ library for making maps, so ``matplotlib`` has to be installed before either ``xarray`` or ``geopandas`` can plot. Map plots can be displayed inline in Jupyter or opened automatically in a pop-up window. Moreover, it is possible to save the files as images, e.g. ``.png``, ``.pdf``,  ``.jpg`` or ``.eps``.


Color selection
^^^^^^^^^^^^^^^^
Matplotlib has a number of built-in colormaps that can be specified on some of the plots. The most common ones used are `Sequential colormaps <https://matplotlib.org/stable/tutorials/colors/colormaps.html#sequential>`_ and `Diverging colormaps <https://matplotlib.org/stable/tutorials/colors/colormaps.html#diverging>`_ .

There are occasions where single colors are used in the plots for representing lines or points. You can use `CSS named colors <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_ or RGB values identifiers to specify the color used.

Default colormaps for ``z0meso``, ``site_elev``, ``*_speedups``, and ``*_turnings`` are specified as part of the package. For other variables, `xarray.plot.pcolormesh` is used to determine if the plot is sequential or diverging and an appropriate colormap is specified.


Exporting map figures
^^^^^^^^^^^^^^^^^^^^^

The different map figures can be exported in different formats according to your requirements. Once you have the :py:class:`matplotlib.collections.QuadMesh <https://matplotlib.org/stable/api/collections_api.html#matplotlib.collections.QuadMesh>` object (output of the plotting function) you can use the following method:

* :py:meth:`.savefig() <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig>`
  For saving a figure to a static image bytes object.
  As an example, assuming that you have a :py:class:`matplotlib.collections.QuadMesh <https://matplotlib.org/stable/api/collections_api.html#matplotlib.collections.QuadMesh>` object saved in "map", when you call ``map.figure.savefig(fname = "elevation_map.pdf")`` the figure is saved with the specified name and ``.pdf`` format. The format can also be specified by the ``format`` argument.  If the format is not specified, by default it will be saved as a ``.png`` file.


Showing maps in Jupyter Notebook and Lab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Map plots can be viewed directly in your notebook. Once you execute the function, the figure will be displayed inline by default, to plot it manually just need to add the ``.figure`` prefix to the output. It is also possible to export the plot in the previously presented formats.
