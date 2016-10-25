Virtual Server Section
~~~~~~~~~~~~~~~~~~~~~~

.. note:: Items marked with an asterisk (*) can be used in a :ref:`Kubernetes service annotation <add-lwp-kubernetes-services>`.

.. list-table:: Virtual Server Configuration Parameters
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - ``destination``
      - number
      - Yes
      - N/A
      - Service port on which this virtual server accepts connections.
      - N/A
    * - ``service-name``
      - string
      - Yes
      - N/A
      - Marathon Application tag for the app the virtual server is proxying (used to dynamically discover services)
      - N/A
    * - ``ip-protocol`` *
      - string
      - No
      - 'http'
      - The virtual server's service type
      - 'http', 'tcp'
    * - ``load-balancing-mode`` *
      - string
      - No
      - 'round-robin'
      - Load balancing algorithm to use for the virtual server
      - 'round-robin'
    * - ``keep-alive-msecs``
      - number
      - No
      - 1000
      - Time (in milliseconds) between TCP keep-alive packets on socket to back-end server
      - N/A
    * - ``flags`` *
      - JSON object
      - No
      - N/A
      - See :ref:`Virtual Server flags <lwp-configs-virtual-server-flags>`.
      - N/A

.. _lwp-configs-virtual-server-flags:

Flags
*****

.. list-table:: Virtual Server Flags Configuration Parameters
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - ``x-forwarded-for`` *
      - boolean
      - No
      - false
      - Flag to set 'x-forwarded-for' header in request to backend server.
      - N/A
    * - ``x-served-by`` *
      - boolean
      - No
      - false
      - Flag to set 'x-served-by' header in response to client.
      - N/A


:ref:`Kubernetes service annotation <add-lwp-kubernetes-services>`