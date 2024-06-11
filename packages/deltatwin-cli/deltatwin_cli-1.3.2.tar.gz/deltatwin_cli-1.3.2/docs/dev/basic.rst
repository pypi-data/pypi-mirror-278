.. click:: delta.cli:delta_login
   :prog: deltatwin login
   :nested: full

All connection information is stored in a conf.ini file.
The path to this file can be set by the user.

.. code-block:: console

    deltatwin login username password -a http://delta-api.com

This command will log in to the service with the api given in argument.
To set the service you want to query, you can either use *--api*,
or set the path to your configuration file *--conf*. If no path is
given, the *conf.ini* is saved in the *.delta* folder in your
home directory.

.. code-block:: console

    INFO: Login to the service token saved in /home/jiloop/.deltatwin/conf.ini

When log, all the connection information will be stored into a configuration file (conf.ini),
it will contain the token, and the api url, all the information mandatory to interact with,
the deltatwin services.

When this file is created to log again, you can do so by using the command

.. code-block:: console

    deltatwin login

It will find all the connection information into the configuration file.

---------------------------------

.. click:: delta.cli:version
   :prog: deltatwin version
   :nested: full

.. code-block:: console

    deltatwin version

Prints the DeltaTwin command line version currently used.

.. code-block:: console

    DeltaTwin CLI version : 1.2.0

.. code-block:: console

    deltatwin version --all

Prints the DeltaTwin command line version and the core version installed.

.. code-block:: console

    DeltaTwin CLI version : 1.3.0
    DeltaTwin CORE version : 1.1.0

---------------------------------

.. click:: delta.cli:list_deltatwins
   :prog: deltatwin list
   :nested: full

.. code-block:: console

    deltatwin list

This command will list the DeltaTwin components visible to the user,
it includes, the user's DeltaTwin components, all the DeltaTwin components of the
Starter Kit and all the published DeltaTwins
with public visibility.
By default the information's will be display as an array, these information can also
be retrieve as a json.

.. code-block:: console

    deltatwin list --format-output json

This command will list the DeltaTwin components of the user.
Before using this command the user must be logged in,
using the *delta* *login* command.

.. code-block:: console

    [
        {
            "name": "Deltatwin1",
            "description": "Description of the Deltatwin1",
            "creation_date": "2024-02-21T13:16:47.548Z",
            "license": "LGPLv3",
            "topics": [
                "starter-kit",
                "sentinel-2",
                "optical",
                "color-composition"
            ],
            "author": "delta-user"
        },
        {
            "name": "Deltatwin2",
            "description": "Description of the Deltatwin2",
            "creation_date": "2024-02-21T13:16:47.548Z",
            "license": "LGPLv3",
            "topics": [
                "starter-kit",
                "sentinel-2",
                "optical",
                "color-composition"
            ],
            "author": "delta-user"
        }
    ]

---------------------------------


.. click:: delta.cli:get_deltatwin_info
   :prog: deltatwin get
   :nested: full

.. code-block:: console

    deltatwin get dt_name -f json

This command will show the information of a DeltaTwin component,
before using this command the user must be logged in,
using the *delta* *login* command.

.. code-block:: console

    {
        "name": "Deltatwin2",
        "description": "Description of the Deltatwin2",
        "publication_date": "2024-03-07T12:50:55.055721Z",
        "topics": [
            "starter-kit",
            "sentinel-2",
            "optical",
            "color-composition"
        ],
        "version": "1.1.0",
        "available_version": [
            "1.1.0",
            "1.0.1",
            "1.0.0"
        ],
        "author": "delta-user",
        "inputs": [],
        "outputs": []
    }
