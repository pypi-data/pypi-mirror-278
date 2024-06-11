#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyMieSim.experiment.source as source

import numpy

from DataVisual import units
from PyMieSim.binary.Sets import CppCoreShellSet, CppCylinderSet, CppSphereSet
from PyMieSim.experiment import measure
from PyOptik import Sellmeier, DataMeasurement

from pydantic.dataclasses import dataclass
from pydantic import Field
from typing import List, Union, NoReturn, Any


@dataclass(kw_only=True, slots=True, config=dict(extra='forbid'))
class BaseScatterer():
    """
    Base class for scatterer objects. This class handles the initialization and setup of
    scatterer parameters for use in PyMieSim simulations.

    Attributes:
        medium_index (List): Refractive index of the medium in which the scatterers are placed.
        source (Union[experiment.source.Gaussian, experiment.source.PlaneWave]): Light source configuration for the simulation.
    """
    source: Union[source.Gaussian, source.PlaneWave]
    mapping: dict = Field(init=False, repr=False)
    binding_kwargs: dict = Field(init=False, repr=False)
    binding: object = Field(init=False, repr=False)

    def __post_init__(self) -> NoReturn:
        """
        Initializes the scatterer instance by asserting inputs, formatting them, building binding
        arguments, and Units for visualization. This method is automatically called after the
        class has been initialized.

        Returns:
            NoReturn
        """
        self.build_binding_kwargs()

    def add_material_index_to_mapping(self, name: str = None) -> NoReturn:
        """
        Adds material or refractive index details to a mapping dictionary used for visualization or further processing.
        This method is used to create a mapping of material properties to human-readable and accessible formats for
        UI or data outputs.

        Parameters:
            name (str, optional): The base name to use for the keys in the mapping dictionary. This name is used
                                  to differentiate between different materials or indices if multiple exist within
                                  the same scatterer.
        """
        detached_material_name = f"{name} material" if name else "material"
        attached_material_name = detached_material_name.replace(' ', '_').lower()

        detached_index_name = f"{name} index" if name else "index"
        attached_index_name = detached_index_name.replace(' ', '_').lower()

        if getattr(self, attached_material_name):
            self.mapping[attached_material_name] = units.Custom(
                long_label=detached_material_name,
                short_label=attached_material_name,
                value_representation=getattr(self, attached_material_name),
                base_values=getattr(self, attached_material_name),
                use_prefix=False,
            )

        else:
            self.mapping[attached_index_name] = units.Index(
                long_label=detached_index_name,
                short_label=attached_index_name,
                base_values=self.binding_kwargs.get(attached_index_name),
                string_format='.2f'
            )

    def add_material_index_to_binding_kwargs(self, name: str, data_type: type) -> NoReturn:
        """
        Adds either material properties or a refractive index to the binding keyword arguments for the experiment.
        This method validates and processes the material or index information, converting it into a format suitable
        for simulation use, and ensuring that either a material or an index is provided but not both.

        Parameters:
            name (str): The base name for the material or index. This name helps identify the property and is used
                        to handle multiple materials or indices.
            data_type (type): The expected Python data type (e.g., float, numpy.ndarray) to which the material
                              or index values should be converted for simulation purposes.

        Raises:
            ValueError: If both a material and an index are provided, or if neither is provided.
        """
        detached_material_name = f"{name} material" if name else "material"
        attached_material_name = detached_material_name.replace(' ', '_').lower()

        detached_index_name = f"{name} index" if name else "index"
        attached_index_name = detached_index_name.replace(' ', '_').lower()

        material_value = getattr(self, attached_material_name)
        index_value = getattr(self, attached_index_name)

        if material_value is not None and index_value is not None:
            raise ValueError(f"Either {name} material or {name} index must be provided, not both.")
        if material_value is None and index_value is None:
            raise ValueError(f"One of {name} material or {name} index must be provided.")

        if material_value:
            self.binding_kwargs[attached_material_name] = numpy.asarray([
                mat.get_refractive_index(self.source.wavelength) for mat in numpy.atleast_1d(getattr(self, attached_material_name))
            ])
            if data_type is float:
                self.binding_kwargs[attached_material_name] = self.binding_kwargs[attached_material_name].real
            self.binding_kwargs[attached_material_name] = self.binding_kwargs[attached_material_name].astype(data_type)

        else:
            self.binding_kwargs[attached_index_name] = numpy.atleast_1d(index_value).astype(data_type)


@dataclass(kw_only=True, slots=True, config=dict(extra='forbid'))
class Sphere(BaseScatterer):
    """
    A data class that represents a spherical scatterer configuration used in PyMieSim simulations.

    This class provides specific implementations for setting up and binding spherical scatterers
    with their properties to a simulation environment. It extends the `BaseScatterer` class by
    adding spherical-specific attributes and methods for handling simulation setups.

    Attributes:
        diameter (List): Diameter(s) of the spherical scatterers in meters.
        medium_index (List, optional): Refractive index or indices of the medium surrounding the scatterers.
        medium_material (List, optional): Material(s) defining the medium, used if `medium_index` is not provided.
        index (List, optional): Refractive index or indices of the spherical scatterers themselves.
        material (List, optional): Material(s) of the scatterers, used if `index` is not provided.
        name (str): Name identifier for the scatterer type, defaulted to 'sphere' and not intended for initialization.
    """
    diameter: Union[List[float], float]
    medium_index: Union[List[float], float, None] = None
    medium_material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None
    index: Union[List[Any], Any] = None
    material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None
    available_measure_list = measure.__sphere__

    def __post_init__(self):
        """
        Extends the base class post-initialization process by setting up additional properties specific to spherical scatterers.
        Initializes a mapping dictionary to support visualization and other operations.
        """
        self.mapping: dict = {
            'diameter': None,
            'index': None,
            'material': None,
            'medium_index': None,
            'medium_material': None
        }

        super(Sphere, self).__post_init__()

    def build_binding_kwargs(self) -> NoReturn:
        """
        Constructs the keyword arguments necessary for the C++ binding interface, specifically tailored for spherical scatterers.
        This includes processing material indices and organizing them into a structured dictionary for simulation interaction.

        This method automatically configures the `binding_kwargs` attribute with appropriately formatted values.
        """
        self.binding_kwargs = dict(
            diameter=numpy.atleast_1d(self.diameter).astype(float),
        )

        self.add_material_index_to_binding_kwargs(name=None, data_type=complex)
        self.add_material_index_to_binding_kwargs(name='medium', data_type=float)

        self.binding = CppSphereSet(**self.binding_kwargs)

    def get_datavisual_table(self) -> NoReturn:
        """
        Constructs a table of the scatterer's properties formatted for data visualization.
        This method populates the `mapping` dictionary with user-friendly descriptions and formats of the scatterer properties.

        Returns:
            list: A list of visual representations for each property in the `mapping` dictionary that has been populated.
        """
        self.mapping['diameter'] = units.Length(
            long_label='Scatterer diameter',
            short_label='diameter',
            base_values=self.binding_kwargs.get('diameter'),
            string_format='.1f'
        )

        self.add_material_index_to_mapping(name=None)
        self.add_material_index_to_mapping(name='Medium')

        return [v for k, v in self.mapping.items() if v is not None]


@dataclass(kw_only=True, slots=True, config=dict(extra='forbid'))
class CoreShell(BaseScatterer):
    """
    A data class representing a core-shell scatterer configuration used in PyMieSim simulations.

    This class facilitates the setup and manipulation of core-shell scatterers by providing structured
    attributes and methods that ensure the scatterers are configured correctly for simulations.
    It extends the BaseScatterer class, adding specific attributes and methods relevant to core-shell geometries.

    Attributes:
        core_diameter (Union[List[float], float]): Diameters of the core components in meters.
        shell_width (Union[List[float], float]): Thicknesses of the shell components in meters.
        medium_index (List, optional): Refractive index or indices of the medium where the scatterers are placed.
        medium_material (List, optional): Material(s) defining the medium, used if `medium_index` is not provided.
        core_index (List, optional): Refractive index or indices of the core.
        shell_index (List, optional): Refractive index or indices of the shell.
        core_material (List, optional): Material(s) of the core, used if `core_index` is not provided.
        shell_material (List, optional): Material(s) of the shell, used if `shell_index` is not provided.
        name (str): An identifier for the scatterer type, defaulted to 'coreshell' and not intended for initialization.
    """
    core_diameter: Union[List[float], float]
    shell_width: Union[List[float], float]
    medium_index: Union[List[float], float, None] = None
    medium_material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None
    shell_index: Union[List[Any], Any, None] = None
    core_material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None
    core_index: Union[List[Any], Any, None] = None
    shell_material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None

    available_measure_list = measure.__coreshell__

    def __post_init__(self):
        """
        Extends the BaseScatterer post-initialization by setting up additional mappings specific to core-shell scatterers.
        Initializes mappings for visualizing and interacting with scatterer properties.
        """
        self.mapping = {
            'core_diameter': None,
            'shell_width': None,
            'core_index': None,
            'core_material': None,
            'shell_index': None,
            'shell_material': None,
            'medium_index': None,
            'medium_material': None
        }

        super(CoreShell, self).__post_init__()

    def build_binding_kwargs(self) -> NoReturn:
        """
        Assembles the keyword arguments necessary for C++ binding, tailored for core-shell scatterers.
        Prepares structured data from scatterer properties for efficient simulation integration.

        This function populates `binding_kwargs` with values formatted appropriately for the C++ backend used in simulations.
        """
        self.binding_kwargs = dict(
            core_diameter=numpy.atleast_1d(self.core_diameter).astype(float),
            shell_width=numpy.atleast_1d(self.shell_width).astype(float),
        )

        self.add_material_index_to_binding_kwargs(name='Core', data_type=complex)
        self.add_material_index_to_binding_kwargs(name='Shell', data_type=complex)
        self.add_material_index_to_binding_kwargs(name='medium', data_type=float)

        self.binding = CppCoreShellSet(**self.binding_kwargs)

    def get_datavisual_table(self) -> NoReturn:
        """
        Generates a list of data visualizations for the scatterer's properties, which can be used in user interfaces or reports.
        Each property is formatted into a user-friendly structure, making it easier to visualize and understand.

        Returns:
            list: A collection of formatted representations for the scatterer properties.
        """
        self.mapping['core_diameter'] = units.Length(
            long_label='Core diameter',
            short_label='core_diameter',
            base_values=self.binding_kwargs.get('core_diameter'),
            string_format='.2f'
        )

        self.mapping['shell_width'] = units.Length(
            long_label='Shell width',
            short_label='shell_width',
            base_values=self.binding_kwargs.get('shell_width'),
            string_format='.2f'
        )

        self.add_material_index_to_mapping(name='Core')
        self.add_material_index_to_mapping(name='Shell')
        self.add_material_index_to_mapping(name='Medium')

        return [v for k, v in self.mapping.items() if v is not None]


@dataclass(kw_only=True, slots=True, config=dict(extra='forbid'))
class Cylinder(BaseScatterer):
    """
    Represents a cylindrical scatterer configuration for PyMieSim simulations.

    Attributes:
        diameter (List): Diameter(s) of the cylinder in meters.
        height (List): Height(s) of the cylinder in meters.
        index (List, optional): Refractive index of the cylinder.
        material (List, optional): Material(s) of the cylinder, used if `index` is not provided.
    """
    diameter: Union[List[float], float]
    medium_index: Union[List[float], float, None] = None
    medium_material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None
    index: Union[List[Any], Any, None] = None
    material: Union[List[Sellmeier | DataMeasurement], Sellmeier | DataMeasurement, None] = None

    available_measure_list = measure.__cylinder__

    def __post_init__(self):
        self.mapping = {
            'diameter': None,
            'index': None,
            'material': None,
            'medium_index': None,
            'medium_material': None
        }

        super(Cylinder, self).__post_init__()

    def build_binding_kwargs(self) -> NoReturn:
        """
        Prepares the keyword arguments for the C++ binding based on the scatterer's properties. This
        involves evaluating material indices and organizing them into a dictionary for the C++ interface.

        Returns:
            None
        """
        self.binding_kwargs = dict(
            diameter=numpy.atleast_1d(self.diameter).astype(float),
        )

        self.add_material_index_to_binding_kwargs(name=None, data_type=complex)
        self.add_material_index_to_binding_kwargs(name='medium', data_type=float)

        self.binding = CppCylinderSet(**self.binding_kwargs)

    def get_datavisual_table(self) -> NoReturn:
        """
        Appends the scatterer's properties to a given table for visualization purposes. This enables the
        representation of scatterer properties in graphical formats.

        Parameters:
            table (list): The table to which the scatterer's properties will be appended.

        Returns:
            list: The updated table with the scatterer's properties included.
        """
        self.mapping['diameter'] = units.Length(
            long_label='Scatterer diameter',
            short_label='diameter',
            base_values=self.binding_kwargs.get('diameter'),
            string_format='.1f'
        )

        self.add_material_index_to_mapping(name=None)
        self.add_material_index_to_mapping(name='Medium')

        return [v for k, v in self.mapping.items() if v is not None]

# -
