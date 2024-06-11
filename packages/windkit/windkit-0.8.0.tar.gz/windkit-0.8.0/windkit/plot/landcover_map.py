"""Plot the line maps and polygon maps."""

import numpy as np

import windkit.map_conversion.lines2poly as lines2poly
import windkit.map_conversion.poly2lines as poly2lines


def landcover_map(
    gdf,
    plot_endpoints=False,
    landcover_table=None,
    cmap=None,
    norm=None,
    ignore_collisions=True,
    color_lines=False,
    side="left",
    **kwargs,
):
    """
    Plot the polygons or lines dataframe as a map.

    Parameters
    ----------
    gdf: GeoDataFrame
        the dataframe to plot.
    plot_endpoints : bool, optional. Default: False
        Whether or not to plot the endpoints of the lines / intersections of
        the polygons.
    landcover_table: windkit LandCoverTable or dict or None. Default: None
        Map ids to roughness values.
    cmap : matplotlib.colors.Colormap, optional. Default: None
        If cmap and norm are set to None, use a default colormap.
    norm : matplotlib.colors.BoundaryNorm, optional. Default: None
        If cmap and norm are set to None, use a default norm.
    ignore_collisions : bool, optional. Default: True
        If ignore_collisions is False and thedefault colormap is used, the
        function will raise an error if two different rougness values are
        mapped to the same colors.
    color_lines : bool or string, optional. Default: False
        Used only for plotting lines geodataframe.
        If set to "z0" or "id", use the corresponding value to color lines.
        If True, use "z0" if available else "id".
    side : str, optional. Default: "left"
        Used only for plotting lines geodataframe.
        Whether to use the left or right id or roughness value to color the
        lines, if they are colored.
    """
    if (np.array(gdf.geom_type) == "LineString").all():
        line_map = lines2poly.LineMap(line_gdf=gdf)
        line_map.plot(
            plot_endpoints=plot_endpoints,
            landcover_table=landcover_table,
            color_lines=color_lines,
            side=side,
            cmap=cmap,
            norm=norm,
            ignore_collisions=ignore_collisions,
            **kwargs,
        )
    elif (np.array(gdf.geom_type) == "Polygon").all():
        poly_map = poly2lines.PolygonMap(poly_gdf=gdf)
        poly_map.plot(
            plot_endpoints=plot_endpoints,
            landcover_table=landcover_table,
            cmap=cmap,
            norm=norm,
            ignore_collisions=ignore_collisions,
            **kwargs,
        )
    else:
        raise TypeError(
            "This function requires a line geodataframe of a polygon geodataframe."
        )
