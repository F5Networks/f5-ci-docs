Deploy the |lwpc|
-----------------

The |lwpc| component of the CSI is packaged in a container and runs in the Marathon environment. It listens to Marathon events related to the management of applications. If an application that it controls is spun up or down, the |lwpc| will insert or remove the |lwp| in front of the application, providing east-west management of that particular app.

    .. note::

        * We use a curl command here; you may substitute the command of your choice (e.g., ``wget``).
        * You will need to substitute the appropriate Splunk values from :ref:`Install and Configure Splunk` in the JSON blob.

#. :ref:`Install the Lightweight Proxy Controller <lwpc-deploy-guide-install>`.

#. Go to your Marathon UI and watch the app creation.

#. Click on the application called ``lwp-controller`` to view its details.
