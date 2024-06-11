.. _wind_turbines:

Wind Turbines
=============

Wind Turbine Generator
^^^^^^^^^^^^^^^^^^^^^^

Wind Turbine Generators (WTGs)


A `.wtg` file can be read using the :py:func:`windkit.read_wtg` function.

.. code-block:: python

    import windkit as wk
    wtg = wk.read_wtg("Bonus_1_MW.wtg")
    print(wtg)

.. code-block:: bash

    <xarray.Dataset>
    Dimensions:                        (mode: 1, wind_speed: 22)
    Coordinates:
    * wind_speed                     (wind_speed) float64 4.0 5.0 ... 24.0 25.0
    * mode                           (mode) int64 0
    Data variables:
        power_output                   (mode, wind_speed) float64 2.41e+04 ... 1e+06
        thrust_coefficient             (mode, wind_speed) float64 0.915 ... 0.161
        air_density                    (mode) float64 1.225
        stationary_thrust_coefficient  (mode) float64 0.161
        wind_speed_cutin               (mode) float64 4.0
        wind_speed_cutout              (mode) float64 25.0
        rated_power                    (mode) float64 1e+06
        name                           <U10 'Bonus 1 MW'
        rotor_diameter                 float64 54.2
        hub_height                     float64 50.0
        regulation_type                int64 2
    Attributes:
        Conventions:      CF-1.8
        Package name:     windkit
        Package version:  0.6.4.dev32+g349fa3c
        Creation date:    2023-10-31T09:04:58
        author:           Bjarke Tobias Olsen
        author_email:     btol@dtu.dk
        institution:      DTU Wind Energy


The **wtg** :py:class:`xarray.Dataset` format contains a number of variables and attributes.
The most important variables are:

    - `power_output`: The power output of the wind turbine generator in W.
    - `thrust_coefficient`: The thrust coefficient of the wind turbine generator.
    - `air_density`: The air density in kg/m3.
    - `stationary_thrust_coefficient`: The stationary thrust coefficient of the wind turbine generator.
    - `wind_speed_cutin`: The cut-in wind speed of the wind turbine generator in m/s.
    - `wind_speed_cutout`: The cut-out wind speed of the wind turbine generator in m/s.
    - `rated_power`: The rated power of the wind turbine generator in W.

The power output and the thrust coefficient are functions of the wind speed and the mode of the WTG.
The mode is used to distinguish between different operating conditions of the WTG.
Each mode is associated with a set of operating conditions, such as varying air density,
cut-in and cut-out wind speeds, and rated power etc. In the WTG object above there is only one mode available.

To manually create a wind turbine generator, a :py:class:`xarray.Dataset` following format desribed above can be created:

.. code-block:: python

    import numpy as np
    import xarray as xr

    # Create a wind turbine generator
    power_output = np.random.rand(1, 22) * 1e6
    thrust_coefficient = np.random.rand(1, 22)
    air_density = np.array([1.225])
    stationary_thrust_coefficient = np.array([0.161])
    wind_speed_cutin = np.array([4.0])
    wind_speed_cutout = np.array([25.0])
    rated_power = np.array([1e6])
    name = "Bonus 1 MW"
    rotor_diameter = 54.2
    hub_height = 50.0
    regulation_type = 2  # 1=stall, 2=pitch

    wind_speed = np.linspace(4.0, 25.0, 22)
    mode = np.array([0])

    wtg = xr.Dataset(
        data_vars=dict(
            power_output=(["mode", "wind_speed"], power_output),
            thrust_coefficient=(["mode", "wind_speed"], thrust_coefficient),
            air_density=(["mode"], air_density),
            stationary_thrust_coefficient=(["mode"], stationary_thrust_coefficient),
            wind_speed_cutin=(["mode"], wind_speed_cutin),
            wind_speed_cutout=(["mode"], wind_speed_cutout),
            rated_power=(["mode"], rated_power),
            name=name,
            rotor_diameter=rotor_diameter,
            hub_height=hub_height,
            regulation_type=regulation_type,
        ),
        coords=dict(
            wind_speed=wind_speed,
            mode=mode,
        ),
    )

The resulting WTG is very similar to the one read from file above (apart from the randomly generated data).

Wind Turbines object
^^^^^^^^^^^^^^^^^^^^

Groups of wind turbines can be created in `windkit <windkit>` by creating a
a :py:class:`xr.Dataset` object containing information about the positions, hub height,
turbine id's, turbine group id's, and wtg keys for each turbine. The wtg keys are used
to map from each turbine to a WTG :py:class:`xr.Dataset` via a dictionary object. The turbines :py:class:`xr.Dataset`
can be created via the functions :py:func:`windkit.create_wind_turbines_from_arrays`,
:py:func:`windkit.create_wind_turbines_from_dataframe`, or
:py:func:`windkit.wind_turbines_to_geodataframe`. Here is a simple example of how to create the
turbines :py:class:`xr.Dataset`:

.. code-block:: python

    import windkit as wk

    turbines = wk.create_wind_turbines_from_arrays(
        x=[0, 0, 0, 0, 0],
        y=[0, 1, 2, 3, 4],
        height=[50, 50, 50, 50, 50],
        crs="epsg:32632",
        turbine_ids=[1, 2, 3, 4, 5],
        group_ids=[0, 0, 1, 1, 1],
        wtg_keys=["wtg1", "wtg1", "wtg2", "wtg2", "wtg2"],
    )

In this example, we have defined five turbines in two groups, with each group using a different WTG.
The wtg keys ("wtg1" and "wtg2"), should exist in a dictionary that maps to
the WTG :py:class:`xr.Dataset`'s: ``{"wtg1": wtg1, "wtg2": wtg2}``.
