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
      - Yes
      - N/A
      - URL of the stats service
      - N/A
    * - ``token``
      - string
      - Yes
      - N/A
      - Authentication token for the stats server
      - N/A
    * - ``flushInterval``
      - number
      - No
      - 10000
      - Frequency, in milliseconds, of flushing stats to server
      - N/A
    * - ``backend``
      - string
      - Yes
      - N/A
      - Type of backend stats service
      - 'splunk'

