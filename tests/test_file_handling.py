"""Tests for helpers/file_handling.py"""

import os

import pytest
import numpy as np
import iris

import helpers.file_handling as file_handling

def test_get_month_from_src():
    path_list = [
        "dummy_01.nc",
        "dummy_02.nc",
        ]
    assert file_handling.get_month_from_src('02', path_list) == "dummy_02.nc"
    pytest.raises(
        FileNotFoundError,
        file_handling.get_month_from_src,
        '03',
        path_list,
        )

def test_change_directory(tmpdir):
    cwd = os.getcwd()
    nwd = tmpdir.mkdir('temp')
    with file_handling.ChangeDirectory(nwd):
        assert os.getcwd() == nwd
    assert os.getcwd() == cwd

def test_compute_spatial_weights(tmpdir, monkeypatch):
    e1t_cube = iris.cube.Cube([1], var_name='e1t')
    e2t_cube = iris.cube.Cube([2], var_name='e2t')
    cube_list = iris.cube.CubeList([e1t_cube, e2t_cube])
    domain_path = str(tmpdir + "/temp.nc")
    iris.save(cube_list, domain_path)
    assert file_handling.compute_spatial_weights(domain_path, (3,1,1)).all() == np.array([[[2,]],[[2,]],[[2,]]]).all()

def test_load_input_cube():
    assert 0 == 0