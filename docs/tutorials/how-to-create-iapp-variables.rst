.. _create-iapp-variables:

How to Create iApp Variables
============================

The |kctlr-long| and |mctlr-long| both support deployment of iApps, which gives them access to essentially all the advanced l4-l7 features on BIG-IP. To deploy an iApp, you need to create custom ``iappVariables`` key-value pairs; these provide the information the iApp needs to configure the BIG-IP.

.. important::

    The instructions provided here apply to all supported orchestration environments. In the examples, we reference Marathon and the |mctlr-long|.

At a high level, the way it works is:

1) You define a new Application in Marathon, with F5 :ref:`Application labels <app-labels>` defined.
2) The |mctlr| notices the new labels and configures a new iApp on the BIG-IP. Referencing an iApp Template that already exists on the BIG-IP (several are built-in).
3) The iApp template is invoked to handle the new iApp that was just defined. The iApp template can create a virtual server, pool members, and so on. 

First, you need to determine what fields in the iApp template need correspondin ``iappVariables``.

#. We recommend that you `deploy the iApp <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-iapps-developer-11-4-0/2.html#unique_1831084015>`_ using the BIG-IP configuration utility.

#. Make a REST call to the BIG-IP to determine what configurations were applied.


At a high level, the way it works is:
1) You define a new application in Marathon, with a bunch of labels.
2) f5-marathon-lb notices the new labels.  Instead of configuring a plain ol' virtual server, pool, pool members, it configures a new iApp.  The iApp must be configured from an iApp Template that already exists on the BIG-IP (several are built-in).
3) The iApp template is invoked to handle the new iApp that was just defined.  The iApp template can create a virtual server, pool members and so on.  It can do anything an iApp can do, which gives it access to essentially all the advanced features on BIG-IP.
 
Here's the JSON for an example application I configured in Marathon (via ``curl -v -H "Accept: application/json" http://10.190.25.245:8080/v2/apps/test-svc | json_pp``).  It's long; I bold-faced the interesting parts:
 
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
            "image" : "docker-registry.pdbld.f5net.com/systest-common/test-nginx",
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
 
The labels are instructions to f5-marathon-lb about what to do to BIG-IP in response to this application being configured.  You can also configure an app using the Marathon GUI and specify these labels there.
                                         
"F5_PARTITION" : "test":  This is the partition on BIG-IP to create/update/delete the iApp in.  This should be the same partition that you passed to f5-marathon-lb (if it is different, the f5-marathon-lb will assume you actually want some other f5-marathon-lb to handle it, and skip).
 
"F5_0_IAPP_TEMPLATE" : "/Common/f5.http":  This is the iApp template to invoke.  ("list sys application template" on BIG-IP, or in the GUI under iApps -> Templates.)  These templates can be in any partition that the f5-marathon-lb partition has permissions to refer to; we recommend putting new iApps in /Common in this case so that you follow the rule "Only f5-marathon-lb creates/updates/deletes things in its partition".
 
"F5_0_IAPP_POOL_MEMBER_TABLE_NAME" : "pool__members": This is the name of the special iApp table that contains the pool members.  When f5-marathon-lb goes to configure the iApp, it will fill out this table: the pool members are the Marathon tasks for this app.
 
"F5_0_IAPP_VARIABLE_*": These are iApp variables - configuration input to the iApp.  These are opaque to f5-marathon-lb.
  One example - F5_0_IAPP_VARIABLE_pool__addr: "172.16.3.2"
"F5_0_IAPP_OPTION_*": These are iApp options - configuration input to the iApp.  These are opaque to f5-marathon-lb.
  One example - F5_0_IAPP_OPTION_description: "This is a test iApp"
 
The best way to understand _VARIABLE_ and _OPTION_ is to look at what this configuration produces on the BIG-IP.  Notice how the F5_0_IAPP_VARIABLE_pool__addr is filled in in the "variables" section, and how the F5_0_IAPP_OPTION_description is filled in at the top-level option "description".
 
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
 
Now on the BIG-IP GUI, I can go to iApps -> Application Services, then make sure I am in the "test" partition (top-right), and see the iApp instance and the objects it created:
 

 
In my opinion, the easiest way to identify the \OPTIONS_ and \VARIABLES_ information for an existing iApp is to configure one on the BIG-IP "by hand", then do "list sys app service <foo>" to see what the resulting \OPTIONS_ and \VARIABLES_ are.  You can also actually read the iApp template on the BIG-IP (or write a new one yourself), too.
 
The iApp is reconfigured whenever the labels or the Marathon tasks change (containers die or are spawned).
 
The way the pool members table is filled out looks like (copy-paste from the "tmsh list" output above):
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
 
This does not work for the app services iApp (https://github.com/0xHiteshPatel/appsvcs_integration_iapp), which expects a slightly different table, so IBM cannot currently use f5-marathon-lb with that particular iApp.  We are fixing that for the GA release of f5-marathon-lb (early March).
 
Last note, the _{0}_ part is for the port index in Marathon that this iApp should be used for.  So, if you have an application with only one exposed port (like this example nginx app), you just use F5_0_IAPP_TEMPLATE.  If you have an application that exposes multiple ports, you can use F5_0_IAPP_TEMPLATE (and all the other F5_0_* labels) to configure one iApp for that port, and F5_1_IAPP_TEMPLATE (and F5_1_*) for the next port, and so on.
