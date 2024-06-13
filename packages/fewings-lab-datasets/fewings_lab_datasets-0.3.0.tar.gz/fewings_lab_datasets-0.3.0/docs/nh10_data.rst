NH10Mooring
===========

.. |citation| raw:: html

    <div style="text-indent: -36px; padding-left: 36px;">
    <p>Risien, C. M., Cervantes, B. T., Fewings, M. R., Barth, J. A., & Kosro, P. M. (2023). A stitch in time: Combining more than two decades of mooring data from the central Oregon shelf. Data in Brief, 48, 109041. https://doi.org/10.1016/j.dib.2023.109041</p>
    </div>

.. admonition:: If you use this dataset, please cite it!

    You can access the citation in BibTeX format using :code:`NHLSections().get_citation()`. The plain text version is also included here for convenience:
        |citation|

.. caution::

    Temperature and salinity profiles are not available at all times or depths when velocities are available.
    If you are seeing a blank plot or getting an error, this might be the reason why. Try a different date, 
    use the method :func:`~NH10Mooring.get_valid_depths` to find depths with values, or see
    the `publication <https://www.sciencedirect.com/science/article/pii/S2352340923001592#sec0004>'_
    for more information.

.. currentmodule:: fldatasets

.. autoclass:: NH10Mooring
    :members: