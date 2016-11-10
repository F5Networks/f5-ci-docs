.. rubric:: Overview

Use this guide to deploy a dev stack in `AWS CloudFormation <https://aws.amazon.com/cloudformation/>`_ consisting of the following:

    - the F5 |csi_m|,
    - the F5 |lwp| and |lwpc|,
    - BIG-IP® Virtual Edition (VE),
    - `Mesosphere Enterprise DC/OS <https://mesosphere.com/>`_,
    - `Marathon`_ (container service orchestration platform), and
    - `Splunk`_ (data analysis).

This guide is intended to provide a demonstration of the F5 solution for managing North-South and East-West traffic with Mesos+Marathon.

.. note::

    This guide includes a section on using `Splunk Enterprise <https://www.splunk.com/en_us/download/splunk-enterprise.html>`_ for data analytics and visualization. If you don't already have a Splunk instance, we recommend signing up for the 60-day evaluation program.

.. seealso::

    If you would like to use the F5 |csi_m| in an existing Mesos+Marathon environment, please see the :ref:`User Guide <csim-user-guide>`.



