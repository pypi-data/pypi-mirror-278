from importlib.resources import files
import os
import textwrap
from typing import Union
import warnings

import cmocean.cm as cmo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from numpy.typing import ArrayLike
import xarray as xr


class NH10Mooring:
    """Twenty years of temperature, practical salinity, and velocity data from NH-10 moorings combined into one coherent, hourly averaged, quality-controlled data set, 
    as described in `Risien, et. al., 2023 <https://www.sciencedirect.com/science/article/pii/S2352340923001592>`_.

    .. ipython:: python
        from fldatasets import NH10Mooring
        NH10Mooring()

    :param load_dir: if ``str``, directory to load datasets from, if ``None`` the default package directory is used, defaults to ``None``
    :type load_dir: str, optional
    :param preload: if ``True``, lazy loads all datasets into memory upon instantiation of class, defaults to ``False``
    :type preload: bool, optional
    :return: object for accessing gridded hourly data and climatologies from the NH-10 Mooring
    :rtype: :class:`NH10Mooring`
    """

    HOURLY_DATA_FILE = "nh10_hourly_data_1997_2021.nc"
    CLIMATOLOGY_FILE = "nh10_climatologies.nc"
    COEFFICIENTS_FILE = "nh10_climatology_coefficients.nc"
    VARS = [
        'temperature',
        'salinity',
        'eastward_velocity',
        'northward_velocity',
    ]
    CMAP_DICT = {
        'temperature': cmo.thermal,
        'salinity': cmo.haline,
        'eastward_velocity': cmo.balance,
        'northward_velocity': cmo.balance,
        }
    LABEL_DICT = {
        'temperature': 'Temperature ($\\mathrm{\\degree C}$)',
        'salinity': 'Salinity ($\\mathrm{{PSU}}$)',
        'eastward_velocity': 'Eastward Velocity ($\\mathrm{m/s}$)',
        'northward_velocity': 'Northward Velocity ($\\mathrm{m/s}$)',
        }
    CITATION = """\
    @article{risien_stitch_2023,
        title = {A stitch in time: {Combining} more than two decades of mooring data from the central {Oregon} shelf},
        volume = {48},
        issn = {2352-3409},
        shorttitle = {A stitch in time},
        url = {https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10031349/},
        doi = {10.1016/j.dib.2023.109041},
        urldate = {2024-01-24},
        journal = {Data in Brief},
        author = {Risien, Craig M. and Cervantes, Brandy T. and Fewings, Melanie R. and Barth, John A. and Kosro, P. Michael},
        month = mar,
        year = {2023},
        pmid = {36969969},
        pmcid = {PMC10031349},
        pages = {109041},
    }"""
    CITATION = textwrap.dedent(CITATION)

    def __init__(self, load_dir: str = None, preload: bool = False,):
        if load_dir is not None:
            if not os.path.exists(load_dir):
                raise FileNotFoundError(f"Directory {load_dir!r} does not exist.")

        self.load_dir = load_dir

        self.hourly_data = None
        self.climatology = None
        self.coefficients = None

        if preload:
            self.get_hourly_data()
            self.get_climatology()
            self.get_coefficients()

    def get_hourly_data(self) -> xr.Dataset:
        """Loads dataset containing gridded hourly data.

        :Example:
        .. ipython:: python

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            nh10.get_hourly_data()

        :return: dataset containing gridded hourly data
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.hourly_data is not None:
            return self.hourly_data
        self.hourly_data = self._open_file(NH10Mooring.HOURLY_DATA_FILE) 
        return self.hourly_data

    def get_climatology(self) -> xr.Dataset:
        """Loads dataset containing daily climatologies.

        :Example:
        .. ipython:: python

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            nh10.get_climatology()

        :return: dataset containing monthly climatologies
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.climatology is not None:
            return self.climatology
        self.climatology = self._open_file(NH10Mooring.CLIMATOLOGY_FILE)
        return self.climatology

    def get_variables(self) -> list[str]:
        """Returns the variables available in the dataset.

        :Example:
        .. ipython:: python

            from fldatasets import NHLhourly_data
            nh10 = NH10Mooring()
            nh10.get_variables()

        :return: variables available in the dataset
        :rtype: list[str]
        """
        return NH10Mooring.VARS

    def get_coefficients(self) -> xr.Dataset:
        """Loads dataset containing climatology coefficients.

        :Example:
        .. ipython:: python

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            nh10.get_coefficients()

        :return: dataset containing climatology coefficients
        :rtype: `xarray.Dataset <http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html>`_
        """
        if self.coefficients is not None:
            return self.coefficients
        self.coefficients = self._open_file(NH10Mooring.COEFFICIENTS_FILE)
        return self.coefficients

    def get_citation(self) -> str:
        """Returns the citation for this dataset in BibTeX format.

        :Example:
        .. ipython:: python

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            print(nh10.get_citation())

        :return: citation in BibTeX format
        :rtype: str
        """
        return self.CITATION

    def get_valid_depths(self, variable: str) -> ArrayLike:
        """Returns the valid (i.e., depths where there is not all NaN values) depths for a specified variable.

        :Example:
        .. ipython:: python

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            nh10.get_valid_depths('temperature')

        :param variable: variable to get valid depths for, options include ``'temperature'``, ``'salinity'``, ``'eastward_velocity'``, ``'northward_velocity'``
        :type variable: str
        :return: valid depths for the specified variable
        :rtype: ArrayLike
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NH10Mooring.get_variables`)
        """
        if variable not in NH10Mooring.VARS:
            raise KeyError(f"No variable named {variable!r}. Variables on the dataset include {repr(NH10Mooring.VARS)}")
        if self.hourly_data is None:
            self.get_hourly_data()
        data = self.hourly_data[variable]
        data = data.where(data.notnull(), drop=True)
        return data.depth.values

    def plot_time_series(self, variable: str, depth: int, start_date: str = None, end_date: str = None) -> None:
        """Creates a time series plot of a specified variable at a specified depth from the dataset.

        :Example:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_time_series(variable='temperature', depth=8, start='2016-01-01', end='2021-01-01')

        :param variable: variable to plot, options include ``'temperature'``, ``'salinity'``, ``'eastward_velocity'``, ``'northward_velocity'``
        :type variable: str
        :param depth: depth to plot, from 0-80 meters
        :type depth: int
        :param start_date: start date for time series plot, defaults to ``None`` (default starts from beginning of full dataset)
        :type start_date: str, optional
        :param end_date: end date for time series plot, defaults to ``None`` (default ends at end of full dataset)
        :type end_date: str, optional
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NH10Mooring.get_variables`)
        :raises ValueError: if no data is available for the specified variable and depth
        """
        if self.hourly_data is None:
            self.get_hourly_data()
        if variable not in NH10Mooring.VARS:
            raise KeyError(f"No variable named {variable!r}. Variables on the dataset include {repr(NH10Mooring.VARS)}")
        if depth % 2 != 0:
            warnings.warn("Depth bins are 2 m, meaning any odd depths will be interpretted as the closest even depth.", UserWarning)
        time_series_data = self.hourly_data.sel(depth=depth, method='nearest')[variable].squeeze()
        depth = int(time_series_data.depth.values)
        if time_series_data.isnull().all():
            raise ValueError(f"No data available for {variable!r} at depth of {depth!r} m.")
        self._plot_time_series(
            time_series_data.time,
            time_series_data.values,
            NH10Mooring.LABEL_DICT[variable],
            'Time Series at Depth ' + str(depth) + ' m',
            start=start_date,
            end=end_date,
            )

    def plot_profile(self, variable: str, profile: Union[int, str]) -> None:
        """Creates a plot of a single profile of a variable from the dataset.

        .. note::

            Temperature and salinity profiles are not available at all times or depths when velocities are available.
            If you are seeing a blank plot or getting an error, this might be the reason why. Try a different date or see
            the `publication <https://www.sciencedirect.com/science/article/pii/S2352340923001592#sec0004>'_
            for more information.

        :Example:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_profile(variable='eastward_velocity', profile='2015-05-01')

        :param variable: variable to plot, options include ``'temperature'``, ``'salinity'``, ``'eastward_velocity'``, ``'northward_velocity'``
        :type variable: str
        :param profile: profile to plot, if ``int`` the index of the profile, if ``str`` the date of the profile, e.g. ``'2015-05-01'`` (the profile closest to the specified date is plotted)
        :type profile: int or str
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NH10Mooring.get_variables`)
        :raises ValueError: if no data is available for the specified profile
        """
        if self.hourly_data is None:
            self.get_hourly_data()
        if variable not in NH10Mooring.VARS:
            raise KeyError(f"No variable named {variable!r}. Variables on the dataset include {repr(NH10Mooring.VARS)}")
        if isinstance(profile, int):
            profile_data = self.hourly_data.isel(time=profile)[variable].squeeze()
        elif isinstance(profile, str):
            profile_data = self.hourly_data.sel(time=profile, method='nearest')[variable].squeeze()
        if profile_data.isnull().all():
            raise ValueError(f"No data available for {variable!r} at time {np.datetime_as_string(profile_data.time.values)!r}.")
        profile_data = profile_data.dropna('depth')
        self._plot_profile(
            profile_data.depth,
            profile_data.values,
            NH10Mooring.LABEL_DICT[variable],
            profile_data.time.values.astype('datetime64[D]').astype(str) + ' Profile'
            )

    def plot_velocity_climatology(self, depth: int = None) -> None:
        """Creates a plot of the daily climatology of velocities.
        If depth is not specified, creates a pcolor plot, otherwise creates multiple line plots.

        .. note::

            Temperature and salinity climatologies are not available at all depths when velocities are available.
            If you are seeing a blank plot, this might be the reason why. Try a different depth or see
            the `publication <https://www.sciencedirect.com/science/article/pii/S2352340923001592#sec0004>'_
            for more information.

        :Example:
        Plot all depths as `pcolormesh <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolormesh.html>`_ plot:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_velocity_climatology()

        Plot specific depths as `line <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html>`_ plots:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_velocity_climatology(depth=8)

        :param depth: depth to plot, from 0-80 meters, defaults to ``None`` (default plots all depths as pcolormesh plot)
        :type depth: int, optional
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NH10Mooring.get_variables`)
        :raises ValueError: if depth is not between 0 and 80 meters
        """
        if self.climatology is None:
            self.get_climatology()
        if depth is None:
            data = self.climatology.squeeze()
            self._plot_velocities(
                data.time.values,
                data.depth.values,
                data.eastward_velocity.values,
                data.northward_velocity.values,
                True,
                )
        else:
            if depth not in range(0, 81):
                raise ValueError(f"Depth must be between 0 and 80 meters, not {depth!r}")
            if depth % 2 != 0:
                warnings.warn("Depth bins are 2 m, meaning any odd depths will be interpretted as the closest even depth.", UserWarning)
            data = self.climatology.squeeze().sel(depth=depth, method='nearest')
            self._plot_velocities(
                data.time.values,
                data.depth.values,
                data.eastward_velocity.values,
                data.northward_velocity.values,
                False,
                )

    def plot_temp_sal_climatology(self, depth: int = None) -> None:
        """Creates a plot of the daily climatology of temperature and salinity.
        If depth is not specified, creates a line plot of all available depths, otherwise creates line plots only at specified depth.

        .. note::

            Temperature and salinity climatologies are not available at all depths when velocities are available.
            If you are seeing a blank plot or getting an error, this might be the reason why. Try a different depth or see
            the `publication <https://www.sciencedirect.com/science/article/pii/S2352340923001592#sec0004>'_
            for more information.

        :Example:
        Plot all depths:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_temp_sal_climatology()

        Plot a specific depth:
        .. plot::

            >>> from fldatasets import NH10Mooring
            >>> nh10 = NH10Mooring()
            >>> nh10.plot_temp_sal_climatology(depth=8)

        :param depth: depth to plot, from 0-80 meters, defaults to ``None`` (default plots all depths)
        :type depth: int, optional
        :raises KeyError: if variable is not valid for the dataset (see also :func:`~NH10Mooring.get_variables`)
        :raises ValueError: if depth is not between 0 and 80 meters
        """
        if self.climatology is None:
            self.get_climatology()
        if depth is None:
            data = self.climatology.squeeze()
            self._plot_temp_sal(
                data.time.values,
                data.depth.values,
                data.temperature.values,
                data.salinity.values,
                )
        else:
            if depth not in range(0, 81):
                raise ValueError(f"Depth must be between 0 and 80 meters, not {depth!r}")
            if depth % 2 != 0:
                warnings.warn("Depth bins are 2 m, meaning any odd depths will be interpretted as the closest even depth.", UserWarning)
            data = self.climatology.squeeze().sel(depth=depth, method='nearest')
            if data.temperature.isnull().all() and data.salinity.isnull().all():
                raise ValueError(f"No data available for temperature or salinity at depth of {depth!r} m.")
            self._plot_temp_sal(
                data.time.values,
                data.depth.values,
                data.temperature.values,
                data.salinity.values,
                all_depths=False,
                )

    def save(self, save_dir: str) -> None:
        """Saves all datasets to a specified directory.

        .. warning::
            You must keep the file names the same after saving! Custom file names have not been implemented.

        :Example:
        .. ipython:: python
            :verbatim:

            from fldatasets import NH10Mooring
            nh10 = NH10Mooring()
            nh10.save('/some/path')  # save dataset to local path
            nh10 = NH10Mooring(load_dir='/some/path')  # can now open datasets from new path

        :param save_dir: path to save datasets
        :type save_dir: str
        """
        if self.hourly_data is None:
            self.get_hourly_data()
        if self.climatology is None:
            self.get_climatology()
        if self.coefficients is None:
            self.get_coefficients()
        self.climatology.to_netcdf(os.path.join(save_dir, self.CLIMATOLOGY_FILE))
        self.hourly_data.to_netcdf(os.path.join(save_dir, self.HOURLY_DATA_FILE))
        self.coefficients.to_netcdf(os.path.join(save_dir, self.COEFFICIENTS_FILE))

    def _open_file(self, file_name) -> xr.Dataset:
        if self.load_dir is None:
            load_path = files('fldatasets.data').joinpath(file_name)
        else:
            load_path = os.path.join(self.load_dir, file_name)
        file = xr.open_dataset(load_path)
        return file

    def _plot_velocities(self, time, depth, east_vel, north_vel, pcolor) -> None:
        # plot things
        fig, axs = plt.subplots(2, 1, sharex=True)
        if pcolor:
            # make sure colorbar is centered for velocity plots
            if np.abs(east_vel.max()) > np.abs(east_vel.min()):
                max = np.abs(east_vel.max())
            elif np.abs(east_vel.max()) < np.abs(east_vel.min()):
                max = np.abs(east_vel.min())
            pcm = axs[0].pcolormesh(time, -depth, east_vel, shading='gouraud', cmap=cmo.balance, vmin=-max, vmax=max)
            c = axs[0].contour(time, -depth, east_vel, colors='black', linewidths=0.5)
            axs[0].clabel(c, inline=True)
            cbar = plt.colorbar(pcm, ax=axs[0])
            cbar.set_label('Zonal Velocity ($\\mathrm{{m/s}}$)', rotation=270, labelpad=20)
            if np.abs(north_vel.max()) > np.abs(north_vel.min()):
                max = np.abs(north_vel.max())
            elif np.abs(north_vel.max()) < np.abs(north_vel.min()):
                max = np.abs(north_vel.min())
            c = axs[1].contour(time, -depth, north_vel, colors='black', linewidths=0.5)
            axs[1].clabel(c, inline=True)
            pcm = axs[1].pcolormesh(time, -depth, north_vel, shading='gouraud', cmap=cmo.balance, vmin=-max, vmax=max)
            cbar = plt.colorbar(pcm, ax=axs[1])
            cbar.set_label('Meridional Velocity ($\\mathrm{{m/s}}$)', rotation=270, labelpad=20)
            axs[1].set_xticks(np.arange(time[0] - np.timedelta64(1, 'D'), time[-1], np.timedelta64(365, 'D')))
            [ax.set_ylim(-80, 0) for ax in axs]
            fig.supylabel('Depth ($\\mathrm{{m}}$)')
        else:
            axs[0].plot(time, east_vel, label=f'{int(depth)} m')
            axs[1].plot(time, north_vel, label=f'{int(depth)} m')
            axs[0].legend()
            axs[0].set_ylabel('Zonal Velocity ($\\mathrm{{m/s}}$)')
            axs[1].set_ylabel('Meridional Velocity ($\\mathrm{{m/s}}$)')
        axs[1].xaxis.set_major_locator(mdates.MonthLocator())
        axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        fig.supxlabel('Time')
        fig.suptitle('Daily Velocity Climatology', y=0.95)
        plt.show()

    def _plot_temp_sal(self, time, depth, temp, sal, all_depths=True) -> None:
        fig, axs = plt.subplots(2, 1, sharex=True)
        if all_depths:
            cmap = cmo.tools.crop_by_percent(cmo.dense, 30, which='both')
            cmap = cmap.from_list('cmap', cmap(np.linspace(0, 1, 11)), len(depth))
            for i, (d, t, s) in enumerate(zip(depth, temp, sal)):
                if np.isnan(t).all() and np.isnan(s).all():
                    continue
                axs[0].plot(time, t, label=f'{int(d)} m', c=cmap(i))
                axs[1].plot(time, s, label=f'{int(d)} m', c=cmap(i))
                axs[0].legend(bbox_to_anchor=(1.2, 1))
        else:
            axs[0].plot(time, temp, label=f'{int(depth)} m')
            axs[1].plot(time, sal, label=f'{int(depth)} m')
            axs[0].legend()
        axs[0].set_ylabel('Temperature ($\\mathrm{\\degree C}$)')
        axs[1].set_ylabel('Salinity ($\\mathrm{PSU}$)')
        axs[1].xaxis.set_major_locator(mdates.MonthLocator())
        axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        fig.suptitle('Daily Temperature and Salinity Climatology', y=0.95)

    def _plot_profile(self, depth, data, label, time_label) -> None:
        # plot things
        fig, ax = plt.subplots()
        ax.plot(data, -depth, '-o')
        ax.set_xlabel(label)
        ax.set_ylim(-90, 10)
        ax.set_ylabel('Depth ($\\mathrm{m}$)')
        ax.set_title(time_label)
        plt.show()

    def _plot_time_series(self, time, data, label, depth_label, start=None, end=None) -> None:
        # plot things
        fig, ax = plt.subplots()
        ax.plot(time, data)
        ax.set_xlabel('Time')
        ax.set_ylabel(label)
        ax.set_title(depth_label)
        if start is not None and end is not None:
            start = np.datetime64(start)
            end = np.datetime64(end)
            if start < time[0]:
                start = time[0]
            if end > time[-1]:
                end = time[-1]
            ax.set_xlim(start, end)
        elif start is not None and end is None:
            start = np.datetime64(start)
            if start < time[0]:
                start = time[0]
            ax.set_xlim(start, time[-1])
        elif start is None and end is not None:
            end = np.datetime64(end)
            if end > time[-1]:
                end = time[-1]
            ax.set_xlim(time[0], end)
        xaxis_length = ax.get_xlim()[1] - ax.get_xlim()[0]
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        if xaxis_length <= 365:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha='right')
        elif xaxis_length <= 365*5:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.show()
