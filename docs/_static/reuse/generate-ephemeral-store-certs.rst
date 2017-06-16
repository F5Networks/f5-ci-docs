#. Create the Root Certificate Authority for the ephemeral store.
   This is a self-signed rootCA certificate and key.

   .. code-block:: console

      openssl genrsa -out rootCA.key 2048
      openssl req -new -key rootCA.key -out rootCA.csr -subj "/CN=rootCA"
      openssl x509 -req -days 365 -in rootCA.csr -signkey rootCA.key -out rootCA.crt

#. Create certificates for users.
   The ephemeral store uses these certificates to authenticate with the server.

   .. attention::

      - The common name (``/CN``) should match a username defined in the ``ephemeral store.user`` configuration parameter. [#ephemstoreconfig]_
      - Use the Root Certificate to sign the user certificates (line 3 in the example below).

   \

   .. code-block:: console

      openssl genrsa -out myuser.key 2048
      openssl req -new -key myuser.key -out myuser.csr -subj "/CN=myuser"
      openssl x509 -req -days 365 -in myuser.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out myuser.crt


.. [#ephemstoreconfig] See the `ASP product documentation`_ for a full list of ASP ephemeral store configuration parameters.
