PXE Manager
===========

The idea is to build an automaton to control when to boot from the
local drives and when to boot from the network.

The system can be used to run automated tests. You can also use this
system only to provision on demand systems or backup your partitions
using partimage or anything you want to do with an automated PXE
system...


Concepts
--------
PXE Manager (pxemngr) manage a list of registered nodes and point them to the proper
PXElinux boot configuration.

Every boot configuration is named a `profile` and located in the ``<tftp_root_dir>/pxelinux.cfg/profiles/``

Nodes's profile can be choosen via a cli or web interface.

Requirements
-------------
- Django on the server.
- The controlled systems must be configured to always boot over PXE.

How to install PXE Manager ?
----------------------------

- edit the database and PXE config in ``settings.py`` according to
  your local setup.

- you need ``python-django`` installed.

- run ``./manage.py syncdb`` to create the needed sql tables.

- export these 2 environment variables.

::

  DJANGO_SETTINGS_MODULE=pxemngr.settings and PYTHONPATH=$PWD.

- To get the service alive, run ``./manage.py runserver <ip addr>:<port>`` to have a web server
  waiting for requests to boot locally or you can also configure django
  to use apache instead of the little embedded server.

Usage:
------

How to create a new profile ?
+++++++++++++++++++++++++++++
- create the PXE profiles in ``pxelinux.cfg/profiles/`` ending in
  ``.prof``. The local.prof is mandatory and must point to a local boot
  config. The user running the scripts must have the right to write in
  pxelinux.cfg. I usually create a group and put it under control of
  the files under pxelinux.cfg.

- run ``pxemngr syncbootnames`` to add the names of the PXE profiles in the
  database.


How to register a new node ?
++++++++++++++++++++++++++++
- add the systems that you want to control by this system like this

::

 pxemngr addsystem <name> <mac address> [<mac address 2>...]


How to select the profile to boot for a particular node ?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
- set which profile you want your system to PXE boot

::

 pxemngr nextboot <node_name> <profile_name>


It is also possible to trigger a change by using a simple HTTP GET on the
following url :

   - from any node : ``http://<ip_addr>:<port>/nextboot/<node_name>/<profile_name>``



   - from the node itself :  ``http://<ip_addr>:<port>/<profile_name>/``

   - examples:

::

  curl http://172.21.0.50:83/nextboot/mira062/centos72
  curl http://172.21.0.50:83/centos72/

If you want to assign a default profile to all systems, use the
reserved system name 'default'.

::

  pxemngr nextboot default <profile_name>
  curl http://172.21.0.50:83/nextboot/default/centos72


How can I know the current profile for a node ?
+++++++++++++++++++++++++++++++++++++++++++++++

It is possible to find the current profile of a node from :

  - from the node itself : ``http://<ip_addr>:<port>/profile/``
  - any node : ``http://<ip_addr>:<port>/profile/<mac_address_of_node>``
  - example: ``wget -qO- http://172.21.0.50:83/profile/00:25:90:03:b6:e8``


How can I get the history of a node ?
+++++++++++++++++++++++++++++++++++++

- Connect your browser to ``http://<ip_addr>:<port>``
- Select a node from the list
- Output looks like :

::

 Test reports
 System info
 Name	mira062
 Last 10 PXE requests

    July 6, 2016, 12:22 a.m. local
    July 6, 2016, 12:15 a.m. centos72
    July 5, 2016, 11:23 p.m. local
    July 5, 2016, 11:23 p.m. deploy
    July 4, 2016, 2:31 p.m. centos72
    July 4, 2016, 12:18 p.m. local
    July 4, 2016, 12:12 p.m. centos72
    July 4, 2016, 11:57 a.m. local
    July 4, 2016, 11:52 a.m. centos72
    July 4, 2016, 11:41 a.m. local

 Tests



Test system
-----------

Description
+++++++++++

The test system allows to provide test scripts to running systems
declared in the PXE manager database.

The target system can request a test by using this url:
``http://<ipaddr>:<port>/nexttest/``

The tests are usually shell scripts that are built using Django
templating system. By convention, the tests are usinf a suffix of
.test. They are stored in the directory set in settings.py under the
TESTS_DIR variable. A wait.test must exist and will be sent by the
server to the target system when no test is available. This wait.test
must wait for some time and then exit to let the system send a new
test if needed or send back a new wait.test.

After the execution of a test script, the result is sent back to the
server using the following url: ``http://<ipaddr>:<port>/upload/<test id>/``. I
usualy run the following curl command to upload the result::

 curl --retry 0 -s -f -F "file=@$output" http://<ipaddr>:<port>/upload/<test id>/

These uploaded files are stored under the directory set by the
``TEST_UPLOAD_DIR`` variable in settings.py.

The system uses a simple convention in these files to lookup
information. It parses the lines to store informations, warnings and
errors lines if they begin by 'I: ', 'W: ' and 'E: '. The system also
tries to find the version of the system by looking for a line starting
by 'V: '.

You can then navigate on web pages displaying these parsed
informations under: ``http://<ipaddr>:<port>/``.

Control
+++++++

To instruct the system about which tests are available, use the
following command::

 pxemngr synctestnames

To assign a test to a target system, use the following command::

 pxemngr nexttest <system name> <test name>

To display all the tests scheduled for a system, use::

 pxemngr dpytest <system name>

Web navigation
++++++++++++++

By pointing your browser to ``http://<ipaddr>:<port>/``, you can navigate
in the results of the test system.
