:orphan: true

Prerequisites
=============

.. INTERNAL USE ONLY
    The following prerequisites can be copied and pasted into any feature document.

- Licensed, operational BIG-IP.

- An existing, functional `Mesos`_ `Marathon`_ deployment.
    .. must include the following at end of document:
        .. _Mesos: https://mesos.apache.org/
        .. _Marathon: https://mesosphere.github.io/marathon/

- Administrator access to both the BIG-IP device(s) and the Mesos/Marathon environment.

- Basic understanding of BIG-IP® `system configuration`_.

- Basic understanding of BIG-IP® `local traffic management`_.

- Knowledge of BIG-IP® `system configuration`_ & `local traffic management`_.

- Mesos tbd

- Marathon tbd

- Internet access


- Licensed, operational BIG-IP (hardware or Virtual Edition).
- Knowledge of BIG-IP `system configuration`_ and `local traffic management`_.
- Administrator access to both the BIG-IP and Marathon. [*]_
- An existing, functional `Mesos`_ `Marathon`_ deployment.
- BIG-IP partitions that correspond to the Marathon apps.
- The official F5 ``f5-marathon-lb`` image pulled from the `F5 Docker registry`_.

.. [*] Admin access to the BIG-IP is only required to create the partitions the CSI will manage. Users with permission to configure objects in the partition can do so via the CSI.