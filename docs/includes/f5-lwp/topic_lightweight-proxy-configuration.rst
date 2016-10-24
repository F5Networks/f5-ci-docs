Overview
````````

You can configure |lwp| using valid JSON config file; this can be passed in as a ``--config-file`` option or set as an environment variable (``LWP_CONFIG``), as shown in :ref:`How to Run |lwp|`.

The |lwp| config file must contain the following sections:

-  :ref:`Global <#>`: global configurations that are not specific to an orchestration environment.
-  :ref:`Orchestration <#>`: contains parameters that allow you to specify your orchestration environment
-  :ref:`Stats <#>`: contains parameters for statistics gathering and reporting.
-  :ref:`Virtual servers <#>`: contains parameters that specify list(s) of virtual server objects representing service endpoints.


