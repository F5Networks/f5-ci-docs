Statistics
~~~~~~~~~~

.. list-table:: Statistics Parameters (scroll for more)
    :header-rows: 1

    * - Property
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - ``url``
      - string
      - No
      - N/A
      - URL of the backend stats server; if no URL is provided, stats are logged internally
      - N/A
    * - ``token``
      - string
      - No
      - N/A
      - Authentication token for the stats server; required only if using a backend stats server
      - N/A
    * - ``flushInterval``
      - number
      - No
      - 10000
      - Frequency, in milliseconds, at which to flush the stats; applies to both local and backend stats collection
      - N/A
    * - ``backend``
      - string
      - No
      - N/A
      - Type of backend stats service; required only if using a backend stats server
      - 'splunk'
