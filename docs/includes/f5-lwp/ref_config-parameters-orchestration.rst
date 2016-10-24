Orchestration section
^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Orchestration Configuration Parameters
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - marathon
      - JSON object
      - No
      - N/A
      - Marathon specific configs
      - see :ref:`Marathon configs <Orchestration section \ marathon>`
    * - kubernetes
      - JSON object
      - No
      - N/A
      - Kubernetes specific configs
      - see :ref:`Kubernetes configs <Orchestration section \ kubernetes>`


Marathon
********

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


Kubernetes
**********

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

