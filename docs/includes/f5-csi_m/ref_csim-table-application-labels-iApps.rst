.. list-table:: iApp Application Labels
    :header-rows: 1

    * - Label
      - Definition
      - Additional Information
    * - ``F5_{n}_IAPP_TEMPLATE``
      - The iApp template to use to create the Application Service
      - Example: ``"F5_0_IAPP_TEMPLATE": "/Common/f5.http"``
    * - ``F5_{n}_IAPP_OPTION_*``
      - Configuration options to apply to the Application Service
      - ``"F5_0_IAPP_OPTION_description": "This is a test iApp"``
    * - ``F5_{n}_IAPP_VARIABLE_*``
      - Defines the variables the iApp needs to create the Service
      - Use an existing resource, or tell the service to create a new one using ``#create_new#``.
        | Example: ``"F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240"``
        | Example: ``"F5_0_IAPP_VARIABLE_pool__pool_to_use": "#create_new#"``
    * - ``F5_{n}_IAPP_POOL_MEMBER_TABLE_NAME``
      - The iApp table entry that specifies the pool members
      - Can be different for each iApp template.
        | Example: ``"F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members"``



