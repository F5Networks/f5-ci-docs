Virtual Server
~~~~~~~~~~~~~~

.. csv-table:: Virtual Server Parameters (scroll for more)
    :header: Property, Sub-Property, Type, Required, Default, Description, Allowed Values

    ``destination``, " ", "number", "Required", "N/A", "Service port on which this virtual server accepts connections", "N/A"
    ``service-name``, " ", "string", "Required", "N/A", "Marathon Application tag for the app the virtual server is proxying (used to dynamically discover services)", "N/A"
    ``ip-protocol`` [#k8svs]_, " ", "string", "Optional", "'http'", "The virtual server's service type", "'http'", "'tcp'"
    ``load-balancing-mode`` [#k8svs]_, " ", "string", "Optional", "'round-robin'", "Load balancing algorithm to use for the virtual server", "'round-robin'"
    ``keep-alive-msecs`` [#k8svs]_, " ", "integer", "Optional", "1000", "Time (in milliseconds) between TCP keep-alive packets on socket to back-end server", "N/A"
    ``flags`` [#k8svs]_, " ", "JSON object", "Optional", "N/A", "see below", "N/A"
    " ", ``x-forwarded-for`` [#k8svs]_, "boolean", "Optional", "false", "Flag to set 'x-forwarded-for' header in request to backend server", "N/A"
    " ", ``x-served-by`` [#k8svs]_, "boolean", "Optional", "false", "Flag to set 'x-served-by' header in response to client", "N/A"


.. [#k8svs] These items can be used in a :ref:`Kubernetes service annotation <add-lwp-kubernetes-services>`.


