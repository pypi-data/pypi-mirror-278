DeltaTwin run module uses models stored into DeltaTwin component repository.
The objective of this service is to allow edition and run of the models stored into the DeltaTwin component.
The run can be done remotely and locally when possible.
Run results shall be stored into the artifact folder of the DeltaTwin drive environment.

______________________________________________

.. click:: delta.cli.run.configuration:configuration
   :prog: deltatwin run configuration
   :nested: full

.. code-block:: console

    deltatwin run configuration [TBD]

______________________________________________

.. click:: delta.cli.run.resume:resume
   :prog: deltatwin run resume
   :nested: full

.. code-block:: console

    deltatwin run resume [TBD]

______________________________________________

.. click:: delta.cli.run.start:start
   :prog: deltatwin run start
   :nested: full

.. code-block:: console

    deltatwin run start <DELTATWIN_NAME> -i image "http://img/\\$value" -i angle 45

______________________________________________

.. click:: delta.cli.run.local:run_local
   :prog: deltatwin run run_local
   :nested: full

.. code-block:: console

    deltatwin run start_local <DELTATWIN_NAME> -i image "http://img/\\$value" -i angle 45

______________________________________________

.. click:: delta.cli.run.list:list_deltatwin_executions
   :prog: deltatwin run list
   :nested: full

.. code-block:: console

    deltatwin run list <DELTATWIN_NAME>

______________________________________________

.. click:: delta.cli.run.get:get_deltatwin_execution
   :prog: deltatwin run get
   :nested: full

.. code-block:: console

    deltatwin run get <RUN_ID>

______________________________________________

.. click:: delta.cli.run.delete:delete_deltatwin_execution
   :prog: deltatwin run delete
   :nested: full

.. code-block:: console

    deltatwin run delete <RUN_ID>