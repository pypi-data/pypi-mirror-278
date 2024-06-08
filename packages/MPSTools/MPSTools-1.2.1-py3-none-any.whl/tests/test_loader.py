#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from MPSTools import fiber_catalogue
from MPSTools import material_catalogue

# print(dir(material_catalogue))


@pytest.mark.parametrize("material", material_catalogue.material_list)
def test_material_loader(material: str):
    material_catalogue.loader.get_material_index(material_name=material, wavelength=1550e-9)


@pytest.mark.parametrize("fiber_model", fiber_catalogue.fiber_mode_list)
def test_fiber_loader(fiber_model: str):
    fiber_catalogue.loader.load_fiber_as_dict(fiber_name=fiber_model, wavelength=1550e-9)

# -
