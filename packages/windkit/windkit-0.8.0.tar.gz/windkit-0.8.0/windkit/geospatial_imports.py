import inspect

# Check importability of geopandas
try:
    import geopandas as _  # nopycln: import

    HAS_GEOPANDAS = True
except (ModuleNotFoundError, ImportError):
    HAS_GEOPANDAS = False


def requires_geopandas():
    try:
        import geopandas as gpd

        return gpd
    except (ModuleNotFoundError, ImportError):
        function_name = inspect.stack()[1].function
        raise ValueError(f"Function {function_name} requires geopandas")


def is_GeoDataFrame(obj):
    if HAS_GEOPANDAS:
        import geopandas as gpd

        return isinstance(obj, gpd.GeoDataFrame)
    else:
        return False


def is_GeoSeries(obj):
    if HAS_GEOPANDAS:
        import geopandas as gpd

        return isinstance(obj, gpd.GeoSeries)
    else:
        return False


# Check importability of rasterio
try:
    import rasterio as _  # nopycln: import

    has_rasterio = True
except (ModuleNotFoundError, ImportError):
    has_rasterio = False


def requires_rasterio():
    if not has_rasterio:
        function_name = inspect.stack()[1].function
        raise ValueError(f"Function {function_name} requires rasterio")
