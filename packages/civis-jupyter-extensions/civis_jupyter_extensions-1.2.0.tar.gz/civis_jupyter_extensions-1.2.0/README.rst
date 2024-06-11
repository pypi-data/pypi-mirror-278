civis-jupyter-extensions
========================

.. image:: https://circleci.com/gh/civisanalytics/civis-jupyter-extensions.svg?style=shield
   :target: https://circleci.com/gh/civisanalytics/civis-jupyter-extensions
   :alt: CircleCI build status

.. image:: https://img.shields.io/pypi/v/civis-jupyter-extensions.svg
   :target: https://pypi.org/project/civis-jupyter-extensions/
   :alt: Latest version on PyPI

Tools for using the Civis Platform with Jupyter notebooks

Installation and Setup
----------------------

Run the following commands in a shell::

    pip install civis-jupyter-extensions
    jupyter nbextension install --py civis_jupyter_ext
    jupyter nbextension enable --py civis_jupyter_ext

In order to use the extensions, make sure to have your Civis Platform API key in
your local environment as `CIVIS_API_KEY`.

Magic Commands
--------------

To load the magic commands, use the following in ipython or a
Jupyter notebook::

    %load_ext civis_jupyter_ext

You can also autoload the magic commands every time a notebook is opened by
adding::

    c.InteractiveShellApp.extensions = ['civis_jupyter_ext']

to your ``~/.ipython/profile_default/ipython_config.py``.

SQL Queries
~~~~~~~~~~~

To get a table preview, use the cell magic like this::

    %%civisquery my-database
    select * from dummy.table limit 10;

To return a DataFrame for further processing, use the line magic like this::

    df = %civisquery my-database; select * from dummy.table;
