Orchestration section
~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Orchestration Configuration Parameters
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - kubernetes
      - JSON object
      - No
      - N/A
      - Kubernetes specific configs
      - see :ref:`Kubernetes configs <lwp-orchestration-configs-kubernetes>`
    * - marathon
      - JSON object
      - No
      - N/A
      - Marathon specific configs
      - see :ref:`Marathon configs <lwp-orchestration-configs-marathon>`



.. _lwp-orchestration-configs-kubernetes:

Kubernetes
^^^^^^^^^^

.. list-table:: Orchestration Configuration Parameters - Kubernetes
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - config-file
      - string
      - Yes
      - N/A
      - Service config file to watch
      - N/A
    * - poll-interval
      - number
      - No
      - 1000
      - Polling time in milliseconds
      - N/A



.. _lwp-orchestration-configs-marathon:

Marathon
^^^^^^^^

.. list-table:: Orchestration Configuration Parameters - Marathon
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - uri
      - string
      - Yes
      - N/A
      - URL of the Marathon service
      - N/A
    * - poll-interval
      - number
      - No
      - 1000
      - Polling time in milliseconds
      - N/A

