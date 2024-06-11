# (c) 2022 DTU Wind Energy
"""
Generalized wind climate module

This module contains the various functions for working with generalized wind climates.

Currently this only supports creating gwc datasets from .lib files or from
NetCDF files. In the future we will also support the ability to read in .gwc
files.
"""

import re
import warnings
from pathlib import Path

import numpy as np
import xarray as xr
from lxml import etree

from ._errors import WindClimateValidationError
from ._rvea_xml import (
    _parse_rvea_anemometer_site_details,
    _parse_rvea_generalised_mean_wind_climate,
)
from ._validate import create_validator
from .metadata import (
    _WEIB_ATTRS,
    ALL_VARS_META,
    create_coords,
    update_history,
    update_var_attrs,
)
from .sector import create_sector_coords
from .spatial import create_dataset, crs_are_equal, reproject, to_point

_GEN_COORDS_META = {
    "gen_height": ALL_VARS_META["gen_height"],
    "gen_roughness": ALL_VARS_META["gen_roughness"],
}

DATA_VAR_DICT_GWC = {
    "A": ["sector", "gen_height", "gen_roughness"],
    "wdfreq": ["sector", "gen_height", "gen_roughness"],
    "k": ["sector", "gen_height", "gen_roughness"],
}

REQ_DIMS_GWC = ["sector", "gen_height", "gen_roughness"]

REQ_COORDS_GWC = [
    "south_north",
    "west_east",
    "gen_height",
    "gen_roughness",
    "sector_ceil",
    "sector_floor",
    "sector",
    "crs",
]


def _validate_height_and_roughness(genwc):
    """Helper function to validate generalized_height and generalized_roughness"""
    response_list = []

    if "gen_height" in genwc.dims:
        if genwc.sizes["gen_height"] < 2:
            response_list.append("gen_height needs at least 2 entries")

    if "gen_roughness" in genwc.dims:
        if genwc.sizes["gen_roughness"] < 2:
            response_list.append("gen_roughness needs at least 2 entries")
        if genwc["gen_roughness"].min() != 0.0:
            response_list.append("The first entry of gen_roughness must be 0.0")

    return response_list


def _validate_greater_than_zero(genwc):
    """Helper function to validate generalized heights and roughness are positive"""
    response_list = []

    if "gen_roughness" in genwc.dims and any(
        xr.where(genwc.gen_roughness.values < 0.0, True, False)
    ):
        response_list.append("'gen_roughness' has negative values")

    if "gen_height" in genwc.dims and any(
        xr.where(genwc.gen_height.values < 0.0, True, False)
    ):
        response_list.append("'gen_height' has negative values")

    return response_list


gwc_validate, gwc_validate_wrapper = create_validator(
    DATA_VAR_DICT_GWC,
    REQ_DIMS_GWC,
    REQ_COORDS_GWC,
    checks_iterator=[_validate_height_and_roughness, _validate_greater_than_zero],
)


def _is_gwc(wco):
    """Check if this is a generalized wind climate

    Returns true if gwc and false if not

    Parameters
    ----------
    wco: xarray.Dataset
        Wind Climate Object

    Returns
    -------
    Bool
        Returns true if gwc and false if not
    """
    try:
        gwc_validate(wco)
        return True
    except WindClimateValidationError:
        return False


@gwc_validate_wrapper
def lib_string(gwc, /, gen_height=None):
    """Generates string representation of gwc dataset.

    Parameters
    ----------
    gwc: xarray.Dataset
        Dataset containing A, k, and wdfreq.
        Dimensions should be ('gen_height', 'gen_roughness', 'sector')
    gen_height: float
        Value of gen_height to use for saving to libfile. Since libfiles only allow a
        single set of wdfreq values, when your data has varying wdfreq values, you need
        to set this value. It is selected using the .sel selector from xarray.

    Returns
    -------
    str
        String representation of gwc dataset.

    """

    def _fmt_floats(dat, prec=3, extra=False):
        """
        Format a list of floats into a common format

        Parameters
        ----------
        dat: list
            List of floats to be formatted
        prec: int
            Precision of output string
            Default set to 3
        extra: bool
            Extra space between characters
            Default set to False (i.e., no extra space)

        Returns
        -------
        str
            String containing space separated floats
        """

        sep = " " if extra else ""
        fmt = "{0:9.%df}" % prec
        return sep.join([fmt.format(i) for i in dat])

    def _to_string(node):
        """Generates string representation of gwc dataset

        Parameters
        ----------
        node : xarray.Dataset
            Dataset containing A, k, and wdfreq.
            Dimesions should be ('height', 'roughness', 'sector')

        Returns
        -------
        str
            String representation of xarray dataset
        """
        if "height" not in node.coords:
            node = node.expand_dims({"height": [0.0]}).isel(height=0)
        nrough = node.sizes["gen_roughness"]
        nhgt = node.sizes["gen_height"]
        nsec = node.sizes["sector"]
        node = reproject(node, 4326).squeeze()
        # Extract numpy arrays to speed up the processing
        A = node.A.values
        k = node.k.values
        wdfreq = node.wdfreq.values
        string = ""
        newline = "\n"

        height = node.height

        # Write the header
        header_without_coord = re.sub(
            "<coordinates>(.*)</coordinates>", "", node.attrs["wasp_header"]
        )
        string += (
            header_without_coord
            + f"<coordinates>{float(node.west_east)},{float(node.south_north)},{float(height)}</coordinates>{newline}"
        )

        # Write the dimensions nz0,nz,nsec
        string += " ".join([str(i) for i in (nrough, nhgt, nsec)]) + newline

        # Write the roughness classes
        string += _fmt_floats(node.gen_roughness.values, 3, True) + newline

        # Write the heights
        string += _fmt_floats(node.gen_height.values, 1, True) + newline

        # Write the data arrays
        for i in range(nrough):
            # sectorwise frequency in percent
            string += _fmt_floats(100.0 * wdfreq[i, ...], 2) + newline
            for j in range(nhgt):
                # Sectorwise A's
                string += _fmt_floats(A[j, i, ...], 2) + newline
                # Sectorwise k's
                string += _fmt_floats(k[j, i, ...]) + newline

        return string

    dims_order = ["gen_height", "gen_roughness", "sector"]

    gwc = gwc.copy()
    gwc = gwc.transpose(*dims_order, ...)

    # if wdfreq varues with height we require users to choose the height
    if _wdfreq_constant_with_gen_height(gwc):
        gwc["wdfreq"] = gwc["wdfreq"].isel(gen_height=0)
    else:
        if gen_height is None:
            raise ValueError(
                "Lib files do not support different 'wdfreq' values for different heights. Please specify the 'gen_height' for the 'wdfreq' values that you wish to use for all levels."
            )
        else:
            gwc["wdfreq"] = gwc["wdfreq"].sel(gen_height=gen_height, method="nearest")

    if gwc.squeeze().A.ndim == 3:
        return _to_string(gwc.squeeze())

    dims_extra = [d for d in gwc.A.dims if d not in dims_order]
    stacked = gwc.stack(point=dims_extra).transpose(*dims_order, "point")
    # Get numbers of sectors, roughness classes and
    strings = []
    for ipt in range(stacked.sizes["point"]):
        # Need the slice to keep the point dimension as multi-index
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        strings.append(_to_string(node))

    return strings


def _wdfreq_constant_with_gen_height(gwc):
    """Check if 'wdfreq' is constant with 'gen_height' dimension.

    Parameters
    ----------
    gwc : xarray.Dataset
        Generalized wind climate dataset.

    Returns
    -------
    bool
        True if 'wdfreq' is constant with 'gen_height' dimension across whole dataset.
    """
    return np.isclose(gwc["wdfreq"].diff(dim="gen_height").max(), 0.0).all()


@gwc_validate_wrapper
def to_libfile(gwc, /, path=None, gen_height=None):
    """Creates lib-style ascii file from gwc dataset

    Parameters
    ----------
    gwc : xarray.Dataset
        Generalized wind climate dataset.
    path : str
        dir or file path for storing lib file
        Default value set to the current working directory.
    gen_height: float
        Value of gen_height to use for saving to libfile. Since libfiles only allow a
        single set of wdfreq values, when your data has varying wdfreq values, you need
        to set this value. It is selected using the .sel selector from xarray.

    """

    gwc = gwc.copy()

    def _write(node, fpath):
        # Set newline explicitly in string not in open.
        with open(fpath, "w", newline="\r\n") as fobj:
            fobj.write(lib_string(node, gen_height=gen_height))

    def _fmt_single_point_filename(ds):
        single_point_coords = ["height", "south_north", "west_east"]
        vals = []
        for coord in single_point_coords:
            vals.append(ds[coord].values.flatten()[0])
        filename = f"gwc_height{vals[0]}_south_north{vals[1]}_west_east{vals[2]}.lib"
        return filename

    if path is None:
        path = Path.cwd()
    path = Path(path)

    if path.suffix == "":  # it is a directory
        path.mkdir(parents=True, exist_ok=True)

    if gwc.squeeze().A.ndim == 3:
        if path.is_dir():
            # fpath = path / "gwc.lib"
            fpath = path / _fmt_single_point_filename(gwc)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            fpath = path
        _write(gwc.squeeze(), fpath)
        return

    # If dataset has extra dimensions (of size > 1):
    # Stack extra dimensions, loop over them, and write to tab files
    # Using file_name that contains coordinate information.
    dims_extra = [
        d for d in gwc.A.dims if d not in ["gen_height", "gen_roughness", "sector"]
    ]
    stacked = gwc.stack(point=dims_extra)

    # Create file_name format string
    if Path(path).is_dir():
        file_name_fmt = (
            "_".join(["gwc"] + [f"{d}" + "{" + f"{d}" + "}" for d in dims_extra])
            + ".lib"
        )
    else:
        raise ValueError(
            "'path' argument is a filename, but the dataset has more than one point."
            " Try giving a directory as an argument."
        )

    # Loop and write to tab files
    for ipt in range(stacked.sizes["point"]):
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        kwds = {d: node[d].values for d in dims_extra}
        fpath = path / file_name_fmt.format(**kwds)
        _write(node, fpath)

    return


def read_gwc(
    file_or_obj, crs=None, west_east=None, south_north=None, height=None, header=None
):
    """Create gwc xarray.Dataset from file.

    Parameters
    ----------
    file : str or Path
        Path to a file that can be opened a gwc. This includes .lib, .gwc, and
        .nc files that were created as gwc files. The script will use the file
        extension to determine the file type and then parse it into a gwc object.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum). for .lib and .gwc.
    west_east : float or None, optional
        West-East coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    south_north : float or None, optional
        South-North coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    height : float or None, optional
        Height coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    header : str or None, optional
        Header string to use for .lib and .gwc files, by default None, which will
        attempt to read from the file.

    Returns
    -------
    xarray.Dataset
        Generalized wind climate dataset.

    Raises
    ------
    ValueError
        If the file extension is not recognized.
    ValueError
        If the requested crs does not match the dataset crs.

    """
    file_or_obj = Path(file_or_obj)
    ext = file_or_obj.suffix

    if ext == ".lib":
        ds = _read_lib_file(
            file_or_obj,
            crs=crs,
            west_east=west_east,
            south_north=south_north,
            height=height,
            header=header,
        )
    elif ext in [".gwc"]:
        ds = _read_gwc_file(
            file_or_obj,
            crs=crs,
            west_east=west_east,
            south_north=south_north,
            height=height,
            header=header,
        )
    elif ext in [".nc"]:
        ds = xr.open_dataset(file_or_obj)
        if crs is not None and not crs_are_equal(ds, crs):
            raise ValueError(f"Requested crs does not match dataset crs")
    else:
        raise ValueError(
            f"Unable to detect type of gwc file {file_or_obj} with extension {ext}."
        )
    gwc_validate(ds)  # Validate for all file types
    ds = update_var_attrs(ds, _WEIB_ATTRS)
    return update_history(ds)


def _read_lib_file(
    lib_file, crs=None, west_east=None, south_north=None, height=None, header=None
):
    r"""
    Create GenWindClimate object from WAsP .lib file

    Parameters
    ----------
    lib_file : str, pathlib.Path
        Path to lib file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum)
    west_east : float or None, optional
        West-East coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    south_north : float or None, optional
        South-North coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    height : float or None, optional
        Height coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    header : str or None, optional
        Header string to use for .lib and .gwc files, by default None, which will
        attempt to read from the file.

    Returns
    -------
    xr.DataSet
        xarray DataSet that is formatted to match the gwc description

    Raises
    ------
    ValueError
        If coordinates are not present in the file and are not provided as
        arguments.

    Notes
    -----
    Automatically adds lat, lon coords if present inside
    <coordinates>lon,lat,height<\coordinates> brackets
    """

    def _read_float_(f):
        """Reads a line of space separated data and splits it into floats

        Parameters
        ----------
        f : file
            Object with method readline

        Returns
        -------
        list
            List of floats
        """
        return [np.float32(i) for i in f.readline().strip().split()]

    def _read_int_(f):
        """Reads a line of space-separated data and splits it into integers

        Parameters
        ----------
        f : file
            Object with method readline

        Returns
        -------
        list
            List of integers
        """
        return [np.int32(i) for i in f.readline().strip().split()]

    # Open libfile
    with open(lib_file) as f:
        # Read header information one line at a time
        desc = f.readline().strip()  # File Description
        nrough, nhgt, nsec = _read_int_(f)  # dimensions
        gen_roughness = _read_float_(f)  # Roughness classes
        gen_height = _read_float_(f)  # heights

        # Initialize arrays
        wdfreq = np.zeros([nsec, nrough], dtype="f4", order="F")
        k = np.zeros([nsec, nhgt, nrough], dtype="f4", order="F")
        A = np.zeros([nsec, nhgt, nrough], dtype="f4")

        ##################################################################
        # The remainder of the file is made up of rows with nsec columns.
        # For each height there is first a frequency row, then pairs of
        # A & k rows for each height.
        ##################################################################
        # Loop over roughness classes to read frequency line
        for i, dummy in enumerate(gen_roughness):
            wdfreq[:, i] = _read_float_(f)
            # Loop over heights to read in all A & k values
            for j, dummy in enumerate(gen_height):
                A[:, j, i] = _read_float_(f)
                k[:, j, i] = _read_float_(f)

    if crs is None:
        crs = "EPSG:4326"

    # Find the coordinates if they aren't provided
    if all(c is None for c in [west_east, south_north, height]):
        # Find the coordinates
        latlons = re.search("<coordinates>(.*)</coordinates>", desc)
        if latlons:
            west_east, south_north, height = map(
                np.float32, latlons.group(1).split(",")
            )
        else:
            raise ValueError(
                f"Coordinates not found in {lib_file}, "
                + "please set 'west_east', 'south_north', and 'height' explicitly. "
                + "These values should ge in the projection given by the 'crs' argument,"
                + " which defaults to the WGS84 projection."
            )

    if header is None:
        if len(desc) > 0:
            header = desc
        else:
            header = ""

    # Add height to wdfreq
    wdfreq = np.tile(wdfreq[:, np.newaxis, :], (1, nhgt, 1))

    return _weibull_to_dataset(
        wdfreq,
        A,
        k,
        gen_roughness,
        gen_height,
        south_north,
        west_east,
        height,
        crs,
        wasp_header=header,
    )


def _weibull_to_dataset(
    wdfreq,
    A,
    k,
    gen_roughness,
    gen_height,
    south_north,
    west_east,
    height,
    crs,
    **kwargs,
):
    """
    Converts parsed xml gwc object to WindKit gwc xarray dataset

    Parameters
    ----------
    wdfreq : 1-D sequence of floats
        Wind direction frequencies. Dimensions=[sector, gen_height, gen_roughnness]
    A : numpy
        Weibull A parameters.  Dimensions=[sector, gen_height, gen_roughnness]
    k : numpy
        Weibull k parameters.  Dimensions=[sector, gen_height, gen_roughnness]
    gen_roughness : numpy
        Array of generalized roughnesses
    gen_height : numpy
        Array of generalized heights
    west_east : float or None, optional
        West-East coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    south_north : float or None, optional
        South-North coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    height : float or None, optional
        Height coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum)

    kwargs : dict, optional
        Other key-word arguments are added as attributes to the dataset.

    Returns
    -------
    xarray.Dataset
        WindKit GWC dataset
    """

    nsec, _, _ = wdfreq.shape

    na = np.newaxis

    # Create dataset
    ds = create_dataset(west_east, south_north, height, crs).drop_vars("output")
    ds.attrs = kwargs

    # Add variables
    dims = ("sector", "gen_height", "gen_roughness", "point")
    ds["A"] = (dims, A[..., na])
    ds["k"] = (dims, k[..., na])
    ds["wdfreq"] = (dims, wdfreq[..., na])

    # Add coordinates
    ds = ds.assign_coords(
        {
            **create_coords(gen_height, "gen_height", _GEN_COORDS_META).coords,
            **create_coords(gen_roughness, "gen_roughness", _GEN_COORDS_META).coords,
            **create_sector_coords(nsec).coords,
        }
    )

    ds["wdfreq"] = ds["wdfreq"] / ds["wdfreq"].sum(dim="sector")

    return ds.transpose("gen_height", "gen_roughness", "sector", "point")


def _read_gwc_file(
    gwc_file,
    crs=None,
    west_east=None,
    south_north=None,
    height=None,
    header=None,
):
    """Read Generalized Wind Climate from XML-based .gwc file.

    Parameters
    ----------
    gwc_file : str, pathlib.Path
        input file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum)
    west_east : float or None, optional
        West-East coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    south_north : float or None, optional
        South-North coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    height : float or None, optional
        Height coordinate of the GWC grid, by default None, which will attempt to
        read from the file.
    header : str or None, optional
        Header string to use for .lib and .gwc files, by default None, which will
        attempt to read from the file.

    Returns
    -------
    xarray.Dataset
        WindKit GWC dataset

    Raises
    ------
    ValueError
        If no RveaGeneralisedMeanWindClimate is found in the file.
    ValueError
        If coordinates are not found in the file and are not provided explicitly.

    Warns
    -----
    UserWarning
        If 'height' is not found in the file and are not provided explicitly.
        It will be set to 0.0

    """

    if crs is None:
        crs = "EPSG:4326"

    tree = etree.parse(str(gwc_file))
    root = tree.getroot()

    descendants = list(e.tag for e in root.getiterator())

    if root.tag == "RveaGeneralisedMeanWindClimate":
        gwc_tree = root
    elif "RveaGeneralisedMeanWindClimate" in descendants:
        gwc_tree = tree.find(".//RveaGeneralisedMeanWindClimate")
    else:
        raise ValueError(f"No RveaGeneralisedMeanWindClimate found in '{gwc_file}'")

    gwc_data = _parse_rvea_generalised_mean_wind_climate(gwc_tree)

    if "RveaAnemometerSiteDetails" in descendants:
        site_data = _parse_rvea_anemometer_site_details(
            tree.find(".//RveaAnemometerSiteDetails")
        )
    else:
        site_data = {}

    if west_east is None:
        west_east = gwc_data.get("longitude", site_data.get("longitude", None))

    if south_north is None:
        south_north = gwc_data.get("latitude", site_data.get("latitude", None))

    if height is None:
        height = gwc_data.get("height", site_data.get("height", None))

    if header == None:
        header = gwc_data.get("header", site_data.get("header", ""))

    if west_east is None or south_north is None:
        raise ValueError(
            "'west_east' or 'south_north' coordinate not found in file or provided as argument. "
            + "Please set 'west_east' and 'south_north' explicitly."
        )

    if height is None:
        height = 0.0
        warnings.warn(
            "No height found in file or provided as argument, using 0 m. Set 'height' explicitly to avoid this warning.",
        )

    return _weibull_to_dataset(
        wdfreq=gwc_data["wdfreq"],
        A=gwc_data["A"],
        k=gwc_data["k"],
        gen_roughness=gwc_data["gen_roughness"],
        gen_height=gwc_data["gen_height"],
        west_east=west_east,
        south_north=south_north,
        height=height,
        crs=crs,
        wasp_header=header,
    )


@gwc_validate_wrapper
def reproject_gwc(gwc, /, to_crs):
    """Reprojects Generalized wind climate dataset.

    Parameters
    ----------
    gwc: xarray.Dataset
        Valid GWC dataset.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`

    Returns
    -------
    xarray.Dataset
        Point based generalized wind climate dataset in new projection.
    """
    if not crs_are_equal(gwc, to_crs):
        return reproject(gwc, to_crs)

    # Return point based dataset even if not reprojected
    ds = to_point(gwc)
    return update_history(ds)
