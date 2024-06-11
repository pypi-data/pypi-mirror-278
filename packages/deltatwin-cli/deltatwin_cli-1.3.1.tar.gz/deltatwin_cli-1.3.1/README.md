# DeltaTwin service

GAEL Systems is developing a dedicated service, named "DeltaTwin Service" to 
facilitate modelling activities of digital twins. 

It aims to offer a collaborative environment for building and running 
multi-scale and composable workflow, leveraging the numerous 
available data sources, sharing results, and easing interoperability 
with other digital twin standards and system dynamics models.

The DeltaTwin is the central element for the management of workflows, 
resources and their results. They follow a precise structure folder to ensure 
they are handled by the DeltaTwin service.

The service includes the “drive” element in charge of handling DeltaTwin 
storage, their configuration and versionning.   
The “run“ element is in charge of the models executions and their monitoring. 

The DeltaTwin command line allows user to control the management of the 
later modules. It allows user to either work online and perform all actions
in a cloud environment or locally using your computer's resources. 

DeltaTwin service also provides a web application to graphically manages your
Deltatwins and their execution.

# DeltaTwin Command-line

The command line interface allows the user to configure a DeltaTwin and manage its run
operation either from the a shell command prompt or with a script. 

The commands are divided into two main groups: those that allow user to configure and manage
the DeltaTwin’s composition (``deltatwin drive``) and those dedicated to the to the run concept (
``deltatwin run``).  


## Installation

DeltaTwin command-line can be installed using pip:
```
pip install --extra-index-url https://USERNAME:PASSWORD\@repository.gael-systems.com/repository/python-gael/simple deltatwin-cli
```

To get an USERNAME and PASSWORD, please contact the administrator of the DeltaTwin service.




# *Delta* API

Commands are described below. 
These descriptions are also available by using the ``--help`` option on each 
individual command.


| *delta* command |                parameters                 |                                                                                                                                 description |
|-----------------|:-----------------------------------------:|--------------------------------------------------------------------------------------------------------------------------------------------:|
| version         | -all: show all deltatwin components versions. |                                                                                Show DeltaTwin version and check if deltatwin is properly installed. |
| list            |                   None                    |                                                                                                        	List the DeltaTwin from marketplace |
| login           |  -u username -p password  -c conf.ini path                                   |   logs the user to the service, and allows the use of commands, such as ``deltatwin list`` command,that require online registration                                                                                                                                          |

Configured deltatwin information will be stored into $HOME/.delta/config.json 

# *DeltaTwin drive* API

he ``deltatwin drive`` is the command line dedicated to handle DeltaTwin project repository. 
It stores all the configuration, resources, models and sources to run a DeltaTwin and retrieve data.

The DeltaTwin project anatomy can be described with the following empty local representation:



| *deltatwin drive* command |               parameters               |                                                                     description |
|-----------------------|:--------------------------------------:|--------------------------------------------------------------------------------:|
| init                  | <parent_directory>      |              	Create an empty DeltaTwin repository. |
| dependency add        |             <project_url>              |                                       add a dependency to an existing DeltaTwin |
| dependency delete        |             <dependency_name>              |                                       delete a dependency to an existing DeltaTwin |
| dependency list        |                          |                                       delete a dependency to an existing DeltaTwin |
| add-resource          |            	<dependency_name>             |                                               add a resource in this DeltaTwin. |
| check                 | all, dependencies, resources,--verbose | Check that related references are accessible,Details the accessibility problem. |
| fetch                 |                  None                  |                               Download objects and refs from another repository |
| sync                  |       [download [<resource_id>]]       |                         Reload manifest to refresh project resources (no args). |


# *DeltaTwin run* API

DeltaTwin run module uses models stored into DeltaTwin repository. 
The objective of this service is to allow edition and run of the models stored into the DeltaTwin.
The run can be done remotely and locally when possible.
Run results shall be stored into the artifact folder of the deltatwin drive environment. 

| *deltatwin run* command   |       parameters        |                                                       description |
|-----------------------|:-----------------------:|------------------------------------------------------------------:|
| start                 |          model          | Start the DeltaTwin execution with the expected DeltaTwins inputs |
| stop                  |          model          |                                      Stop the DeltaTwin execution |
| resume                |          None           |                           Resume a model execution (if supported) |
| process/configuration |          None           |                                          Manage run configuration |
| get                   |     twin_id, run_id     |                               Show information about an execution |
| list                  |   twin_id, owner, ...   |                                  Show list of execution for model |
| download              | twin_id, run_id, output |                                      Download an output execution |

Configured deltatwin information will be stored into $HOME/.delta/config.json 


# *DeltaTwin artifact* API

DeltaTwin artifact allows to store an output of an execution into the repository Delta

| *deltatwin artifact* command |        parameters         |                          description |
|------------------------------|:-------------------------:|-------------------------------------:|
| add                          | run_id, output, name, ... |          Create a DeltaTwin artifact |
| list                         |                           |    Show list of artifact for a model |
| get                          |        artifact_id        | get or download a DeltaTwin artifact |
| delete                       |        artifact_id        |          Delete a DeltaTwin artifact |

