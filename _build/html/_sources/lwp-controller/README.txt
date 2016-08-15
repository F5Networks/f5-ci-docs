Status: [![build status](https://bldr-git.int.lineratesystems.com/velcro/lwp-controller/badges/master/build.svg)](https://bldr-git.int.lineratesystems.com/velcro/lwp-controller/commits/master)


# Intro

The lwp-controller is designed to run as a docker container in
Mesos+Marathon. It watches applications being created and
destroyed. When an application with the proper labels is created a new
LWP is created for that application and it is scaled to have the
requested number of tasks.

# Configuration
Environment variables are used to configure the lwp-controller. The variables are:
- MARATHON_URL (URL of the Marathon API. default: http://127.0.0.1:8080)
- LWP_ENABLE_LABEL (label used to determine LWP requirements. default: f5-lwp)
- LWP_DEFAULT_CPU (amount of CPU for LWP tasks. default: 0.1)
- LWP_DEFAULT_MEM (amount of memory for LWP tasks. default: 64)
- LWP_DEFAULT_STORAGE (amount of memory for LWP tasks. default: 0)
- LWP_DEFAULT_COUNT_PER_APP (number of LWP tasks per application. default: 1)
- LWP_DEFAULT_CONTAINER (location of docker image to pull. default: f5networks/lwp)
- LWP_DEFAULT_CONTAINER_PORT (container port to expose. default: 8000)
- LWP_DEFAULT_URIS (comma separated list of URIs to pass to Marathon. default: EMPTY)
- LWP_DEFAULT_VS_KEEP_ALIVE (Virtual server keep alive, in msecs. default: 1000)
- LWP_DEFAULT_VS_PROTOCOL (protocol for virtual server, http or tcp. default: http)
- LWP_DEFAULT_STATS_URL (Url for sending stats. default: None)
- LWP_DEFAULT_STATS_TOKEN (Stats authentication token. default: None)
- LWP_DEFAULT_STATS_FLUSH_INTERVAL (Stats flush intercal, in msecs. default: 10000)
- LWP_DEFAULT_STATS_BACKEND (Stats backend type, i.e. splunk. default: None)
- LWP_DEFAULT_FORCE_PULL (Sets Marathon to force pull every time the LWP starts. default: true)
- LWP_ENV_PREFIX (prefix for environment variables to pass to the LWP. default: LWP_ENV_)
- LWP_DEFAULT_LOG_LEVEL (logging level. default: INFO)
- LWP_DEFAULT_VS_FLAGS (flags for configuring LWP behavior. Only bools (true or false) are permitted as values. default: {})

## Example

Usually, the lwp-controller is deployed by Marathon. This is an
example of how it would be run by a human on the command-line. This is
provided for enhanced understanding, not as a recommendation.

```sh
docker run -it -d \
  -e MARATHON_URL="http://172.28.128.3:8080" \
  -e LWP_ENABLE_LABEL lwp-myapp \
  -e LWP_DEFAULT_CONTAINER f5networks/lwp
  f5velcro/lwp-controller
```

Then create your application in the Marathon instance running
at 172.28.128.3 and label it with the label:

```
lwp-myapp:enable
```

The lwp-controller will create a new application in your Marathon
cluster to be the LWP for your application.

# Overriding Controller Configuration

Default values configured for the LWP Controller can be modified on a
per-app basis. The following labels can be applied to the application
being controlled and will override the corresponding LWP Controller
default value.

- LWP_VS_KEEP_ALIVE (overrides LWP_DEFAULT_VS_KEEP_ALIVE)
- LWP_VS_PROTOCOL (overrides LWP_DEFAULT_VS_PROTOCOL)
- LWP_LOG_LEVEL (overrides LWP_DEFAULT_LOG_LEVEL)
- LWP_STATS_URL (overrides LWP_DEFAULT_STATS_URL)
- LWP_STATS_TOKEN (overrides LWP_DEFAULT_STATS_TOKEN)
- LWP_STATS_FLUSH_INTERVAL (overrides LWP_DEFAULT_STATS_FLUSH_INTERVAL)
- LWP_STATS_BACKEND (overrides LWP_DEFAULT_STATS_BACKEND)
- LWP_FORCE_PULL (overrides LWP_DEFAULT_FORCE_PULL)
- LWP_CPU (overrides LWP_DEFAULT_CPU)
- LWP_MEM (overrides LWP_DEFAULT_MEM)
- LWP_STORAGE (overrides LWP_DEFAULT_STORAGE)
- LWP_COUNT_PER_APP (overrides LWP_DEFAULT_COUNT_PER_APP)
- LWP_CONTAINER (overrides LWP_DEFAULT_CONTAINER)
- LWP_URIS (overrides LWP_DEFAULT_URIS)
- LWP_VS_FLAGS (merges with and overrides collisions on LWP_DEFAULT_VS_FLAGS)

# Configuring the LWP (not yet implemented)

LWP is configured by adding a special label to your app containing the
desired configuration in JSON format. The special label is
```LWP_CONFIG```. See documentation at
https://bldr-git.int.lineratesystems.com/velcro/traffic-director-proxy
for details. Note, values specified in this config will not be
overwritten by the LWP Controller. Specifying the app name and port
might lead to misconfiguration or unexpected behavior. Avoid this in
general. There are no known use cases for specifying these yet.

The LWP Controller (TDC) can also pass through environment variables
for additional configuration. Add labels to your application to pass
through to the LWP using the LWP_ENV_PREFIX.

## Example 

Add to pass through the environment ```FOO=bar``` just add this label
to your application:

```
LWP_ENV_FOO:bar
```

Also, any of the ```LWP_DEFAULT_*``` environment variables can be
overriden by adding a label. For example, override the LWP_DEFAULT_CPU
and set it to 2.3 by adding the label:

```
LWP_ENV_LWP_CPU:2.3
```

# Known Limitations

- Changes to LWP_ENABLE_LABEL cause the lwp-controller to start
  controlling a new set of apps which have the new value as a
  label. All apps with the old label will be ignored. Since the
  lwp-controller is stateless with respect to Marathon it needs to be
  this way. An easy way to avoid this problem is to never change the
  LWP_ENABLE_LABEL of an existing lwp-controller. Always just destroy
  the lwp-controller and create a new one. This way there is no
  confusion or expectation of a different behavior.

- More than 1 Mesos slave is required. By default, Marathon's restart
  policy starts a new instance of the app being modified before
  killing the old version. When there is only 1 slave the LWP reserves
  a port on that slave and then a new version cannot be started when
  there is a configuration modification. This will be addressed in a
  future version by permitting Marathon's restart policy to be
  configurable on a per lwp-controller or per app basis.
