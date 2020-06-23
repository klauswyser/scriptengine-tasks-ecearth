"""Processing Task that creates a 2D dynamic map of sea ice concentration."""

import os

import numpy as np
import iris
import iris_grib
import cftime

from scriptengine.tasks.base import Task
from scriptengine.jinja import render as j2render
import helpers.file_handling as helpers

class SiconcDynamicMap(Task):
    """SiconcDynamicMap Processing Task"""
    def __init__(self, parameters):
        required = [
            "src",
            "dst",
            "hemisphere",
        ]
        super().__init__(__name__, parameters, required_parameters=required)
        self.comment = (f"Dynamic Map of Sea Ice Concentration on {self.hemisphere.capitalize()}ern Hemisphere.")
        self.type = "dynamic map"
        self.map_type = "polar ice sheet"
        self.long_name = "Sea Ice Concentration"

    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        hemisphere = self.getarg('hemisphere', context)
        self.log_info(f"Create dynamic siconc map for {hemisphere}ern hemisphere at {dst}.")
        self.log_debug(f"Source file(s): {src}")

        if not dst.endswith(".nc"):
            self.log_warning((
                f"{dst} does not end in valid netCDF file extension. "
                f"Diagnostic will not be treated, returning now."
            ))
            return

        month_cube = iris.load_cube(src, 'siconc')
        month_cube.attributes.pop('uuid')
        month_cube.attributes.pop('timeStamp')
        latitudes = np.broadcast_to(month_cube.coord('latitude').points, month_cube.shape)
        if hemisphere == "north":
            month_cube.data = np.ma.masked_where(latitudes < 0, month_cube.data)
            month_cube.long_name = self.long_name + " Northern Hemisphere"
            month_cube.var_name = "siconcn"
        elif hemisphere == "south":
            month_cube.data = np.ma.masked_where(latitudes > 0, month_cube.data)
            month_cube.long_name = self.long_name + " Southern Hemisphere"
            month_cube.var_name = "siconcs"
        month_cube.data = np.ma.masked_equal(month_cube.data, 0)


        # Remove auxiliary time coordinate
        month_cube.remove_coord(month_cube.coord('time', dim_coords=False))
        month_cube = helpers.set_metadata(
            month_cube,
            title=f'{month_cube.long_name} (Simulation Average)',
            comment=self.comment,
            diagnostic_type=self.type,
            map_type=self.map_type,
            presentation_min=0.0,
            presentation_max=1.0,
        )

        try:
            saved_diagnostic = iris.load_cube(dst)
        except OSError: # file does not exist yet
            iris.save(month_cube, dst)
        else:
            current_bounds = saved_diagnostic.coord('time').bounds
            new_bounds = month_cube.coord('time').bounds
            if current_bounds[-1][-1] > new_bounds[0][0]:
                self.log_warning("Inserting would lead to non-monotonic time axis. Aborting.")
            else:
                cube_list = iris.cube.CubeList([saved_diagnostic, month_cube])
                single_cube = cube_list.concatenate_cube()
                iris.save(single_cube, f"{dst}-copy.nc")
                os.remove(dst)
                os.rename(f"{dst}-copy.nc", dst)
