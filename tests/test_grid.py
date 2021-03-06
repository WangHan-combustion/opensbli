#!/usr/bin/env python

#    OpenSBLI: An automatic code generator for solving differential equations.
#    Copyright (C) 2016 Satya P. Jammy, Christian T. Jacobs, Neil D. Sandham

#    This file is part of OpenSBLI.

#    OpenSBLI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    OpenSBLI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with OpenSBLI.  If not, see <http://www.gnu.org/licenses/>.

import os
import pytest

from sympy import Idx, IndexedBase, Symbol, symbols

# OpenSBLI classes and functions
from opensbli.grid import Grid, GridVariable
from opensbli.equations import EinsteinTerm

@pytest.fixture
def grid():
    return Grid(ndim=3)

@pytest.fixture
def grid_with_data():
    return Grid(ndim=3, grid_data={"number_of_points":[10, 5, 2], "delta":[0.5, 0.25, 1.0]})

@pytest.fixture
def grid_variable():
    return GridVariable('test')


def test_grid(grid, grid_with_data):
    """ Ensure that a numerical grid of solution points is set up correctly. """

    assert len(grid.shape) == 3
    assert grid.shape == tuple(symbols('nx0:3', integer=True)) # nx x ny x nz grid shape
    assert grid.indices == tuple(symbols('i0:3', integer=True)) # Grid index for each dimension
    assert len(grid.deltas) == 3

    assert grid_with_data.total_points == 10*5*2 # Grid index for each dimension
    #assert grid_with_data.deltas == [0.5, 0.25, 1.0]

    return


def test_work_array(grid):
    """ Ensure that a work array is set up correctly on the Grid. """
    xi = EinsteinTerm('x_i')
    indices = xi.get_array(xi.get_indexed(3)).tolist()
    assert grid.work_array("test") == IndexedBase("test")[indices]
    return


def test_grid_variable(grid, grid_variable):
    """ Ensure that a variable on a grid returns an object of type GridVariable. """
    assert grid.grid_variable('test') == grid_variable
    return


def test_indexed_by_grid(grid):
    """ Ensure that an Indexed object gets correctly indexed by the Grid indices. """

    idx = Idx(Symbol("i", integer=True))
    base = IndexedBase("test")
    i = base[idx]
    
    assert grid.indexed_by_grid(i) == base[grid.indices]

    return 


if __name__ == '__main__':
    pytest.main(os.path.abspath(__file__))
