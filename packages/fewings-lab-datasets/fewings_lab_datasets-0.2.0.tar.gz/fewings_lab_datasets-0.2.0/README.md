Fewings Lab Datasets
====================

`fewings-lab-datasets` is a Python package for accessing various oceanographic datasets assembled by members of the [Fewings Lab](https://fewingslab.ceoas.oregonstate.edu/).

Installation
------------

The latest version can be downloaded using Pip:

    pip install fewings-lab-datasets

You can install the most up-to-date version using:

    pip install git+https://github.com/andrew-s28/fewings-lab-datasets.git

Usage
-----

Import specific datasets from this package:
    
    from fldatasets import NHLSections

The following datasets have been implemented as classes in this package:

* [NHLSections](https://fewings-lab-datasets.readthedocs.io/en/latest/nhl_data.html)
    * [Spatially gridded cross-shelf hydrographic sections and monthly climatologies from shipboard survey data collected along the Newport Hydrographic Line, 1997–2021](https://www.sciencedirect.com/science/article/pii/S2352340922001342)

Each dataset class has slightly different methods to access the data, since each dataset itself is different.
The documentation for each dataset class describes the methods available for that dataset.

Credits
-------

The datasets contained within this package were collected by a wide range of people working for lots of different programs, and we owe many thanks to their efforts.
Members of the Fewings Lab have assembled these datasets, and every dataset available in this package has a corresponding publication that should be cited when using the data.