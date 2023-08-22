DCI Agent Python Framework
==========================

.. sectnum::
.. contents::
   :backlinks: top


About
-----

This is a python framework to write *agents*: An *agent* is a control script
that will drive the execution of programs, specially for the DCI ecosystem.


Runtime Requirements
--------------------

The framework itself tries to have as few dependencies as possible:

* Python 3.6+
* Argparse (part of the python stdlib starting with 3.x)
* `Importlib metadata
  <https://docs.python.org/3/library/importlib.metadata.html>`_ (part of the
  python stdlib starting with 3.8)
* `DCI client libraries<https://pypi.org/project/dciclient/>`_ for interacting
  with the DCI control server


Development
-----------

This tool is written with python 3.6 in mind, as that's what is currently
provided for RHEL 8.4.

For development you will have to create your own virtual environment with
whatever tool you choose, activate it, then install through the
``dev-requirements.txt`` file. You should have a virtual environment with the
package installed and ready to run in editable mode, this means that your
changes should be reflected instantly (unless you rename/move packages around)

Testing automation is done using the `tox automation
framework <https://tox.wiki>`_, so installing it is highly encouraged although
not strictly necessary.

A highly suggested dependency is the `pre-commit
framework<https://pre-commit.com>`_, which will help you speed up the feedback
loop when contributing code. Internally, this will check code style using:

* `python black <https://black.readthedocs.io>`_
* `flake8 <https://flake8.pycqa.org>`_
* `isort <https://pycqa.github.io/isort/>`_
* `pydocstyle <http://www.pydocstyle.org>`_

`PyTest<https://docs.pytest.org>`_ is used for unit testing on top of the
quality of code testing mentioned above.

Development can be done without these tools, but the checks may fail if you
don't follow the appropriate guidelines, it is encouraged to configure your IDE
to make things easier. If you don't have them that's fine, the checks can be
performed either via pre-commit or via tox


Quickstart
^^^^^^^^^^

In order to get you started with development you can:

1. ``sudo dnf install python3-virtualenv tox pre-commit  # install development tools``
2. ``pre-commit install  # install the pre-commit hooks``
3. ``tox  # optionally, run the full test suite``
4. ``virtualenv /tmp/dciagent  # create the virtual environment``
5. ``source /tmp/dciagent/bin/activate  # activate the virtual environment``
6. ``pip install -r dev-requirements.txt  # install in development mode``


Test suite
^^^^^^^^^^

TBD


Writing agents
^^^^^^^^^^^^^^

You can find an example of an agent in ``samples/ansible.py``: the agent will
execute a very simple playbook against your configured hosts as per
``/etc/ansible/hosts`` inventory (or `localhost` if not configured/default).

In order to write an agent you basically need to:

* ``import dciagent.core.agent.<agent>``
* Create your ``Agent`` class inheriting from one of the agent classes
* Scaffold your entrypoint in the way you see fit as long as the entrypoint
  maps to your ``Agent.run()`` method


dci-agent-ctl
-------------

This framework also provides a single entrypoint that can leverage python
`namespace packages
<https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#native-namespace-packages>`_
to auto-discover agents. If you develop your agent and register it in the
``dciagent.agents`` namespace, it should be automatically picked by
``dci-agent-ctl``.

Agents successfully registered in the namespace will appear as sub-commands of
the main entrypoint, you should be able to run them that way. There is an
example command in ``dciagent/agents/example.py`` to showcase a sub-command
registered in the namespace. Using this example, you should be able to run this
like ``dci-agent-ctl example``.
