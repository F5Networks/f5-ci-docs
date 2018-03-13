Source Address Translation
==========================

Source address translation can be configured on individual virtual servers for both the marathon and k8s BIG-IP controllers.
This is done in marathon by providing an app label on a service. This is done in k8s and openshift through configmaps or
through annotations. Annotations are used to configure source address translation for ingresses in k8s and for ingresses and
routes in openshift. Configmap configurations are used in both k8s and openshift. For an overview on source address
translation see the following article: https://support.f5.com/csp/article/K7820. There are three types of source address
translation that can be configured on virtual servers. Those types are automap, none, and snat. For an overview of types see
https://support.f5.com/csp/article/K7820#Types. By default automap source address translation type is configured on virtual
servers. The following examples show how source address translation can be configured by controller:

Marathon
--------

Example automap (default) App Label:

"F5_<#>_SOURCE_ADDR_TRANSLATION": "{\"type\":\"automap\"}"

where <#> is the virtual server index

Example none App Label:

F5_<#>_SOURCE_ADDR_TRANSLATION": "{\"type\":\"none\"}"

Example snat App Label:

"F5_<#>_SOURCE_ADDR_TRANSLATION": "{\"type\":\"snat\",\"pool\":\"snat-pool\"}"

Kubernetes and Openshift
------------------------

Example virtual server with automap (default) Configmap (k8s and openshift):

"virtualServer": {
  "frontend": {
    "balance": "round-robin",
    "mode": "http",
    "partition": "kubernetes",
    "virtualAddress": {
      "bindAddr": "1.2.3.4",
      "port": 443
    },
    "sslProfile": {
      "f5ProfileName": "Common/testcert"
    },
    "sourceAddressTranslation": {"type": "automap"}
  }
}

Example virtual server with none Configmap (k8s and openshift):

"virtualServer": {
  "frontend": {
    "balance": "round-robin",
    "mode": "http",
    "partition": "kubernetes",
    "virtualAddress": {
      "bindAddr": "1.2.3.4",
      "port": 443
    },
    "sslProfile": {
      "f5ProfileName": "Common/testcert"
    },
    "sourceAddressTranslation": {"type": "none"}
  }
}

Example virtual server with snat Configmap (k8s and openshift):

"virtualServer": {
  "frontend": {
    "balance": "round-robin",
    "mode": "http",
    "partition": "kubernetes",
    "virtualAddress": {
      "bindAddr": "1.2.3.4",
      "port": 443
    },
    "sslProfile": {
      "f5ProfileName": "Common/testcert"
    },
    "sourceAddressTranslation": {
      "type": "snat",
      "pool": "snat-pool"
    }
  }
}

Example automap (default) Annotation (k8s ingress, openshift ingress/route):

virtual-server.f5.com/source-addr-translation: |
  {"type": "automap"}

Example none Annotation (k8s ingress, openshift ingress/route):

virtual-server.f5.com/source-addr-translation: |
  {"type": "none"}

Example snat Annotation (k8s ingress, openshift ingress/route):
virtual-server.f5.com/source-addr-translation: |
  {
    "type": "snat",
    "pool": "snat-pool"
  }

Note:
If using type snat the pool field must be the name of a preconfigured SNAT pool otherwise the virtual server being
configured will not be created. SNAT pools should be created in the Common partition on the BIG-IP so an example SNAT name
would be:

"pool": "Common/my-snat-pool"
