Orchestration
~~~~~~~~~~~~~

.. csv-table:: Orchestration Parameters (scroll for more)
    :header: Property, Sub-Property, Type, Required, Default, Description, Allowed Values

    "``kubernetes``", " ", "JSON object", "Optional", "N/A", "JSON blob defining the kubernetes-specific configurations", "see below"
    " ", "``config-file``", "string", "Required", "N/A", "the configuration file for the `Kubernetes Service`_ the |lwp| should watch", "N/A"
    " ", "``poll-interval``", "integer", "Optional", 1000, "Polling time, in milliseconds", "N/A"
    "``marathon``", " ", "JSON object", "Optional", "N/A", "JSON blob defining the marathon-specific configurations", "see below"
    " ", "``uri``", "string", "Required", "N/A", "Marathon Service URL", "N/A"
    " ", "``poll-interval``", "integer", "Optional", 1000, "Polling time, in milliseconds", "N/A"