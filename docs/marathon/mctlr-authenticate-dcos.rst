.. _mesos-authentication:

Set up authentication to a secure DC/OS cluster
===============================================

If you're using the Apache Mesos DC/OS `cluster security features <https://docs.mesosphere.com/1.8/overview/features/#identity-access-mgmt>`_, you'll need to give |mctlr-long| access to your cluster.

DC/OS Open
----------

Apache Mesos `DC/OS Open <https://dcos.io/>`_ uses `DC/OS oauth <https://dcos.io/docs/1.8/administration/id-and-access-mgt/>`_ to secure access. To use the |mctlr| App with a secure cluster, assign it a user account with permission to access the desired cluster.

#. `Create a user account for the App <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/oss/managing-authentication/>`_

#. `Generate the HTTP API token <https://dcos.io/docs/1.8/administration/id-and-access-mgt/oss/iam-api/>`_ and record it in a safe place.

#. Add the token to your |mctlr| App definition using the ``F5_CC_DCOS_AUTH_TOKEN`` configuration parameter.

   .. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example.json
      :linenos:
      :lines: 1-18, 22-26
      :emphasize-lines: 21-22


DC/OS Enterprise
----------------

`DC/OS Enterprise <https://docs.mesosphere.com/>`_ provides access control via `Service Accounts <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/ent/service-auth/>`_.

- If you use the ``permissive`` or ``strict`` `Security Mode <https://docs.mesosphere.com/1.8/administration/installing/ent/custom/configuration-parameters/#security>`_, you'll need to create a Service Account for the |mctlr|.
- If you have disabled the Security Mode, you don't need to create a Service Account for the |mctlr|.

#. `Create a Service Account <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/ent/service-auth/custom-service-auth>`_ with the permissions shown below.

   ================================================   =======
   Resource                                           Action
   ================================================   =======
   ``dcos:adminrouter:service:marathon``              full
   ``dcos:service:marathon:marathon:admin:events``    read
   ``dcos:service:marathon:marathon:services:/``      read
   ================================================   =======

#. Get the certificate for your cluster:

   .. code-block:: bash

      curl -k -v https://<cluster-url>/ca/dcos-ca.crt -o dcos-ca.crt

   .. important::

      If you don't provide a server certificate, the |mctlr| won't be able to authenticate to the Marathon API server.

#. Define the ``F5_DC/OS_AUTH_CREDENTIALS`` JSON blob.

   .. important::

      - ``F5_CC_DCOS_AUTH_CREDENTIALS`` is a JSON object, so you'll have to escape all quotes (e.g., ``\"``).
      - Incorrectly formatted keys will cause authentication failures. Denote and escape all newlines (``\\n``) in the private key string before removing the line breaks.

   .. code-block:: bash

      "{
          \"scheme\": \"RS256\",
          ## the DC/OS account name
          \"uid\": \"my_example_service_account\",
          ## the cluster login endpoint
          \"login_endpoint\": \"https://my_example_mesos_master.com/acs/api/v1/auth/login\",
          ## the contents of the private key you created for the DC/OS account
          \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+qqT9WhKnWa9G\\nxeJ889v+uuvHs0QBnDC0FeqQXwNJdYoxjJBPFSBp2j82MrWA7llamKyZqZqPF69C\\nO2/PetkqzMMhPlhVbYqJ/yObqrTpjwREv8qHovnEyD7pZeOd87/UoT6Bb6pAITjW\\nJvtRkqrjzfpFM9oeu/Ln3+0lY45s3TcDhsE0Ytl1m9IzyUg23CkGWvg41c6K2yPa\\ng4zstnImgpr+Tont1Jt1Hz9skwtiUQgsswTrJ784F0iKGiFmx9zR5Up9iuYPTo+G\\nOHHwrOi0emxrNm9iFPRtnyzs16daDCBcfmWFJFHZeFJc/yDqWNvd9uNCZCNdBpHP\\nAy97Rh8tAgMBAAECggEBALCvO2NXY6/W6RkBaUd3R2c/Whzd32hKj8th/9K3aTla\\nhawy4MuX/Uh6KVeVGCMZPI46qr9ers5pGUyb/Znb8oC57RzSRFMtxlLortujDjDd\\nCgyXWhvlB+W11q68b3hAl4R3w494peD1qFCzIPNPobKmfoRAb6FJc+gx1vVt017G\\n6qRhwSU0GC0DQDvpe6Zr6cih0gzkEeaadfeNsHhPwfa4xgd5tagqfBl9jaW09bzn\\nJWJguEybfcj88bvQsQbW+goKYqPo/QeX4cuP4zxLSSUiZ6Nl3XCYLrnqHClJknEl\\nswj/CS3d6TKJNuxwT3dnWT72ntg/XpYtC63knHoR//UCgYEA35D9tg0woqOnuOt5\\nrm2Kbt9WNDUdH+ov5L8zQ9Lqop+3JBAAWcUHvUFx54ub0SYoonUZrLS3gqlWv9Vl\\noKu63ypN1uaNRwoWqCDByUAUeJ5NL3plViTLGVWpybEN+WJLB8l4IaIMmwe1vn42\\ntZQqlzpme/7bV9pHNqs+cCzWAKMCgYEA2lPKmQyO//ynHiNH15mhCqQ3Ce9i4WCK\\nNoL5SA0YLaKycHe/KGqXnFIll8Tly5iot/W7c7dW2sGV7URv23EgeGVfG1hi8MyW\\nB7aXu63VDVmCf3R0YAZx10Yr80XypSRhlJxw8PjrTBGogQVVyvH/CXvx54ClowZL\\n1PMl3uWzze8CgYEAq3OyXu92oQQJGJPd2ZtAUw8MOTWShGtBF5haZGVYdCcweIOd\\nATtNWCLci8pRUPCGsTBE5GIjah0b3jp1meaZhZQX5fsh1Z0zCvU0KHbwPCCK6SJg\\nnNPSvjcn4vnZ0atEB1DGxGRWbn5XLyP0KQTcNOYgum8VICbR/mcNl1GLPSkCgYAC\\nh0vmX93cGxn4YGI5nf7ed65ngA0+HPcc0IGAkx4/kQ3N/aUKG8nrtovW6SHcLMVv\\nc/oayfnIiMtqtwswmGvO2SWz1F84+LWYG0ZAly/LesjnHvsmDY0N+DMUGzBHN1el\\n9/Xa5JcdB2tTKzOmKQ1SF8xiaPwCGlWQfsxme3SMowKBgH+XXogAosJITFxZlIx0\\ngYPFWFCNDMpFrp5+hur8XPHQTf7N/6byVkNeUltdzXfkVepDJGaani+N05YpUi1o\\nt7PTl1fZrDNAhdU6mqNS1GjOZPsRWTm6g2Ful9vPwIst+HK5R+7jouneWGkOa/PP\\nLcmeSjG19SE4XX+SWUlzuDck\\n-----END PRIVATE KEY-----\"
      }"


#. Add the ``F5_CC_DCOS_AUTH_CREDENTIALS`` and ``F5_CC_MARATHON_CA_CERT`` labels to the |mctlr| App definition.

   .. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example.json
      :lines: 1-23, 26-27
      :linenos:
      :emphasize-lines: 19-21
