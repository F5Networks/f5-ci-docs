.. list-table::
    :widths: 10, 30
    :header-rows: 1

    * -
      - **Configuration Flow**
    * - 1
      - Administrator configures a new container application AppB in Marathon, requesting 2 tasks and LWP services
    * - 2
      - Marathon schedules and starts 2 tasks in the Mesos cluster
    * - 3
      - Marathon notifies F5 Container Service Integrator of new app and 2 new tasks
    * - 4
      - F5 Container Service Integrator configures Marathon to start a new container application that is LWP-AppB.
    * - 5
      - Marathon starts an LWP-AppB application with 1 task. LWP application learns about AppB-Task1 and AppB-Task2 from Marathon.
    * -
      - **Traffic Flow**
    * - 6
      - Client Microservice AppA-Task1 connects to LWP-AppB and sends request
    * - 7
      - LWP proxies request to a pool member (e.g. AppB-Task1)
