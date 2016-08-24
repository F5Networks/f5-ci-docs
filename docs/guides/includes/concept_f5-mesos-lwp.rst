Internal Load Balancing with F5 Lightweight Proxy
`````````````````````````````````````````````````

Internal load balancing and service discovery is provided by F5's Lightweight Proxy Controller.

The lwp-controller subscribes to Marathon's event stream and will automatically launch a lightweight proxy (LWP) configured with each task within Maraton. As tasks are scaled or failed tasks are moved to a new node, the lwp-controller configures the LWP in real-time to correct direct traffic to the correct applciation or service.
