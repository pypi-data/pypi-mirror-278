The ``deltatwin drive`` is the command line dedicated to handle DeltaTwin project repository.
It stores all the configuration, resources, models and sources to run a DeltaTwin component and retrieve data.

The DeltaTwin component anatomy can be described with the following empty local representation:

::

    my_project
    ├─── manifest.json
    ├─── artifacts/
    ├─── models/
    ├─── resources/
    ├─── sources/
    └─── workflow.yml/


---------------------------------

.. click:: delta.cli.drive.init:init
   :prog: deltatwin drive init
   :nested: full

**Examples:**

For example, you can create a new DeltaTwin called *ndvi* with the following command:

.. code-block:: console

    deltatwin drive init /home/user/desktop/ndvi

This command will create the basic files of a DeltaTwin component, in a folder called *ndvi*.

.. code-block:: console

    INFO:Delta:New commit : 076f911d678a97038bf83d873c8d94797341ef65 master
    INFO:Delta:Twin has been initialized at /home/user/desktop/ndvi
    INFO: DeltaTwin ndvi created


---------------------------------


.. click:: delta.cli.drive.check:check
   :prog: deltatwin drive check
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive check http://dt_repository.com/dt_to_add

This command will check if the DeltaTwin component which is indicated
in the url is accessible.

This command is not yet implemented.

---------------------------------


.. click:: delta.cli.drive.build:build
   :prog: deltatwin drive build
   :nested: full

**Examples:**

.. code-block:: console

    delta drive build -t <tag name>

This command will build a (Docker) image of your DeltaTwin component.

---------------------------------


.. click:: delta.cli.drive.publish:publish_dt
   :prog: deltatwin drive publish
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive publish  <version name>
    deltatwin drive publish -d <DeltaTwin name> <version name>

This command will publish your DeltaTwin component to the DeltaTwin platform.
But you can also publish a new version of your DeltaTwin.
**Note:** If you have already pushed your DeltaTwin, please use the second command.


===========
Dependency
===========

.. click:: delta.cli.drive.dependency.add:add_dependency
   :prog: deltatwin drive dependency add
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive dependency add demo-rotate-python [TDB]

This command will add the dependency to the working DeltaTwin component.

---------------------------------

.. click:: delta.cli.drive.dependency.delete:delete_dependency
   :prog: deltatwin drive dependency delete
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive dependency delete demo-rotate-python [TBD]

This command will remove the dependency of the working DeltaTwin component.

---------------------------------

.. click:: delta.cli.drive.dependency.list:list_dependency
   :prog: deltatwin drive dependency list
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive dependency list [TBD]

List all the dependencies from the manifest.json of the
working DeltaTwin component.

---------------------------------

===========
Resource
===========

.. click:: delta.cli.drive.resource.add:add_resource
   :prog: deltatwin drive resource add
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource add /path/to/resource Sentinel1.zip

Will add the resource given in argument, to the resources of the
working DeltaTwin component.
If given the option *--download*, it will download the resource and
put it in the resources folder.
This command will add the entry to *manifest.json*.

---------------------------------

.. click:: delta.cli.drive.resource.delete:delete_resource
   :prog: deltatwin drive resource delete
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource delete Sentinel1.zip

This command will remove the entry from the *manifest.json*.

---------------------------------

.. click:: delta.cli.drive.resource.list:list_resource
   :prog: deltatwin drive resource list
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource list

List all the resources from the *manifest.json* of the
working DeltaTwin component.

______________________________________________

.. click:: delta.cli.drive.resource.sync:sync
   :prog: deltatwin drive resource sync
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive sync

This command will reload the *manifest.json*, to update all the resources
with the last manifest load.

.. code-block:: console

    INFO:Delta:Fetching https://catalogue.dataspace.copernicus.eu/odata/v1/Products(UUID)...
    INFO:Delta:https://catalogue.dataspace.copernicus.eu/odata/v1/Products(UUID) has been fetched.

______________________________________________

==========
Artifact
==========

DeltaTwin artifact stores output Data of DeltaTwin component executions.

______________________________________________

.. click:: delta.cli.drive.artifact.add:add_artifact
   :prog: deltatwin drive artifact add
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.list:list_artifact
   :prog: deltatwin drive artifact list
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.get:get_artifact
   :prog: deltatwin drive artifact get
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.delete:delete_artifact
   :prog: deltatwin drive artifact delete
   :nested: full
