dqrxfer - Transfer Data Quality reports to central location
===========================================================

.. |date| date::
.. |time| date:: %H:%M

This document was built from version |version|,  |today| at |time|

Introduction
++++++++++++

The DQR file transfer package is a client-server set of programs which use the https
protocol to securely transfer results from remote locations such as LLO, EGO, Kagra ... to
the central location at CIT in order to minimize the time to load these reports by users
of web services.

The package uses Shibboleth authentication and authorization services. During development
all LVK members and robot certificates that can access the web site dqr.ligo.caltech.edu
can push data to the webserver. We may be limiting uploads to specific users and robots
in the future.

Ping
++++

The `dqr-ping` program is used to confirm connectivity and authentication with the server.
It requires a valid Kerberos ticket (TGT) to log in.

.. code::

    (dqr-igwn39) [dqr@LLO-pcdev5:~]$ dqr-ping
    OK
    INFO:dqr-xfer:Login: 1.33, Ping: 0.30, status:200
    OK
    INFO:dqr-xfer:Login: 1.33, Ping: 0.27, status:200
    OK
    INFO:dqr-xfer:Login: 1.33, Ping: 0.27, status:200
    INFO:dqr-xfer:Success = 100.0%
    INFO:dqr-xfer:Elapsed time: 2.7s

If no Kerberos TGT is available the expected error message will start with:

.. code-block::

    klist: No credentials cache found

Upload
++++++

The `dqr-upload` program is used to **push** a single Data Quality Report, or part of one, to
the central server currently at Caltech. In normal operation:

- Each site responds to an igwn-alert or manually creates a report using data local
  to the site.
- These reports can be sent multiple times during the analysis. For example tier 1 results could
  be sent as soon as they are available while other, longer running processes are still
  running.

  - Files may be sent individually to a single [sub]directory or as a tarball which
    may create/fill multiple subdirectories.

- A database is maintained on the DQR machine at Caltech. It contains information on all
  reports stored at CIT. A simple RestFUL interface is used to update the html reports with
  links to each site's report.

.. command-output:: dqr-upload --help

The result is a directory at CIT of the form <graceid>_<remote_site>_<revision> that will
contain all the files needed for this report. The directory will be stored in <graceid>_dir
as defined by the project's configuration.

The arguments are used to determine where to save the file(s) that make up the report:

- Project is used to look up the appropriate task-manager configuration if this is
  the first report for this event. The current options are:
    - replay
    - MDC
    - O4
    - personal - a catch-all for ewrubs with nonstandard configuration
- graceid - specifies the event. It may also be a GPS time to 3 decimal places
- uploader - specifies the site which ran thhew analysis. Current values are llo, lho, virgo, kagra
- revision - an integer specifying the run.
- subdir - a subdirectory of the report. Needed for individual files or tarballs bot rooted
  at the report's top directory.

RESTful API
+++++++++++

The expected use of the DQR database is to allow a report generated at one site to provide
links to related reports generated at other sites.  A simple API allows a web page to query
the database for a list of links in JSON format using Ajax.

We provide a convenience funtion that can be used or a direct query. Both require jQuery.




Use cases
---------

Individual task uploads
.......................

The upload process can be used as an htCondor task that is a child of all jobs for
a specific task. It then creates a tarball of all files that make up the report and
any log or output files of inetrest to developers.

.. code-block::



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
