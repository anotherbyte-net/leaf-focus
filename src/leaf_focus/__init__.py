"""Documentation for the leaf focus package.

.. include:: ../../README.md
.. include:: ../../CHANGELOG.md
"""

# from beartype import BeartypeConf
# from beartype.claw import beartype_all, beartype_this_package
# beartype_all(conf=BeartypeConf(violation_type=UserWarning))

from beartype.claw import beartype_this_package


beartype_this_package()
