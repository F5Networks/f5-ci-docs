Overview
--------

F5's Lightweight Proxy Controller (lwp-controller) provides internal load balancing and service discovery in a Mesos cluster. It watches Marathon's event stream for changes in applications and automatically starts, stops, and/or reconfigures the lightweight proxy (LWP) app as needed. The LWP, in turn, watches Marathon to automatically load balance across an application's tasks as the application is scaled.

Current Versions
````````````````
* lwp-controller - |lwpc_version|
* lightweight-proxy - |lwp_version|
