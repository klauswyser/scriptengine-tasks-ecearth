**********************
Atmosphere Diagnostics
**********************

These processing tasks assume that the provided input files are GRIB output files from OpenIFS. Further assumptions:

- regularly-spaced in time
- data in grid-point space on a reduced Gaussian grid
- 2D variables only

.. highlight:: yaml

OifsGlobalMeanYearMeanTimeseries
================================

| Diagnostic Type: Time Series
| Mapped to: ``ece.mon.oifs_global_mean_year_mean_timeseries``

This processing task computes the global and temporal average of a 2D atmospheric quantity, resulting in a time series diagnostic.

To compute an annual mean, the leg has to be one year long.
If it is, e.g., six months long, the task will compute the six month global mean of the input variable.

**Required arguments**

* ``src``: A list of strings containing paths to the desired OpenIFS output files. This list can be manually entered or (often better) created by the ``find`` task. The task removes the initialization file from this list.
* ``grib_code``: The grib code as it is stored in the output file. Refer to the `ECMWF parameter database`_ for the meaning of the parameters.
* ``dst``: A string ending in ``.nc``. This is where the diagnostic will be saved.

::

    - ece.mon.oifs_global_mean_year_mean_timeseries:
        src: "{{gg_files}}"
        grib_code: 167
        dst: "{{mondir}}/2t_oifs_global_mean_year_mean_timeseries.nc"


OifsAllMeanMap
==============

| Diagnostic Type: Map
| Map Type: global atmosphere
| Mapped to: ``ece.mon.oifs_all_mean_map``

This task takes the "simulation average climatology" (i.e., a multi-year mean) of a global 2D atmospheric variable and saves it as a map diagnostic on disk.

**Required arguments**

* ``src``: A list of strings containing paths to the desired OpenIFS output files. This list can be manually entered or (often better) created by the ``find`` task. The task removes the initialization file from this list.
* ``grib_code``: The grib code as it is stored in the output file. Refer to the `ECMWF parameter database`_ for the meaning of the parameters.
* ``dst``: A string ending in ``.nc``. This is where the diagnostic will be saved.

::

    - ece.mon.oifs_all_mean_map:
        src: "{{gg_files}}"
        grib_code: 167
        dst: "{{mondir}}/2t_oifs_all_mean_map.nc"

OifsYearMeanTemporalmap
=======================

| Diagnostic Type: Temporal Map
| Map Type: global atmosphere
| Mapped to: ``ece.mon.oifs_year_mean_temporalmap``

This task takes the leg mean of a global 2D ocean variable and saves it as a temporal map diagnostic on disk.
It assumes the leg is one year long, which is why it is called "YearMeanTemporalMap".

**Required arguments**

* ``src``: A list of strings containing paths to the desired OpenIFS output files. This list can be manually entered or (often better) created by the ``find`` task. The task removes the initialization file from this list.
* ``grib_code``: The grib code as it is stored in the output file. Refer to the `ECMWF parameter database`_ for the meaning of the parameters.
* ``dst``: A string ending in ``.nc``. This is where the diagnostic will be saved.

::

    - ece.mon.oifs_year_mean_temporalmap:
        src: "{{gg_files}}"
        grib_code: 167
        dst: "{{mondir}}/2t_oifs_year_mean_temporalmap.nc"

.. _ECMWF parameter database: https://apps.ecmwf.int/codes/grib/param-db?&filter=grib1&table=128