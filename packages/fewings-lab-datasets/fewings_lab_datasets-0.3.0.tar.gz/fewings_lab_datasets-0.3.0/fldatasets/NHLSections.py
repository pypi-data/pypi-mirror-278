from importlib.resources import files
import os
import textwrap
from typing import Union

import cmocean.cm as cmo
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


class NHLSections:
    """Gridded, cross-shelf, hydrographic sections and derived monthly climatologies from the Newport Hydrographic Line station data,
    as described in `Risien et. al., 2022 <https://www.sciencedirect.com/science/article/pii/S2352340922001342>`_.

    .. ipython:: python
        from fldatasets import NHLSections
        NHLSections()

    :param load_dir: if ``str``, directory to load datasets from, if ``None`` the default package directory is used, defaults to ``None``
    :type load_dir: str, optional
    :param preload: if ``True``, lazy loads all datasets into memory upon instantiation of class, defaults to ``False``
    :type preload: bool, optional
    :return: object for accessing gridded sections and climatologies from the Newport Hydrographic Line
    :rtype: :class:`NHLSections`
    """

    SECTIONS_FILE = "newport_hydrographic_line_gridded_sections.nc"
    CLIMATOLOGY_FILE = "newport_hydrographic_line_gridded_section_climatologies.nc"
    COEFFICIENTS_FILE = "newport_hydrographic_line_gridded_section_coefficients.nc"
    BATHYMETRY_FILE = "newport_hydrographic_line_bathymetry.nc"
    VARS = [
        'temperature',
        'salinity',
        'potential_density',
        'spiciness',
        'dissolved_oxygen',
    ]
    CMAP_DICT = {
        'temperature': cmo.thermal,
        'salinity': cmo.haline,
        'potential_density': cmo.dense,
        'spiciness': cmo.balance,
        'dissolved_oxygen': cmo.matter,
        }
    LABEL_DICT = {
        'temperature': 'Temperature ($\\mathrm{\\degree C}$)',
        'salinity': 'Salinity ($\\mathrm{{PSU}}$)',
        'potential_density': 'Potential Density ($\\mathrm{kg/m^3}$)',
        'spiciness': 'Spiciness ($\\mathrm{kg/m^3}$)',
        'dissolved_oxygen': 'Oxygen ($\\mathrm{\\mu mol / kg}$)',
        }
    MONTH_DICT = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }
    CITATION = """\
    @article{risien_spatially_2022,
        title = {Spatially gridded cross-shelf hydrographic sections and monthly climatologies from shipboard survey data collected along the {Newport} {Hydrographic} {Line}, 1997–2021},
        volume = {41},
        tissn = {2352-3409},
        turl = {https://www.sciencedirect.com/science/article/pii/S2352340922001342},
        tdoi = {10.1016/j.dib.2022.107922},
        tlanguage = {en},
        turldate = {2022-11-02},
        tjournal = {Data in Brief},
        tauthor = {Risien, Craig M. and Fewings, Melanie R. and Fisher, Jennifer L. and Peterson, Jay O. and Morgan, Cheryl A.},
        tmonth = apr,
        tyear = {2022},
        tkeywords = {Dissolved oxygen, Oregon, California current, Climatology, Potential density, Practical salinity, Seawater temperature, Spiciness},
        tpages = {107922},
    }"""
    CITATION = textwrap.dedent(CITATION)

    def __init__(self, load_dir: str = None, preload: bool = False,):
        if load_dir is not None:
            if not os.path.exists(load_dir):
                raise FileNotFoundError(f"Directory {load_dir!r} does not exist.")

        self.load_dir = load_dir

        self.sections = None
        self.climatology = None
        self.bathymetry = None
        self.coefficients = None

        if preload:
            self.get_sections()
            self.get_climatology()
            self.get_bathymetry()
            self.get_coefficients()

    def get_sections(self) -> xr.Dataset:
        """Loads dataset containing gridded sections and saves it locally.
        If the dataset has not been loaded yet, it is loaded into memory.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.get_sections()

        :return: dataset containing gridded sections
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.sections is not None:
            return self.sections
        self.sections = self._open_file(NHLSections.SECTIONS_FILE) 
        return self.sections

    def get_climatology(self) -> xr.Dataset:
        """Loads dataset containing monthly climatologies and saves it locally.
        If the dataset has not been loaded yet, it is loaded into memory.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.get_climatology()

        :return: dataset containing monthly climatologies
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.climatology is not None:
            return self.climatology
        self.climatology = self._open_file(NHLSections.CLIMATOLOGY_FILE)
        return self.climatology

    def get_variables(self) -> list[str]:
        """Returns the variables available in the dataset.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.get_variables()

        :return: variables available in the dataset
        :rtype: list[str]
        """
        return NHLSections.VARS

    def get_coefficients(self) -> xr.Dataset:
        """Loads dataset containing climatology coefficients.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.get_coefficients()

        :return: dataset containing climatology coefficients
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.coefficients is not None:
            return self.coefficients
        self.coefficients = self._open_file(NHLSections.COEFFICIENTS_FILE)
        return self.coefficients

    def get_bathymetry(self) -> xr.Dataset:
        """Returns the bathymetry data for the Newport Hydrographic Line.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.get_bathymetry()

        :return: bathymetry
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.bathymetry is not None:
            return self.bathymetry
        self.bathymetry = self._open_file(NHLSections.BATHYMETRY_FILE)
        return self.bathymetry

    def get_citation(self) -> str:
        """Returns the citation for this dataset in BibTeX format.

        :Example:
        .. ipython:: python

            from fldatasets import NHLSections
            nhl = NHLSections()
            print(nhl.get_citation())

        :return: citation in BibTeX format
        :rtype: str
        """
        return self.CITATION

    def plot_section(self, variable: str, section: Union[int, str]) -> None:
        """Creates a plot of a gridded section of a variable from the dataset.

        :Example:
        .. plot::

            >>> from fldatasets import NHLSections
            >>> nhl = NHLSections()
            >>> nhl.plot_section(variable='temperature', section='2015-05-01')

        :param variable: variable to plot, options include ``'temperature'``, ``'salinity'``, ``'potential_density'``, ``'spiciness'``, ``'dissolved_oxygen'``
        :type variable: str
        :param section: section to plot, if ``int`` the index of the section, if ``str`` the date of the section, e.g. ``'2015-05-01'`` (the section closest to the specified date is plotted)
        :type section: int or str
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NHLSections.get_variables`)
        """
        if self.sections is None:
            self.get_sections()
        if variable not in NHLSections.VARS:
            raise KeyError(f"No variable named {variable!r}. Variables on the dataset include {repr(NHLSections.VARS)}")
        if isinstance(section, int):
            section_data = self.sections.isel(time=section)[variable].squeeze()
        elif isinstance(section, str):
            section_data = self.sections.sel(time=section, method='nearest')[variable].squeeze()
        self._plot(
            section_data.longitude,
            section_data.pressure,
            section_data.T,
            NHLSections.CMAP_DICT[variable],
            NHLSections.LABEL_DICT[variable],
            section_data.time.values.astype('datetime64[D]').astype(str) + ' Section'
            )

    def plot_climatology(self, variable: str, month: int) -> None:
        """Creates a plot of the climatology of a variable from the dataset for a specified month.

        :Example:
        .. plot::

            >>> from fldatasets import NHLSections
            >>> nhl = NHLSections()
            >>> nhl.plot_climatology(variable='salinity', month=5)

        :param variable: variable to plot, options include ``'temperature'``, ``'salinity'``, ``'potential_density'``, ``'spiciness'``, ``'dissolved_oxygen'``
        :type variable: str
        :param month: month to plot, from 1-12 for Jan-Dec
        :type month: int
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NHLSections.get_variables`)
        :raises ValueError: if month is not between 1 and 12
        """
        if self.climatology is None:
            self.get_climatology()
        if month < 1 or month > 12:
            raise ValueError('Month must be between 1 and 12.')
        if variable not in NHLSections.VARS:
            raise KeyError(f"No variable named {variable!r}. Variables on the dataset include {repr(NHLSections.VARS)}")
        month_data = self.climatology.isel(time=month-1)[variable].squeeze()
        self._plot(
            month_data.longitude,
            month_data.pressure,
            month_data.T,
            NHLSections.CMAP_DICT[variable],
            NHLSections.LABEL_DICT[variable],
            NHLSections.MONTH_DICT[month] + ' Climatology'
            )

    def save(self, save_dir: str) -> None:
        """Saves all datasets to a specified directory.

        .. warning::
            You must keep the file names the same after saving! Custom file names have not been implemented.

        :Example:
        .. ipython:: python
            :verbatim:

            from fldatasets import NHLSections
            nhl = NHLSections()
            nhl.save('/some/path')  # save dataset to local path
            nhl = NHLSections(load_dir='/some/path')  # can now open datasets from new path

        :param save_dir: path to save datasets
        :type save_dir: str
        """
        if self.sections is None:
            self.get_sections()
        if self.climatology is None:
            self.get_climatology()
        if self.bathymetry is None:
            self.get_bathymetry()
        if self.coefficients is None:
            self.get_coefficients()
        self.climatology.to_netcdf(os.path.join(save_dir, self.CLIMATOLOGY_FILE))
        self.sections.to_netcdf(os.path.join(save_dir, self.SECTIONS_FILE))
        self.bathymetry.to_netcdf(os.path.join(save_dir, self.BATHYMETRY_FILE))
        self.coefficients.to_netcdf(os.path.join(save_dir, self.COEFFICIENTS_FILE))

    def _open_file(self, file_name) -> xr.Dataset:
        if self.load_dir is None:
            load_path = files('fldatasets.data').joinpath(file_name)
        else:
            load_path = os.path.join(self.load_dir, file_name)
        file = xr.open_dataset(load_path)
        return file

    def _plot(self, lon, pres, data, cmap, label, time_label) -> None:
        # make sure bathymetry is loaded
        self.get_bathymetry()
        # plot things
        fig, ax = plt.subplots()
        if data.name == 'spiciness':
            # make sure colorbar is centered for spiciness plots
            if np.abs(data.max()) > np.abs(data.min()):
                max = np.abs(data.max())
            elif np.abs(data.max()) < np.abs(data.min()):
                max = np.abs(data.min())
            pcm = ax.pcolormesh(lon, -pres, data, shading='gouraud', cmap=cmap, vmin=-max, vmax=max)
        else:
            # use default colorbar for everything else
            pcm = ax.pcolormesh(lon, -pres, data, shading='gouraud', cmap=cmap)
        c = ax.contour(lon, -pres, data, colors='black', linewidths=0.5)
        ax.clabel(c, inline=True)
        ax.plot(self.bathymetry.longitude, self.bathymetry.sea_floor_depth, color='black')
        ax.axhline(0, color='black')
        ax.set_ylim(-150, 10)
        ax.set_ylabel('Pressure ($\\mathrm{{dbar}}$)')
        ax.set_xlabel('Longitude ($\\mathrm{\\degree E}$)')
        ax.set_title(time_label)
        cbar = plt.colorbar(pcm, ax=ax)
        cbar.set_label(label, rotation=270, labelpad=20)
        plt.show()
