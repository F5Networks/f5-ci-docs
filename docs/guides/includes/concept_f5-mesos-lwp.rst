Internal Load Balancing with F5 Lightweight Proxy
-------------------------------------------------

F5's Lightweight Proxy Controller provides load balancing and service discovery within Marathon. The lwp-controller subscribes to Marathon's event stream and automatically launches a lightweight proxy (LWP) configured with each task within Marathon. As tasks are scaled, or failed tasks are moved to a new node, the lwp-controller configures the LWP in real-time to direct traffic to the correct application or service.
