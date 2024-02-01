Non-Linear Optimization Project
========================

The goal of this project is to characterize, validate and report a model which fits a particular dataset contained
within \\data\\NLData.csv. When opened, it should start with:

``,x,y,z,p,test_name,t
0,-0.006559763109972462,-0.005918879932836453,0.9635245156180181,3.0475756696241545,char_1,2024-02-01 13:41:49.344556``

The dataset is comprised of three Cartesian space vectors ``x``, ``y``, and ``z`` which represent the system input
signals.

The separate vector ``v`` represents a single measured output signal of the system which is proportional in some way to
the input signals ``x``, ``y``, nd ``z``. The structure of how ``v`` relates to ``x``, ``y``, and ``z`` is related to
the objective of this project. Namely, the objective is to characterize the output vector based on the input vectors.

The dataset is broken into three different ``test_name`` labels representing separate trials where the underlying input
signals may have been modified. The labels ``char_1`` and ``char_2`` represents two sets of characterization data while
the label ``val`` represents a validation data set for testing a model derived from the characterization data.

The last vector is ``t`` which represents a timestamp throughout all of the sample data.

Objective
---------------
Derive a model which best fits the independent variables ``x``, ``y``, and ``z`` to the dependent variable ``v``.

Find ``f(x,y,z)`` such that the error ``||v-f(x,y,z)||`` is minimized.

The solution can take many forms, but for convenience consider attempting to solve utilizing:

* Non-Linear Least Squares with a specific function

Where the specific function is of the form:

``f(r,theta,psi,p) = p[0]*r^2 + p[1]*sin(p[3]*theta+p[4])^2 + p[5]*sin(p[6]*psi+p[7])^2``

with ``r``, ``theta``, and ``psi`` being the Spherical coordinate representation of their ``x``, ``y``, and ``z`` Cartesian coordinate counterparts and ``p`` being the solution vector for coefficients/weights applied to the function described above.

Therefore, it will be useful to create some kind of mapping functions to translate the ``x``, ``y``, and ``z`` Cartesian coordinate vectors into their ``r``, ``theta``, and ``psi`` spherical coordinate counterparts.

Constraints
---------------
The project features a module named ``nlop``. Under this module should be four python files, ``__init__.py``, ``core.py``, ``helpers.py`` and
``functions.py``. For organizing code and methods, observer the following guidelines:

* ``__init__.py`` should import the ``PrimarySolver`` class under the ``core.py`` python file to make this class aailable to the ``nlop`` module.

* ``core.py`` is to feature ``PrimarySolver`` class with four methods:
    * ``PrimarySolver.read()`` should import any necessary data from the ``\\data\\NLData.csv`` dataset for future analysis, simulation and visualization
    * ``PrimarySolver.solve()`` should obtain a model ``f(x,y,z)`` which satisfies the primary objective statement
    * ``PrimarySolver.validate()`` should use the model ``f(x,y,z)`` in simulation using the validation portion of the dataset to demonstrate the robustness of the model using untrained data
    * ``PrimarySolver.report()`` should provide any output reports, figures, datasets, or similar which conveys the structure of the solution method/function/algorithm, how well the solution satisfies the objective statement, and a demonstration of the solution using the validation data

* ``helpers.py`` is where any repetitive generic code is to be placed, and this may include but is not limited to:
    * Sanitation methods to clean datasets
    * Data transformation methods which may convert one signal to another, filter a signal, or similar
    * Executing a sequence to obtain a solution vector using characterization data, initial guesses, and any other necessary pre-conditioning
    * Plotting techniques for data visualization
    * Formatting techniques for report writing

* ``functions.py`` is where any mathematical or design functions are to be located such as:
    * Coordinate transformation methods, such as Cartesian to Spherical coordinates
    * Design function ``f(x,y,z,p)`` where ``x``, ``y``, and ``z`` are independent variables to be fitted using a vector of coefficients/weights ``p=[p[0], p[1],...]`` to minimize ``||v-f(x,y,z,p)||``


Any reports generated for analysis, documentation, or similar should be placed under ``\\docs\\``.

Any images generated for analysis, documentation, or similar should be placed under ``\\img\\``.

Any unit tests that are created to aid with development and/or debugging of code under this project should be placed under ``\\tests``.

This example does not dictate the precise structure that needs to be followed, but it is meant to illustrate what types
of code, methods, or functions belong under which file.

Please make sure all code is commented for clarity.

If additional modules or python files are created, please provide clear descriptions of what the files represent and how they fit into the overall project.
Specifically, describe how these additional modules/files fit into the process of reading, analyzing/solving, validating, and/or reporting in reference to the ``\\nlop\\core.py`` module.

**Please make sure to modify** ``requirements.txt`` **with any and all python package dependencies required for submitted project to function correctly.**

What Will be Reviewed
---------------
The quantitative scoring component is based on optimality using a sum of square of residuals of the validation simulation. This will be compared to the reference solution to determine if solution is approximate.

For qualitative scoring, the organization and clarity of code and reports is equally if not more important, so taking any time to comment source code, annotate figures, and generate readable reports will be crucial in conveying how the problem was attempted for better assessing a particular submission.

To this end, it is imperative that someone reading and executing a completed project be able to understand any and all parts of the project, like the classes or functions within a file, how a report is generated, what the solution parameters are, what the error residual is, and any visualizations to help show how the problem was analyzed and solved.

Other
---------------
Submissions of solved project code can be pushed to a user-created cloned fork of this source project with all relevant updates and changes reflected within the fork.

If you want to learn more about this project, visit the `home repository <https://github.com/mikewcallahan/nonLinearOptimizationProject>`_.
