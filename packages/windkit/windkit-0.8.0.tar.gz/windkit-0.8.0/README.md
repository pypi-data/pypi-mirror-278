# WindKit

WindKit provides the following core sets of functionalities for working with wind resource data:

- Read and write common data formats, and provide support for self-describing formats
- Create commonly used plots
- Perform common spatial data manipulation
- Perform common calculations

## File Read and Write

### Wind climates
WindKit can read many common wind climate and map formats into common scientific python data structures, provided by the xarray and geopandas projects. WindKit makes use of xarray’s self-documenting data structure to provide common metadata to all data structures, and by allowing output and input in the NetCDF and Zarr formats, the metadata can be preserved on disk as well.

### Maps

Maps in WindKit can be either vector maps or raster maps. Vector maps are the traditional maps used in WAsP and other wind resource assessment tools, while raster maps are often obtained through satellite data. Both types of maps can be used to represent either elevation or land-cover classes. A land-cover class map should be combined with a land-cover table, to provide a mapping between the class and various aerodynamic properties. Currently there is support for displacement height and roughness lengths.

### WAsP Workspace

In addition to reading files directly from disk, WindKit can read WAsP Workspace files and to extract various data structures from that format. However, it only supports the most recent versions of the Workspace format, so for older Workspaces, you will need to import them into WAsP 12 first and then save the workspace again. Additionally, WindKit cannot yet work with WAsP 12.7 files that include landcover maps.

## Plotting

WindKit provides two types of plotting functionality, the main plotting functionality is statistical plots using plotly, which allows for interactive plots via Javascript. These plots work both in web pages and Jupyter Notebooks, andNotebooks and can be saved in many common image formats. Additionally a convenience script for plotting maps is provided, which allows you to create plots with overlays to mark areas of interest.

## Spatial Processing

In WindKit the spatial dimension is treated as a first-class object, and a lot of functionality is based around this. All objects must have a defined coordinate reference system, this allows data from different projections to be utilized together. Any wind climate object in WindKit can be represented with three different spatial structures: "point", "stacked point", and "cuboid". This provides a lot of flexibility to handle different types of wind resource data, e.g., a LIDAR plane or resource grid can be represented as a cuboid object, while a collection of masts with the same heights can be represented as a stacked point object. All objects can be converted to point representations allowing for common processing. All spatial objects can be masked, clipped, and reprojected to ensure the right region is used for any analysis.

## Common processing

WindKit can perform many common functions that are part of wind resource assessment workflow. These include: converting between vector and speed/direction representations of the wind, fitting Weibull distributions; calculating important statistics from wind climates.

## Documentation

You can find the full documentation for WindKit at https://docs-wasp.ramtt.xyz/windkit. There is also a [WAsP Python tools](https://www.wasptechnical.dk/forum/forum/19-wasp-python-tools/) forum, where you can ask questions or help other users.
