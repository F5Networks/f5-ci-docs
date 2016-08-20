Edge Load Balancing with F5 Container Service Integrator
````````````````````````````````````````````````````````

To provide edge load balancing for applications running in Marathon, F5's f5-marathon-lb is used to dynamically configure an F5 BIG-IP device.

f5-marathon-lb listens to the Marathon event stream and automatically updates the configuration of the BIG-IP as follows:

- Matches Marathon apps to a specified BIG-IP partition.
- Creates a Virtual Server and pool for each application type in Marathon that matches an existing BIG-IP partition.
- For each task, creates a pool member and adds the member to the default pool.
- If the application has a Marathon Health Monitor configured, creates a corresponding health monitor for each BIG-IP pool member.
