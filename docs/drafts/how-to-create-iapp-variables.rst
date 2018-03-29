.. _create-iapp-variables:

How to Create iApp Variables
============================

The |kctlr-long| and |mctlr-long| both support deployment of iApps, which gives them access to essentially all the advanced l4-l7 features on BIG-IP. To deploy an iApp, you need to create custom ``iappVariables`` key-value pairs; these provide the information the iApp needs to configure the BIG-IP.

.. important::

    The instructions provided here for determining which iApp variables to create apply to all supported orchestration environments. In the examples, we reference Marathon and the |mctlr-long|.

At a high level, the way it works is:

1) You define a new Application in Marathon, with the :ref:`marathon-bigip-ctlr iApp Application labels for iApp mode </products/connectors/marathon-bigip-ctlr/latest/index.html#application-labels-for-iapp-mode>` defined.
2) The |mctlr-long| notices the new labels and configures a new iApp on the BIG-IP.
3) The iApp template is invoked to handle the new iApp the |mctlr| defined. The iApp template can create a virtual server, pool members, and so on. 

First, you need to determine what fields in the iApp template need corresponding ``iappVariables``.

#. `Deploy an iApp <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-iapps-developer-11-4-0/2.html#unique_1831084015>`_ using the BIG-IP configuration utility.

#. Make a REST call to the BIG-IP to determine the configurations applied.


.. rubric:: For example:
 
Here's the JSON for an example application configured in Marathon

.. code-block:: json
    :linenos:
    :emphasize-lines:
         
        {
           "app" : {
              "instances" : 2,
              "acceptedResourceRoles" : null,
              "tasksStaged" : 0,
              "env" : {},
              "container" : {
                 "type" : "DOCKER",
                 "docker" : {
                    "privileged" : false,
                    "forcePullImage" : true,
                    "portMappings" : [
                       {
                          "containerPort" : 80,
                          "hostPort" : 0,
                          "servicePort" : 10001,
                          "protocol" : "tcp"
                       }
                    ],
                    "network" : "BRIDGE",
                    "image" : "nginx",
                    "parameters" : []
                 },
                 "volumes" : []
              },
              "maxLaunchDelaySeconds" : 3600,
              "executor" : "",
              "tasksRunning" : 2,
              "healthChecks" : [
                 {
                    "gracePeriodSeconds" : 10,
                    "maxConsecutiveFailures" : 3,
                    "protocol" : "TCP",
                    "timeoutSeconds" : 5,
                    "ignoreHttp1xx" : false,
                    "portIndex" : 0,
                    "intervalSeconds" : 5
                 }
              ],
              "backoffSeconds" : 1,
              "tasksHealthy" : 2,
              "disk" : 0,
              "requirePorts" : false,
              "mem" : 32,
              "ports" : [
                 10001
              ],
              "uris" : [],
              "dependencies" : [],
              "cpus" : 0.1,
              "user" : null,
              "constraints" : [],
              "id" : "/test-svc",
              "versionInfo" : {
                 "lastScalingAt" : "2017-02-03T23:06:03.940Z",
                 "lastConfigChangeAt" : "2017-02-03T23:05:38.429Z"
              },
              "deployments" : [],
              "tasks" : [
                 {
                    "appId" : "/test-svc",
                    "startedAt" : "2017-02-03T23:05:55.329Z",
                    "id" : "test-svc.470699a1-ea65-11e6-b367-fa163ef52e22",
                    "healthCheckResults" : [
                       {
                          "consecutiveFailures" : 0,
                          "taskId" : "test-svc.470699a1-ea65-11e6-b367-fa163ef52e22",
                          "alive" : true,
                          "firstSuccess" : "2017-02-03T23:05:58.639Z",
                          "lastFailure" : null,
                          "lastSuccess" : "2017-02-03T23:20:15.793Z"
                       }
                    ],
                    "ipAddresses" : [],
                    "host" : "172.16.1.21",
                    "stagedAt" : "2017-02-03T23:05:38.575Z",
                    "ports" : [
                       13122
                    ],
                    "slaveId" : "4b371649-4dd7-43bd-bb8c-516f66d34f40-S0",
                    "version" : "2017-02-03T23:05:38.429Z"
                 },
                 {
                    "host" : "172.16.1.21",
                    "healthCheckResults" : [
                       {
                          "consecutiveFailures" : 0,
                          "firstSuccess" : "2017-02-03T23:06:29.144Z",
                          "lastFailure" : null,
                          "lastSuccess" : "2017-02-03T23:20:16.154Z",
                          "alive" : true,
                          "taskId" : "test-svc.56399762-ea65-11e6-b367-fa163ef52e22"
                       }
                    ],
                    "ipAddresses" : [],
                    "stagedAt" : "2017-02-03T23:06:04.060Z",
                    "id" : "test-svc.56399762-ea65-11e6-b367-fa163ef52e22",
                    "startedAt" : "2017-02-03T23:06:25.485Z",
                    "appId" : "/test-svc",
                    "version" : "2017-02-03T23:06:03.940Z",
                    "ports" : [
                       16324
                    ],
                    "slaveId" : "4b371649-4dd7-43bd-bb8c-516f66d34f40-S0"
                 }
              ],
              "args" : null,
              "cmd" : null,
              "tasksUnhealthy" : 0,
              "storeUrls" : [],
              "version" : "2017-02-03T23:06:03.940Z",
              "labels" : {
                 "F5_0_IAPP_VARIABLE_pool__addr" : "172.16.3.2",
                 "F5_0_IAPP_VARIABLE_monitor__monitor" : "/#create_new#",
                 "F5_0_IAPP_TEMPLATE" : "/Common/f5.http",
                 "F5_0_IAPP_OPTION_description" : "This is a test iApp",
                 "F5_0_IAPP_VARIABLE_net__server_mode" : "lan",
                 "F5_0_IAPP_VARIABLE_pool__mask" : "255.255.255.255",
                 "F5_0_IAPP_VARIABLE_client__standard_caching_with_wa" : "/#create_new#",
                 "F5_0_IAPP_VARIABLE_net__vlan_mode" : "all",
                 "F5_0_IAPP_VARIABLE_pool__lb_method" : "round-robin",
                 "F5_0_IAPP_VARIABLE_net__snat_type" : "automap",
                 "F5_0_IAPP_VARIABLE_client__tcp_wan_opt" : "/#create_new#",
                 "F5_0_IAPP_VARIABLE_pool__persist" : "/#do_not_use#",
                 "F5_0_IAPP_VARIABLE_server__tcp_lan_opt" : "/#create_new#",
                 "F5_0_IAPP_VARIABLE_server__ntlm" : "/#do_not_use#",
                 "F5_0_IAPP_VARIABLE_monitor__uri" : "/",
                 "F5_0_IAPP_VARIABLE_server__oneconnect" : "/#create_new#",
                 "F5_0_IAPP_VARIABLE_monitor__response" : "none",
                 "F5_0_IAPP_VARIABLE_net__client_mode" : "wan",
                 "F5_0_IAPP_VARIABLE_ssl_encryption_questions__advanced" : "yes",
                 "F5_0_IAPP_VARIABLE_pool__port" : "8080",
                 "F5_0_IAPP_VARIABLE_pool__pool_to_use" : "/#create_new#",
                 "F5_0_IAPP_VARIABLE_pool__http" : "/#create_new#",
                 "F5_0_IAPP_POOL_MEMBER_TABLE_NAME" : "pool__members",
                 "F5_0_IAPP_VARIABLE_monitor__frequency" : "30",
                 "F5_PARTITION" : "test",
                 "F5_0_IAPP_VARIABLE_client__standard_caching_without_wa" : "/#do_not_use#"
              },
              "backoffFactor" : 1.15,
              "fetch" : [],
              "ipAddress" : null,
              "upgradeStrategy" : {
                 "maximumOverCapacity" : 1,
                 "minimumHealthCapacity" : 1
              }
           }
        }
 

Container connector iApp configuration parameters
-------------------------------------------------
                                         
- "F5_PARTITION" : "test":  This is the partition on BIG-IP to create/update/delete the iApp in. This should be the same partition the BIG-IP Container Connector is configured to manage.
 
- "F5_0_IAPP_TEMPLATE" : "/Common/f5.http":  This is the iApp template to invoke. These templates can be in any partition that the defined "F5_PARTITION" has permissions to refer to. We recommend putting new iApps in /Common, in keeping with the rule that only the BIG-IP Container Connector should create/update/delete objects in its dedicated partition.
 
- "F5_0_IAPP_POOL_MEMBER_TABLE" :  This is a JSON blob defining the special iApp table that contains the pool members. When the BIG-IP Container Connector goes to configure the iApp, it will fill out this table; the pool members are the Marathon tasks for this App.
 
- "F5_0_IAPP_VARIABLE_*": These iApp variables specify user-provided configuration input required by the iApp. These are opaque to the BIG-IP Container Connectors. For example:
    The Marathon Application label ``F5_0_IAPP_VARIABLE_pool__addr: "172.16.3.2"`` defines the IP address to assign to the pool created by the iApp.

- "F5_0_IAPP_OPTION_*": These iApp options also specify user-provided configuration input, but they're not fields that are required by the iApp. These are also opaque to the BIG-IP Container Connectors. For example: The Marathon Application Label ``F5_0_IAPP_OPTION_description: "This is a test iApp"`` populates the iApp's "description" field.
 
The best way to understand ``_VARIABLE_`` and ``_OPTION_`` is to look at what the configuration produces on the BIG-IP. 

Notice that ``F5_0_IAPP_VARIABLE_pool__addr`` is defined in the "variables" section, while ``F5_0_IAPP_OPTION_description`` is defined in the top-level option "description".
 
.. code-block:: text
    :linenos:
    :emphasize-lines: 3, 7-19, 56

    root@(host-172)(cfg-sync Standalone)(Active)(/Common)(tmos)# list sys app service /test/test-svc_iapp_10001.app/test-svc_iapp_10001
    sys application service /test/test-svc_iapp_10001.app/test-svc_iapp_10001 {
        description "This is a test iApp"
        device-group none
        inherited-devicegroup true
        partition test
        tables {
            pool__members {
                column-names { addr port connection_limit }
                rows {
                    {
                        row { 172.16.1.21 13122 0 }
                    }
                    {
                        row { 172.16.1.21 16324 0 }
                    }
                }
            }
        }
        template f5.http
        traffic-group traffic-group-local-only
        variables {
            client__standard_caching_with_wa {
                value "/#create_new#"
            }
            client__standard_caching_without_wa {
                value "/#do_not_use#"
            }
            client__tcp_wan_opt {
                value "/#create_new#"
            }
            monitor__frequency {
                value 30
            }
            monitor__monitor {
                value "/#create_new#"
            }
            monitor__response {
                value none
            }
            monitor__uri {
                value /
            }
           net__client_mode {
                value wan
            }
            net__server_mode {
                value lan
            }
            net__snat_type {
                value automap
            }
            net__vlan_mode {
                value all
            }
            pool__addr {
                value 172.16.3.2
            }
            pool__http {
                value "/#create_new#"
            }
            pool__lb_method {
                value round-robin
            }
            pool__mask {
                value 255.255.255.255
            }
            pool__persist {
                value "/#do_not_use#"
            }
            pool__pool_to_use {
                value "/#create_new#"
            }
            pool__port {
                value 8080
            }
            server__ntlm {
                value "/#do_not_use#"
            }
            server__oneconnect {
                value "/#create_new#"
            }
            server__tcp_lan_opt {
                value "/#create_new#"
            }
            ssl_encryption_questions__advanced {
                value yes
            }
        }
    }
 
Now, on the BIG-IP configuration utility, you can go to iApps -> Application Services and see the iApp instance and the objects it created.
 
The easiest way to identify the ``_OPTIONS_`` and ``_VARIABLES_`` information for an existing iApp is to configure the iApp on the BIG-IP "by hand", then do "list sys app service <foo>" to see what the resulting ``_OPTIONS_`` and ``_VARIABLES_`` are. 

You can also read the iApp template on the BIG-IP (or write a new one yourself) to determine the fields the user is expected/required to populate.
 
The iApp is reconfigured whenever the labels or the Marathon tasks/Kubernetes Pods change (containers die or are spawned).
 
The pool members table is filled out according to the JSON blob defined for the Container Connector. It looks a lot like what you see in the ``tmsh list`` output.

::
   
    tables {
            pool__members {
                column-names { addr port connection_limit }
                rows {
                    {
                        row { 172.16.1.21 13122 0 }
                    }
                    {
                        row { 172.16.1.21 16324 0 }
                    }
                }
            }
        }
 

