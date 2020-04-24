TLS 1.3 Support using AS3
=========================

CIS now supports TLS 1.3 using AS3. This page will show you how to use TLS 1.3 and Cipher groups in CIS using AS3 and how to add TLS 1.3 support to the `TLS_Server` profile. It also shows you how to enable TLS 1.3 support in a declaration when using TMOS 14.1.0.1 and later.

.. sidebar:: :fonticon:`fa fa-info-circle fa-lg` Version notice:

    - AS3 only supports TLS 1.3 in TMOS version 14.0.0 and higher
    - AS3 version 3.17.0 or later supports TLS 1.3

Notes:

- If you are using TLS 1.3, you MUST include a cipher group. However, using cipher groups does not require TLS 1.3. The default value for cipher group is `f5-default`.
- If you are using TLS 1.2, you can specify the cipher string for ciphersuite selection.
- `ciphers` and `cipher group` are mutually exclusive, only use one.

See the `AS3 schema reference <https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/refguide/schema-reference.html>`_ for usage.


Configure TLS 1.3 in CIS
------------------------

#. Configure TLS version to be enabled on BIG-IP with the following command. The default value is ``1.2``.

   ::

        --tls-version=<1.2 or 1.3>


#. Configure a Cipher Group on the BIG-IP system and reference it using the following command. The default path is ``/Common/f5-default``.

   ::

        --cipher-group=<Complete path to BIG-IP Cipher Group>


#. Configure a ciphersuite selection string using the following command with colon-separated values, for example ``ECDHE_ECDSA:ECDHE``. The default value is DEFAULT.

   ::
        
        --ciphers=<colon separated values. eg: ECDHE_ECDSA:ECDHE>
