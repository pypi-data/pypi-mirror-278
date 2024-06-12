==================================
 RsCmwNrFr1Meas
==================================

.. image:: https://img.shields.io/pypi/v/RsCmwNrFr1Meas.svg
   :target: https://pypi.org/project/ RsCmwNrFr1Meas/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsCmwNrFr1Meas.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsCmwNrFr1Meas.svg
   :target: https://pypi.python.org/pypi/RsCmwNrFr1Meas/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsCmwNrFr1Meas.svg
   :target: https://pypi.python.org/pypi/RsCmwNrFr1Meas/

Rohde & Schwarz CMW New Radio FR1 Measurement RsCmwNrFr1Meas instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsCmwNrFr1Meas import *

    instr = RsCmwNrFr1Meas('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: CMW500, CMW100

The package is hosted here: https://pypi.org/project/RsCmwNrFr1Meas/

Documentation: https://RsCmwNrFr1Meas.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

Release Notes:

Latest release notes summary: First released version

	Version 3.8.41
		- First released version for FW 3.8.41
