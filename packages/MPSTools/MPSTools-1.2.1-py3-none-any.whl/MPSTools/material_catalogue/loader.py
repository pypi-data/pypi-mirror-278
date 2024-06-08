#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import numpy
import pandas
import yaml
from pathlib import Path
from typing import Iterable


def get_material_files_dir(subdir: str) -> Path:
    """
    Returns the directory path for material files.

    Parameters:
    - subdir: Subdirectory within the material files directory.

    Returns:
    - A Path object pointing to the specified subdirectory.
    """
    return Path(__file__).parent / 'material_files' / subdir


def list_material_files():
    """
    Prints the list of SellMeier and measurement material files.
    """
    sellmeier_dir = get_material_files_dir('sellmeier')
    measurement_dir = get_material_files_dir('measurements')

    sellmeier_files = [f.stem for f in sellmeier_dir.glob('*.yaml')]
    measurement_files = [f.stem for f in measurement_dir.glob('*.yml')]

    print('SellMeier files:')
    print('\n'.join(f'\t{s}' for s in sellmeier_files))

    print('Measurement files:')
    print('\n'.join(f'\t{m}' for m in measurement_files))


def load_yaml_file(file_path: Path | str) -> dict:
    """
    Loads a YAML file into a dictionary.

    Parameters:
    - file_path: Path to the YAML file.

    Returns:
    - A dictionary containing the YAML file content.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        available = '\n'.join(f.stem for f in file_path.parent.glob('*.yaml'))
        raise FileNotFoundError(f'File: {file_path} not found: \n{available}')
    return yaml.safe_load(file_path.read_text())


def dispersion_formula(parameters: dict, wavelength: float) -> float:
    """
    Calculates the refractive index using the Sellmeier dispersion formula.

    Parameters:
    - parameters: Sellmeier parameters.
    - wavelength: Wavelength in meters.

    Returns:
    - The calculated refractive index.
    """
    wavelength_um = wavelength * 1e6  # Convert wavelength to micrometers
    B = [parameters.get(f'B_{i}') for i in range(1, 4)]
    C = [parameters.get(f'C_{i}')**2 if parameters['C_squared'] else parameters.get(f'C_{i}') for i in range(1, 4)]
    index_squared = 1 + sum(B[i] * wavelength_um**2 / (wavelength_um**2 - C[i]) for i in range(3))
    return numpy.sqrt(index_squared)


def get_index_from_measurements(parameters: dict, wavelength: float | Iterable) -> float | Iterable:
    data_string = parameters['DATA'][0]['data']

    buffer = io.StringIO(data_string)
    data = pandas.read_csv(buffer, sep=' ').to_numpy()
    wavelength_base, n_base, k_base = data.T
    refractive_index_base = n_base + k_base * 1j

    evaluated_refractive_index = numpy.interp(
        wavelength * 1e6,
        wavelength_base,
        refractive_index_base,
        left=None,
        right=None,
        period=None
    )

    return evaluated_refractive_index


def get_material_index(material_name: str, wavelength: float, subdir: str = 'sellmeier') -> float:
    """
    Gets the material refractive index using the dispersion formula or measurement data.

    Parameters:
    - material_name: The material name.
    - wavelength: Wavelength in meters.
    - subdir: Subdirectory name ('sellmeier' or 'measurements').

    Returns:
    - The material refractive index.
    """
    assert subdir in ['sellmeier', 'measurements'], f'Invalid subdir input: {subdir}. Valid has to be either "sellmeier" or "measurements" '

    wavelength = numpy.asarray(wavelength)

    file_path = get_material_files_dir(subdir) / f'{material_name}.yaml'

    parameters = load_yaml_file(file_path)

    if subdir == 'sellmeier':
        return dispersion_formula(parameters=parameters['sellmeier'], wavelength=wavelength)

    else:
        return get_index_from_measurements(parameters=parameters, wavelength=wavelength)


def get_silica_index(wavelength: float, subdir: str = 'sellmeier') -> float:
    return get_material_index(
        material_name='silica',
        wavelength=wavelength,
        subdir=subdir
    )


# -
