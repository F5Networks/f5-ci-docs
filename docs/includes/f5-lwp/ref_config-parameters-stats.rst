Stats Section
~~~~~~~~~~~~~

.. list-table:: Stats Configuration Parameters
    header-rows: 1

    * - Field
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
      - Frequency in milliseconds of flushing stats to server
      - N/A
    * - ``backend``
      - string
      - Yes
      - N/A
      - Type of backend stats service
      - 'leo', 'splunk'

