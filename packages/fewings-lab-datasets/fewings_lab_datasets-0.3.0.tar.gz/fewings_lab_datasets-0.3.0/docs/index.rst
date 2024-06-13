Fewings Lab Datasets
====================

:code:`fewings-lab-datasets` is a Python package for accessing various oceanographic datasets assembled by members of the `Fewings Lab <https://fewingslab.ceoas.oregonstate.edu/>`_.

Installation
------------

The latest version can be downloaded using Pip::

    >>> pip install fewings-lab-datasets

You can install the most up-to-date version using::

    >>> pip install git+https://github.com/andrew-s28/fewings-lab-datasets.git

Only Python 3.10 and later are supported, as this package accesses data files via namespace packages `which were introduced in Python 3.10 <https://github.com/python/importlib_resources/pull/196#issuecomment-734520374>`_.
You should consider updating your Python installation if you are using an older version, since Python 3.9 will reach `EOL in October 2025 <https://devguide.python.org/versions/>`_.

Usage
-----

Import specific datasets from this package:
    
    >>> from fldatasets import NHLSections, NH10Mooring

The following datasets have been implemented as classes in this package:

* `NHLSections <https://fewings-lab-datasets.readthedocs.io/en/latest/nhl_data.html>`_
    * `Spatially gridded cross-shelf hydrographic sections and monthly climatologies from shipboard survey data collected along the Newport Hydrographic Line, 1997–2021 <https://www.sciencedirect.com/science/article/pii/S2352340922001342>`_
* `NH10Mooring <https://fewings-lab-datasets.readthedocs.io/en/latest/nh10_data.html>`_
    * `A stitch in time: Combining more than two decades of mooring data from the central Oregon shelf <https://www.sciencedirect.com/science/article/pii/S2352340923001592>`_

Each dataset class has slightly different methods to access the data, since each dataset itself is different, but are structured to be as similar as possible.

Credits
-------

The datasets contained within this package were collected by a wide range of people working for lots of different programs, and we owe many thanks to their efforts.
Members of the Fewings Lab have assembled these datasets, and every dataset available in this package has a corresponding publication that should be cited when using the data.

.. toctree::
    :maxdepth: 1
    :caption: Datasets
    :hidden:

    nhl_data
    nh10_data