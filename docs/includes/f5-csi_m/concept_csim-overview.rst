.. rubric:: Overview

Apache `Mesos`_ and `Marathon`_ provide a platform for running containerized applications on a shared infrastructure. Applications are implemented by one or more identical tasks that are started and stopped automatically, and often given ephemeral addresses. Native support for exposing and load-balancing these applications to clients outside of Mesos, as well to other services within Mesos, is limited.

Enter the F5® |csi| (CSI), which expands on the native capabilities of Mesos and Marathon. With the |csi_m|, you can manage your BIG-IP® from within Marathon to provide edge load balancing and expose services outside the Mesos cluster. The |csi_m| can be used in conjunction with the F5® |lwp| |tm| for internal load balancing and service discovery.

