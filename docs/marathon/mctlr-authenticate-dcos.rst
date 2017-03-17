.. _mesos-authentication:

Set up authentication to your secure DC/OS cluster
==================================================


If you're using the Apache Mesos DC/OS `cluster security features <https://docs.mesosphere.com/1.8/overview/features/#identity-access-mgmt>`_, you'll need to give |mctlr-long| access to your cluster.

DC/OS Open
----------

Apache Mesos `DC/OS Open <https://dcos.io/>`_ uses `DC/OS oauth <https://dcos.io/docs/1.8/administration/id-and-access-mgt/>`_ to secure access. To use the |mctlr| App with a secure cluster, assign it a user account with permission to access the desired cluster.

#. `Create a user account for the App <https://dcos.io/docs/1.8/administration/id-and-access-mgt/managing-authentication>`_

#. `Generate the HTTP API token <https://dcos.io/docs/1.8/administration/id-and-access-mgt/iam-api/>`_ and record it in a safe place.

#. Add the token to your |mctlr| App definition using the ``F5_CC_DCOS_AUTH_TOKEN`` configuration parameter.

    .. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example.json
        :linenos:
        :lines: 1-18, 22-26
        :emphasize-lines: 22-23


DC/OS Enterprise
----------------

`DC/OS Enterprise <https://docs.mesosphere.com/>`_ provides access control via `Service Accounts <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/service-auth/>`_.

- If you use the ``permissive`` or ``strict`` `Security Mode <https://docs.mesosphere.com/1.8/administration/installing/custom/configuration-parameters/#security>`_, you'll need to create a Service Account for the |mctlr|.
- If you have disabled the Security Mode, you don't need to create a Service Account for the |mctlr|.

#. `Create a Service Account <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/service-auth/custom-service-auth>`_ with the permissions shown below.

    ================================================   =======
    Resource                                           Action
    ================================================   =======
    ``dcos:adminrouter:service:marathon``              full
    ``dcos:service:marathon:marathon:admin:events``    read
    ``dcos:service:marathon:marathon:services:/``      read
    ================================================   =======

#. Get the certificate for your cluster:

    .. code-block:: bash

       $ curl -k -v https://<cluster-url>/ca/dcos-ca.crt -o dcos-ca.crt

    .. important::

        If you don't provide a server certificate, the |mctlr| won't be able to authenticate to the Marathon API server.

#. Define the ``F5_DC/OS_AUTH_CREDENTIALS`` JSON blob.

    .. important::

        - ``F5_CC_DCOS_AUTH_CREDENTIALS`` is a JSON object, so you'll have to escape all quotes (e.g., ``\"``).
        - Incorrectly formatted keys will cause authentication failures. Denote all newlines (``\n``) in the private key string before removing the line breaks.

    .. code-block:: bash

        "{
            \"scheme\": \"RS256\",
            ## the DC/OS account name
            \"uid\": \"<service_account_name>\",
            ## the cluster login endpoint
            \"login_endpoint\": \"https://<mesos_master>/acs/api/v1/auth/login\",
            ## the contents of the private key you created for the DC/OS account
            \"private_key\": \"<private_key>\"
        }"


#. Add the ``F5_CC_DCOS_AUTH_CREDENTIALS`` and ``F5_CC_MARATHON_CA_CERT`` `Marathon BIG-IP Controller configuration labels </products/connectors/marathon-bigip-ctlr/latest/#configuration-parameters>`_ to the |mctlr| App definition.

    .. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example.json
        :lines: 1-21, 24-26
        :linenos:
        :emphasize-lines: 20-21
