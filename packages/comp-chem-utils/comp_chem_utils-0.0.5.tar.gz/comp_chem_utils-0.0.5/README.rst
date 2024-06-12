=============
CompChemUtils
=============

|ccu|_ is a set of tools for computational chemistry workflows.

Requirements
============

* Python_ 3.10 or later
* |click|_ (package for command line interfaces)
* |numpy|_ (N-dimensional array package)
* |scipy|_ (library for scientific computing)
* |ase|_ (tools for atomistic simulations)

Installation
============

.. code-block:: console

    python3 -m pip install comp-chem-utils

or, if you use poetry:

.. code-block:: console

    poetry add comp-chem-utils

You can also install the in-development version with:

.. code-block:: console

    pip install git+ssh://git@gitlab.com:ugognw/python-comp-chem-utils.git

or, similarly:

.. code-block:: console

    poetry add git+ssh://git@gitlab.com:ugognw/python-comp-chem-utils.git

Usage
=====

.. admonition:: Example

   Determine whether a water molecule is symmetric with respect to a 180 degree
   rotation about its secondary orientation axis.

    >>> from ase.build import molecule
    >>> from ccu.structure.axisfinder import find_secondary_axis
    >>> from ccu.structure.symmetry import Rotation, RotationSymmetry
    >>> h2o = molecule('H2O')
    >>> axis = find_secondary_axis(h2o)
    >>> r = Rotation(180, axis)
    >>> sym = RotationSymmetry(r)
    >>> sym.check_symmetry(h2o)
    True

.. admonition:: Example

    Retrieve reaction intermediates for the two-electron |CO2| reduction reaction.

    >>> from ccu.adsorption.adsorbates import get_adsorbate
    >>> cooh = get_adsorbate('COOH_CIS')
    >>> cooh.positions
    array([[ 0.        ,  0.        ,  0.        ],
           [ 0.98582255, -0.68771934,  0.        ],
           [ 0.        ,  1.343     ,  0.        ],
           [ 0.93293074,  1.61580804,  0.        ]])
    >>> ocho =  get_adsorbate('OCHO')
    >>> ocho.positions
    array([[ 0.        ,  0.        ,  0.        ],
           [ 1.16307212, -0.6715    ,  0.        ],
           [ 0.        ,  1.343     ,  0.        ],
           [-0.95002987, -0.5485    ,  0.        ]])

.. admonition:: Example

    Place adsorbates on a surface (namely, ``Cu-THQ.traj``) while considering the
    symmetry of the adsorbate and the adsorption sites.

    .. code-block:: console

        ccu adsorption place-adsorbate CO Cu-THQ.traj orientations/

Documentation
=============

View the latest version of the documentation on `Read the Docs`_.


.. |ccu| replace:: ``CompChemUtils``
.. _ccu: https://gitlab.com/ugognw/python-comp-chem-utils/
.. _Python: https://www.python.org
.. |click| replace:: ``click``
.. _click: https://click.palletsprojects.com/en/8.1.x/
.. |numpy| replace:: ``numpy``
.. _numpy: https://numpy.org
.. |scipy| replace:: ``scipy``
.. _scipy: https://scipy.org
.. |ase| replace:: ``ase``
.. _ASE: https://wiki.fysik.dtu.dk/ase/index.html
.. _Read the Docs: https://python-comp-chem-utils.readthedocs.io/en/latest
.. |CO2| replace:: CO\ :sub:`2`
