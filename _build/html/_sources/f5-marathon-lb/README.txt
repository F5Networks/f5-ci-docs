# f5-marathon-lb
f5-marathon-lb is a tool for managing F5 BIG-IP, by consuming [Marathon's](https://github.com/mesosphere/marathon) app state.

## Architecture
The f5-marathon-lb is a service discovery and load balancing tool for Marathon to configure an F5 BIG-IP. It reads the Marathon task information and dynamically generates BIG-IP configuration details.  

f5-marathon-lb listens to the Marathon event stream and automatically updates the configuration of the BIG-IP and does the following: 

 - Matches Marathon apps by the specified BIG-IP partition
 - Creates a Virtual Server and pool for each app type in Marathon that matches the BIG-IP partition
 - For each task, creates a pool member and adds the member to the server pool 
 - If the app has a Marathon Health Monitor configured, creates a corresponding health monitor for each BIG-IP pool member 

To gather the task information, f5-marathon-lb needs to know where to find Marathon. The service configuration details are stored in labels.  

## Configuration

First, f5-marathon-lb needs to know how to connect to Marathon and the BIG-IP, which is done via the command-line arguments:


```console
usage: f5_marathon_lb.py [-h] [--longhelp]
                         [--marathon MARATHON [MARATHON ...]]
                         [--listening LISTENING] [--callback-url CALLBACK_URL]
                         [--hostname HOSTNAME] [--username USERNAME]
                         [--password PASSWORD] [--partition PARTITION] [--sse]
                         [--health-check] [--syslog-socket SYSLOG_SOCKET]
                         [--log-format LOG_FORMAT]
                         [--marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE]

If an arg is specified in more than one place, then commandline values
override environment variables which override defaults.

optional arguments:
  -h, --help            show this help message and exit
  --longhelp            Print out configuration details (default: False)
  --marathon MARATHON [MARATHON ...], -m MARATHON [MARATHON ...]
                        [required] Marathon endpoint, eg. -m
                        http://marathon1:8080 http://marathon2:8080 [env var:
                        MARATHON_URL] (default: None)
  --listening LISTENING, -l LISTENING
                        The address this script listens on for marathon events
                        [env var: F5_CSI_LISTENING_ADDR] (default: None)
  --callback-url CALLBACK_URL, -u CALLBACK_URL
                        The HTTP address that Marathon can call this script
                        back at (http://lb1:8080) [env var:
                        F5_CSI_CALLBACK_URL] (default: None)
  --hostname HOSTNAME   F5 BIG-IP hostname [env var: F5_CSI_BIGIP_HOSTNAME]
                        (default: None)
  --username USERNAME   F5 BIG-IP username [env var: F5_CSI_BIGIP_USERNAME]
                        (default: None)
  --password PASSWORD   F5 BIG-IP password [env var: F5_CSI_BIGIP_PASSWORD]
                        (default: None)
  --partition PARTITION
                        [required] Only generate config for apps which match
                        the specified partition. Use '*' to match all
                        partitions. Can use this arg multiple times to specify
                        multiple partitions [env var: F5_CSI_PARTITIONS]
                        (default: [])
  --sse, -s             Use Server Sent Events instead of HTTP Callbacks [env
                        var: F5_CSI_USE_SSE] (default: False)
  --health-check, -H    If set, respect Marathon's health check statuses
                        before adding the app instance into the backend pool.
                        [env var: F5_CSI_USE_HEALTHCHECK] (default: False)
  --sse-timeout SSE_TIMEOUT, -t SSE_TIMEOUT
                        Marathon event stream timeout [env var:
                        F5_CSI_SSE_TIMEOUT] (default: 30)
  --syslog-socket SYSLOG_SOCKET
                        Socket to write syslog messages to. Use '/dev/null' to
                        disable logging to syslog [env var:
                        F5_CSI_SYSLOG_SOCKET] (default: /var/run/syslog)
  --log-format LOG_FORMAT
                        Set log message format [env var: F5_CSI_LOG_FORMAT]
                        (default: %(asctime)s %(name)s: %(levelname) -8s:
                        %(message)s)
  --marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE
                        Path to file containing a user/pass for the Marathon
                        HTTP API in the format of 'user:pass'. [env var:
                        F5_CSI_MARATHON_AUTH] (default: None)
```

_The **marathon**, **hostname**, **username**, **password**, and **partition** arguments are mandatory_.

Use the --partition argument multiple times to specify multiple BIG-IP partitions to be managed (e.g. --partition foo --partition bar).

### Partitions

The partitions managed by f5-marathon-lb must already exist, and f5-marathon-lb can manage any partitions except "Common".

f5-marathon-lb takes ownership of certain resource types in the partitions it is given to manage, and modifications to these resource types in other ways (GUI, REST, etc) than via f5-marathon-lb will lead to unpredictable behavior.

The resource types managed by f5-marathon-lb are:

 - Virtual Servers
 - Virtual Addresses
 - Pools
 - Pool Members
 - Nodes
 - Health Monitors
 - Application Services

To prevent conflict with f5-marathon-lb, **no** user-managed items should be configured within partitions that are managed by f5-marathon-lb.

### Application Labels

Applications to be managed by f5-marathon-lb are identified and configured via their _Marathon Labels_. Some labels are specified _per service port_. These are denoted with the `{n}` parameter in the label key, where `{n}` corresponds to the service port index, beginning at `0`.

The list of labels which can be specified are:

```
 F5_PARTITION

    The BIG-IP partition to be configured
    Resources like virtual servers and pool members are configured in this partition on BIG-IP.  It must be one of the partitions that f5-marathon-lb owns (via the "--partition" argument to f5-marathon-lb).

 F5_{n}_BIND_ADDR

    Bind to the specific address for the service
    Ex: "F5_0_BIND_ADDR": "10.0.0.42"

 F5_{n}_PORT

    Bind to the specific port for the service
    This overrides the servicePort which has to be unique
    Ex: "F5_0_PORT": "80"

 F5_{n}_MODE

    Set the connection mode to either TCP or HTTP. The default is TCP.
    Ex: "F5_0_MODE": "http"

 F5_{n}_BALANCE

    Set the load balancing algorithm to be used in a backend. The default is roundrobin.
    Ex: "F5_0_BALANCE": "leastconn"

 F5_{n}_SSL_PROFILE

    Set the SSL profile to be used for the HTTPS Virtual Server
    Ex: "F5_0_SSL_PROFILE": "Common/clentssl"
```


### Building and Running

The following shows how to build and launch f5-marathon-lb as a Docker container. 

Build a Docker container:

```console
    docker build -t docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest .
```

Push it to a Docker registry:

```console
    docker push docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest
```

Launch it in Marathon:

```console
    curl -X POST -H "Content-Type: application/json" http://10.141.141.10:8080/v2/apps -d @f5-marathon-lb.json
```

Where "f5-marathon-lb.json" contains the details needed to deploy the container in Marathon, e.g.:

```json
{
  "id": "f5-marathon-lb",
  "cpus": 0.5,
  "mem": 128.0,
  "instances": 1,
  "container": {
    "type": "DOCKER",
    "forcePullImage": true,
    "docker": {
      "image": "docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest",
      "network": "BRIDGE"
    }
  },
  "args": [
    "sse",
    "--marathon", "http://10.141.141.10:8080",
    "--partition", "mesos_1",
    "--hostname", "10.128.1.145",
    "--username", "admin",
    "--password", "default"
  ]
}
```

Or launch it this way, using **env** variables instead of **args**.

```json
{
  "id": "f5-mlb",
  "cpus": 0.5,
  "mem": 128.0,
  "instances": 1,
  "container": {
    "type": "DOCKER",
    "forcePullImage": true,
    "docker": {
      "image": "docker-registry.pdbld.f5net.com/velcro/f5-marathon-lb:latest",
      "network": "BRIDGE"
    }
  },
  "env": {
    "F5_CSI_USE_SSE": "True",
    "MARATHON_URL": "http://10.141.141.10:8080",
    "F5_CSI_PARTITIONS": "[mesos_1, mesos_test]",
    "F5_CSI_BIGIP_HOSTNAME": "10.128.1.145",
    "F5_CSI_BIGIP_USERNAME": "admin",
    "F5_CSI_BIGIP_PASSWORD": "default"
  }
}
```


The following is an example for an application deployment in Marathon, with the appropriate f5-marathon-lb labels configured. In this example, the app (server-app4) has three service ports configured, but only the first two are exposed via the BIG-IP (i.e. only port indices 0 and 1 are configured in the _labels_ section). Marathon health monitors are configured for all three service ports.

```json
{
  "id": "server-app4",
  "cpus": 0.1,
  "mem": 16.0,
  "instances": 2,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "edarzins/node-web-app",
      "network": "BRIDGE",
      "forcePullImage": false,
      "portMappings": [
        { "containerPort": 8088,
          "hostPort": 0,
          "protocol": "tcp" },
        { "containerPort": 8188,
          "hostPort": 0,
          "protocol": "tcp" },
        { "containerPort": 8288,
          "hostPort": 0,
          "protocol": "tcp" }
      ]
    }
  },
  "labels": {
    "F5_PARTITION": "mesos",
    "F5_0_BIND_ADDR": "10.128.10.240",
    "F5_0_MODE": "http",
    "F5_0_PORT": "8080",
    "F5_1_BIND_ADDR": "10.128.10.242",
    "F5_1_MODE": "http",
    "F5_1_PORT": "8090"
  },
  "healthChecks": [
    {
      "protocol": "HTTP",
      "portIndex": 0,
      "path": "/",
      "gracePeriodSeconds": 5,
      "intervalSeconds": 20,
      "maxConsecutiveFailures": 3
    },
    {
      "protocol": "HTTP",
      "portIndex": 1,
      "path": "/",
      "gracePeriodSeconds": 5,
      "intervalSeconds": 20,
      "maxConsecutiveFailures": 3
    },
    {
      "protocol": "HTTP",
      "portIndex": 2,
      "path": "/",
      "gracePeriodSeconds": 5,
      "intervalSeconds": 20,
      "maxConsecutiveFailures": 3
    }
  ]
}
```

The following shows the BIG-IP configuration produced by f5-marathon-lb for the preceding Marathon configuration; showing virtual servers, pools, and health monitors.

If a Marathon health monitor exists for a service port, f5-marathon-lb will also create a health monitor for it on the BIG-IP. The exception to this is when the "--health-check" option is used when starting f5-marathon-lb. If this option is set, f5-marathon-lb will respect the Marathon health status for the service port before adding it to the backend pool.

```
ltm monitor http server-app4_10.128.10.240_8080 {
    adaptive disabled
    defaults-from /Common/http
    destination *:*
    interval 20
    ip-dscp 0
    partition mesos
    send "GET /\r\n"
    time-until-up 0
    timeout 61
}
ltm monitor http server-app4_10.128.10.242_8090 {
    adaptive disabled
    defaults-from /Common/http
    destination *:*
    interval 20
    ip-dscp 0
    partition mesos
    send "GET /\r\n"
    time-until-up 0
    timeout 61
}
ltm node 10.141.141.10 {
    address 10.141.141.10
    partition mesos
    session monitor-enabled
    state up
}
ltm persistence global-settings { }
ltm pool server-app4_10.128.10.240_8080 {
    members {
        10.141.141.10:31383 {
            address 10.141.141.10
            session monitor-enabled
            state up
        }
        10.141.141.10:31775 {
            address 10.141.141.10
            session monitor-enabled
            state up
        }
    }
    monitor server-app4_10.128.10.240_8080
    partition mesos
}
ltm pool server-app4_10.128.10.242_8090 {
    members {
        10.141.141.10:31384 {
            address 10.141.141.10
            session monitor-enabled
            state up
        }
        10.141.141.10:31776 {
            address 10.141.141.10
            session monitor-enabled
            state up
        }
    }
    monitor server-app4_10.128.10.242_8090
    partition mesos
}
ltm virtual server-app4_10.128.10.240_8080 {
    destination 10.128.10.240:webcache
    ip-protocol tcp
    mask 255.255.255.255
    partition mesos
    pool server-app4_10.128.10.240_8080
    profiles {
        /Common/http { }
        /Common/tcp { }
    }
    source 0.0.0.0/0
    source-address-translation {
        type automap
    }
    vs-index 153
}
ltm virtual server-app4_10.128.10.242_8090 {
    destination 10.128.10.242:8090
    ip-protocol tcp
    mask 255.255.255.255
    partition mesos
    pool server-app4_10.128.10.242_8090
    profiles {
        /Common/http { }
        /Common/tcp { }
    }
    source 0.0.0.0/0
    source-address-translation {
        type automap
    }
    vs-index 154
}
```


### iApps

iApps is the BIG-IP system framework for deploying services-based, template-driven configurations on BIG-IP systems running TMOS 11.0.0 and later. It consists of three components: Templates, Application Services, and Analytics. An iApps Template is where the application is described and the objects (required and optional) are defined through presentation and implementation language. An iApps Application Service is the deployment process of an iApps Template which bundles all of the configuration options for a particular application together.

#### iApp Labels

f5-marathon-lb can be used to instantiate and manage an iApp Application Service, with the iApp template and variables specicified via the LABELS in a Marathon application.

```

 F5_{n}_IAPP_TEMPLATE

    The iApp template to create the Application Service. The template must already be installed on the BIG-IP
    Ex: "F5_0_IAPP_TEMPLATE": "/Common/f5.http"

 F5_{n}_IAPP_OPTION_*

    The predicate that defines configuration options for the service
    Ex: "F5_0_IAPP_OPTION_description": "This is a test iApp"

 F5_{n}_IAPP_VARIABLE_*

    The predicate that defines the variables needed by the iApp to create the service. The variable names and values are specific to the template being used. The "/#create_new#" value directs the service to create the resource, otherwise it will use an existing, specified resource.

    Ex: "F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240"
    Ex: "F5_0_IAPP_VARIABLE_pool__pool_to_use": "/#create_new#"

 F5_{n}_IAPP_POOL_MEMBER_TABLE_NAME

    The name of the iApp table entry that specifies the pool members: THIS NAME IS NOT STANDARD AND CAN BE DIFFERENT FOR EACH iApp TEMPLATE.
    Ex: "F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members"
```

##### iApp Configuration Example

The following shows an example Marathon app definition configured to use the "f5.http" template to define an HTTP service. Note that the only label needed other than the IAPP labels, is the F5_PARTITION label. The parameters that were specified earlier for F5_0_BIND_ADDR and F5_0_PORT are now accounted for as iApp variables (pool__addr and pool__port, respectively).

```
{
  "id": "server-app2",
  "cpus": 0.1,
  "mem": 16.0,
  "instances": 4,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "edarzins/node-web-app",
      "network": "BRIDGE",
      "forcePullImage": false,
      "portMappings": [
        { "containerPort": 8088,
          "hostPort": 0,
          "protocol": "tcp" }
      ]
    }
  },
  "labels": {
    "F5_PARTITION": "mesos",
    "F5_0_IAPP_TEMPLATE": "/Common/f5.http",
    "F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members",
    "F5_0_IAPP_VARIABLE_net__server_mode": "lan",
    "F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240",
    "F5_0_IAPP_VARIABLE_pool__pool_to_use": "/#create_new#",
    "F5_0_IAPP_VARIABLE_monitor__monitor": "/#create_new#",
    "F5_0_IAPP_VARIABLE_monitor__uri": "/",
    "F5_0_IAPP_VARIABLE_monitor__response": "none",
    "F5_0_IAPP_VARIABLE_net__client_mode": "wan",
    "F5_0_IAPP_VARIABLE_pool__port": "8080",
    "F5_0_IAPP_OPTION_description": "This is a test iApp"
  },
  "healthChecks": [
    {
      "protocol": "TCP",
      "portIndex": 0,
      "path": "/",
      "gracePeriodSeconds": 5,
      "intervalSeconds": 20,
      "maxConsecutiveFailures": 3
    }
  ]
}
```
