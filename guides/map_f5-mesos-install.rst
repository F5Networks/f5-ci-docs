.. _index:

F5 Container Services Installation
=========

.. todo::

  Place some Mesos/Marathon prerequistes? Like enable Docker containerization, etc?

Both the f5-marathon-lb and lightweight-proxy-controller run as dockerized container applications inside of Marathon.

In order to retrieve the corresponding images during the F5 Intregration for Mesos Environments beta, you will need to the proper authorization to access the private docker images in the F5 Networks repository.

From the command line on your sysytem, add the following to your local docker configuration file, $HOME/.docker/config.json with the following:

.. code:: javascript

  {
    "auths": {
      "https://index.docker.io/v1/": {
        "auth": "ZjViZXRhdXNlcjpjOURUS3RBVnQyZHc="
      }
    }
  }%

For Windows users, the file is located at *%HOME%\.docker\config.json*

.. include:: includes/topic_f5-mesos-csi-install.rst
.. include:: includes/topic_f5-mesos-lwp-install.rst
