Sphere-ob Airborne EM modelling 
====

Sphere-ob (sphere-overburden) is a python program developed to calculate and plot the airborne TDEM response of a sphere or ‘dipping sphere’ underlying conductive overburden. 
The response is calculated using the semi-analytic solution set presented in Desmerais & Smith (2016), this solution set is computationally efficient and allows the user to model a thin sheet in addition to a sphere, by artificially restricting current flow to parallel planes within an anisotropic sphere.

Installation
====

If python is installed on your system, Sphereob can be installed with pip + git by opening command prompt in administrator and using::

	pip install git+https://github.com/anonseg2023/sphereob

Alternatively, the repository can be manually downloaded and installed using the install script, i.e., by navigating to the SPHERE-OB folder, opening a python / anaconda prompt in administrator and running::

	python setup.py install


Dependencies
====

* matplotlib
* numpy
* scipy
* pyqt5
* pandas

Installing SPHERE-OB through pip + git will result in these libraries being installed in your current python environment.

Getting Started
====

Once installed, the GUI can be launched from the command line as::

	sphereob

The program will launch and the user can now begin plotting airborne EM responses for varying survey configurations and geologic models.

Documentation
====

Documentation, including explanations of the model parameters and data importers is included in SPHERE-OB.pdf
