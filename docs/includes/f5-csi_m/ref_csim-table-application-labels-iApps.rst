
.. table:: iApp Application Labels

    ====================================    =================================================================   =======================================================================
    Field                                   Definition                                                          Additional Information
    ====================================    =================================================================   =======================================================================
    \F5_{n}_IAPP_TEMPLATE                   The iApp template to create the Application Service                 | Example: ``"F5_0_IAPP_TEMPLATE": "/Common/f5.http"``
    ------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
    \F5_{n}_IAPP_OPTION_*                   Defines configuration options for the service                       | Example: ``"F5_0_IAPP_OPTION_description": "This is a test iApp"``
    ------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
    \F5_{n}_IAPP_VARIABLE_*                 Defines the variables needed by the iApp to create the service      | * Use an existing resource, or
                                                                                                                | * tell the service to create a new one using ``#create_new#``.
                                                                                                                | Example: ``"F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240"``
                                                                                                                | Example: ``"F5_0_IAPP_VARIABLE_pool__pool_to_use": "#create_new#"``
    ------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
    \F5_{n}_IAPP_POOL_MEMBER_TABLE_NAME     The name of the iApp table entry that specifies the pool members    | * Can be different for each iApp template.
                                                                                                                | Example: ``"F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members"``
    ====================================    =================================================================   =======================================================================

