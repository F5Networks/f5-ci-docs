:product: Container Ingress Services
:type: concept

.. _kctlr-as3-cert-trust:

Updating the Container Ingress Service (CIS) trusted SSL certificate store
==========================================================================

You can use the CIS trusted SSL certificate store to establish trust between CIS, and your remote BIG-IP systems.

To establish trust, add the BIG-IP device certificate, or the Certificate Authority's (CA) signing certificate to the CIS trusted SSL certificate store.

.. important::

   If you connect to the BIG-IP system using an IP address, instead of a hostname, you must add the IP address to the Common Name (CN), and Subject Alternative Name (SAN) certificate attributes.

   CIS cannot currently establish trust using Private IP addresses.

----

.. _as3-add-device-cert:

Add a certificate to the CIS trusted SSL certificate store
----------------------------------------------------------

You can add either a BIG-IP device certificate, or the CA signing certificate to the trusted SSL certificate store. 

In this procedure, you will Secure copy (SCP) a BIG-IP system device certificate to the Kubernetes master node, add it to the CIS trusted SSL certificate store, and restart the CIS controller.

Prerequisites
`````````````
- The ability to Secure copy (SCP) files from the BIG-IP system.
- Command line access to the Kubernetes master node.

#. Log in to the command line of the master node.

#. Secure copy (SCP) the BIG-IP device certificate to the local working directory. 

   .. parsed-literal::

      scp root@<IP|Hostname>:/config/httpd/conf/ssl.crt/server.crt ./<cert name>.crt   

   For example:

   .. parsed-literal::

      scp root@192.168.10.100:/config/httpd/conf/ssl.crt/server.crt ./bigip1.crt      
     
#. Add the device certificate to the CIS trusted certificate store.

   .. parsed-literal::

      kubectl create configmap <configmap name> --from-file=<cert name>.crt -n <name space>

   For example, to add a single BIG-IP device cert:

   .. parsed-literal::

      kubectl create configmap bigip1cert --from-file=bigip1.crt -n k8s

   For example, to add multiple BIG-IP device certs:

   .. parsed-literal::

      kubectl create configmap bigipcerts --from-file=bigip1.crt --from-file=bigip2.crt --from-file=bigip3.crt -n k8s

#. Reference the CIS trusted certificate store in your configurations when executing Kubernetes deployments.

   .. parsed-literal::

      --trusted-certs-cfgmap=<name space>/<configmap name>

   For example:

   .. parsed-literal::

      args: [ 
              "--bigip-username=$(BIGIP_USERNAME)",
              "--bigip-password=$(BIGIP_PASSWORD)",
              "--bigip-url=192.168.10.100",
              "--trusted-certs-cfgmap=k8s/bigipcerts"
            ]

#. Apply the new configuration to the Kubernetes deployment.

   .. parsed-literal:: 

      kubectl apply -f <deployment name> -n <name space> 

      For example:

      kubectl apply -f k8scontroller.yaml -n <name space> 

#. Restart the controller.

   .. note::

      You can restart the controller by deleting the k8s-bigip-ctlr Pod. A new Pod deploys automatically, thanks to the `ReplicaSet`_.

   .. parsed-literal::

      kubectl get pod --namespace=kube-system | grep bigip-ctlr
         k8s-bigip-ctlr-deployment-bf9c75877-zhzpp    1/1     Running             0          15d

      kubectl delete pod k8s-bigip-ctlr-deployment-bf9c75877-zhzpp --namespace=kube-system
                    
----         
      
.. _as3-add-root-cert:

Create a Certificate Authority (CA) and sign a new BIG-IP device certificate
----------------------------------------------------------------------------

This method for establishing trust between CIS and BIG-IP systems works well when you manage mulitple BIG-IP systems. This method also improves SSL certificate management, offering more control over certificate attributes such as key size, message digest, and expiration date.

Prerequisites
`````````````
- A Linux based workstation with the OpenSSL package installed.
- The ability to Secure copy (SCP) files to and from the BIG-IP system.
- Command line access to Kubernetes master node.

.. important::

   If you access the BIG-IP system using an IP address, ensure you add the IP address to both the Common Name (CN), and SAN field.

Create a root CA and sign a new BIG-IP device certificate
`````````````````````````````````````````````````````````
In this procedure, you will use OpenSSL to create a new Root CA signing certificate, and sign a new BIG-IP device certificate.

#. Log in to the Linux workstation command line.

#. Create a working directory to store the CA root certificate and key.

   .. parsed-literal::

      mkdir <directory>

   For example:

   .. parsed-literal::

      mkdir bigipCa

#. Change to the CA directory.

   .. parsed-literal::

      cd <directory>

   For example:

   .. parsed-literal::

      cd bigipCa
      
#. Determine the OpenSSL configuration file directory.

   .. parsed-literal::

      openssl version -a

   In this example, the location is /etc/pki/tls:

   .. parsed-literal::

      OPENSSLDIR: "/etc/pki/tls"

#. Copy the openssl.cnf file to the CA signing directory:

   .. parsed-literal::

      cp /path/to/openssl.cnf .

   For example:

   .. parsed-literal::

      cp /etc/pki/tls/openssl.cnf .

#. Edit the openssl.cnf file, and ensure the configuration agrees with the example openssl.cnf information.

   .. important::

      You will create the CA certificate and private_key files in step 9. If you prefer to use a different name than bigipCa, modify the openssl.cnf file accordingly, and use the new name when creating the signing certificate and key in step 9.

   Example openssl.cnf

   .. parsed-literal::

      [ CA_default ]

      dir              = .                    # Where everything is kept                            
      new_certs_dir    = $dir                 # default place for new certs

      certificate      = $dir/bigipCa.crt    # The CA certificate
      private_key      = $dir/bigipCa.key    # The private key

      default_days = 3650                     # how long to certified for
      default_md   = sha256                   # use public key default MD

      policy = policy_anything

      [ policy_anything ]

      countryName             = optional
      stateOrProvinceName     = optional
      organizationName        = optional
      organizationalUnitName  = optional
      commonName              = supplied
      emailAddress            = optional

      [ req ]

      default_bits            = 2048
      default_md              = sha256

      [ v3_req ]

      basicConstraints = CA:FALSE
      keyUsage = nonRepudiation, digitalSignature, keyEncipherment, keyCertSign, keyAgreement, dataEncipherment, cRLSign
      extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection

      [ v3_ca ]

      basicConstraints = CA:TRUE
      keyUsage = nonRepudiation, digitalSignature, keyEncipherment, keyCertSign, keyAgreement, dataEncipherment, cRLSign

#. Optional step: If you connect to the BIG-IP system using an IP address, you must add the subject alternative name (SAN) attribute with the IP address of the BIG-IP system to the bottom of [ v3_req ] section.
   
   .. parsed-literal::

      subjectAltName = @alt_names

      [ alt_names ]
      DNS.1 = <IP address>

   For example:

   .. parsed-literal::

      [ v3_req ]

      basicConstraints = CA:FALSE
      keyUsage = nonRepudiation, digitalSignature, keyEncipherment, keyCertSign, keyAgreement, dataEncipherment, cRLSign
      extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection

      subjectAltName = @alt_names

      [ alt_names ]
      DNS.1 = 192.168.10.100

#. Save the file.

#. Create the necessary CA serial, and index.txt files.

   .. note::

      The index.txt file contains the list of signed SSL certificates. The serial file is the source of SSL certificate serial numbers that increments by 1 with each signing.

   .. parsed-literal::

      echo 100000 > serial
      touch index.txt

#. Create the root CA signing certificate and key.

   .. note::

      This command requires that you answer a series of questions. The pass phrase protects the CA key, and you must enter the passphrase each time you sign a new BIG-IP device certificate. Store the passphrase in a safe place. 

   .. parsed-literal::

      openssl req -new -x509 -extensions v3_ca -newkey rsa:4096 -keyout <key name>.key -out <cert name>.crt -days 3650 -config ./openssl.cnf

   For example:
      
   .. parsed-literal::

      openssl req -new -x509 -extensions v3_ca -newkey rsa:4096 -keyout bigipCa.key -out bigipCa.crt -days 3650 -config ./openssl.cnf
      
#. Create a new directory to store signed BIG-IP device certificates.

   .. parsed-literal::
   
      mkdir <directory>

   For example:
   
   .. parsed-literal::

      mkdir signedBigipCerts

#. Create a certificate signing request (CSR) for the new BIG-IP device certificate.

   .. note::
      
      This command requires that you answer a series of the questions. When prompted for a challenge password, you can type Enter for no password.

   .. important::

      The Common Name must match the IP address, or the hostname you use in the Kubernetes deployment.

   .. parsed-literal::

      openssl req -new -nodes -out <directory>/<csr name>.req -keyout <directory>/<key name>.key -config ./openssl.cnf 

   For example:

   .. parsed-literal::

      openssl req -new -nodes -out signedBigipCerts/bigip1.req -keyout signedBigipCerts/bigip1.key -config ./openssl.cnf 

#. Sign the new CSR with the root CA certificate.

   .. parsed-literal::

      openssl ca -out <directory>/<cert name>.crt -config ./openssl.cnf -extensions v3_req -infiles <directory>/<csr name>.req

   For example:

   .. parsed-literal::

      openssl ca -out signedBigipCerts/bigip1.crt -config ./openssl.cnf -extensions v3_req -infiles signedBigipCerts/bigip1.req

   The command output appears similar to:
   
   .. parsed-literal::

      Enter pass phrase for ./bigipCa.key:

      Certificate is to be certified until May 26 22:32:10 2029 GMT (3650 days)

      Sign the certificate? [y/n]:y

      1 out of 1 certificate requests certified, commit? [y/n]y

Repeat steps 12 and 13 this procedure to create, and sign additional BIG-IP device certificates.

Replace the BIG-IP system device certificate
````````````````````````````````````````````
In this procedure, you will back up and replace the BIG-IP system's self-signed device certificate. The procedure assumes that you are working from the same workstation used in the previous procedure, and you have Secure Shell (SSH) access to the BIG-IP system.

.. note::

   If the BIG-IP system has the DNS module license, connectivity to peer BIG-IP DNS systems will fail. You must exchange the new certificate with the BIG-IP DNS peers. For more inforation, refer to the **Sync group peer** section of `K16951115 Changing the BIG-IP DNS system device certificate using the Configuration utility`_.

#. From the Linux workstation, change into the root CA working directory.

   .. parsed-literal::

      cd <directory>

   For example:

   .. parsed-literal::
  
      cd bigiCa

#. Create a new directory to save the BIG-IP system's self-signed device certificate.

   .. parsed-literal::

      mkdir <directory>

   For example:

   .. parsed-literal::

      mkdir oldBigipCerts

#. Copy the current self-signed device certificate and key from the BIG-IP system, to the new directory.

   .. parsed-literal::

      scp root@<IP|Hostname>:/config/httpd/conf/ssl.crt/server.crt <directory>/<cert name>.crt
      scp root@<IP|Hostname>:/config/httpd/conf/ssl.key/server.key <directory>/<key name>.key

   For example:

   .. parsed-literal::
   
      scp root@192.168.10.100:/config/httpd/conf/ssl.crt/server.crt oldBigipCerts/bigip1.bak.crt 
      scp root@192.168.10.100:/config/httpd/conf/ssl.key/server.key oldBigipCerts/bigip1.bak.key

#. Upload the new signed device certificate and key to the BIG-IP system.

   .. parsed-literal::

      scp <directory>/<cert name>.crt root@<IP | Hostname>:/config/httpd/conf/ssl.crt/server.crt
      scp <directory>/<key name>.key root@<IP | Hostname>:/config/httpd/conf/ssl.key/server.key

   For example:

   .. parsed-literal::

      scp signedBigipCerts/bigip1.crt root@192.168.10.100:/config/httpd/conf/ssl.crt/server.crt
      scp signedBigipCerts/bigip1.key root@192.168.10.100:/config/httpd/conf/ssl.key/server.key

#. Secure Shell (SSH) to the BIG-IP system.

   .. parsed-literal::

      ssh root@<IP|Hostname>      

   For example:

   .. parsed-literal::

      ssh root@192.168.10.100
      
#. Log in to the BIG-IP system's TMOS Shell (tmsh).

   .. note::

      Some user accounts may log directly in to tmsh. If your current prompt shows **(tmos)**, you are already in the TMOS Shell (tmsh).

   .. parsed-literal::

      tmsh
      
#. Apply the new device certificate and key.

   .. parsed-literal::

      modify sys httpd { ssl-certkeyfile /config/httpd/conf/ssl.key/server.key ssl-certfile /config/httpd/conf/ssl.crt/server.crt }

#. Save the configuration changes.

   .. parsed-literal::

      save sys config

#. Restart the httpd process.

   .. parsed-literal::

      restart sys service httpd

#. Verify the new certificate is in place.

   .. parsed-literal::

      echo | openssl s_client -connect localhost:443 | openssl x509 -noout -text | less

   The Not Before entry represents when you created the new certificate. The CN and Subject Alternative Name must match if you connect to BIG-IP using an IP address.

   .. parsed-literal::

      Validity
        Not Before: May 29 22:32:10 2019 GMT
        Not After : May 26 22:32:10 2029 GMT

        Subject: C=US, ST=WA, O=F5, OU=Tech, CN=192.168.10.100

      X509v3 Subject Alternative Name:
        DNS:192.168.10.100

Add the CA signing certificate to the CIS trusted SSL certificate store
```````````````````````````````````````````````````````````````````````

In this procedure, you will Secure copy (SCP) the CA signing certificate to the master node, add it to the CIS trusted SSL certificate store, and restart the CIS controller.

#. Log in to the command line of your container orchestration environment (COE).

#. Secure copy (SCP) the CA signing certificate to the local working directory. 

   .. parsed-literal::

      scp root@<IP|Hostname>:/path/to/file.crt      

   For example:

   .. parsed-literal::

      scp root@192.168.10.100:/root/bigipCa/bigipCa.crt .      
     
#. Add the CA signing certificate to the CIS trusted SSL certificate store.

   .. parsed-literal::

      kubectl create configmap <configmap name> --from-file=<cert name>.crt

   For example, to add a single CA signing certificate:

   .. parsed-literal::

      kubectl create configmap bigip-cacert --from-file=bigipCa.crt

   For example, to add multiple CA signing certificates:

   .. parsed-literal::

      kubectl create configmap ca-certs --from-file=bigipCa.crt --from-file=anotherCaCert.crt

#. Reference the CIS trusted SSL certificate store in your configurations when executing Kubernetes deployments.

   .. parsed-literal::

      --trusted-certs-cfgmap=<nameSpace>/<configmap name>

   For example:

   .. parsed-literal::

      args: [ 
              "--bigip-username=$(BIGIP_USERNAME)",
              "--bigip-password=$(BIGIP_PASSWORD)",
              "--bigip-url=192.168.10.100",
              "--trusted-certs-cfgmap=default/bigip-cacert"
            ]

#. Apply the new configuration to the Kubernetes deployment.

   .. parsed-literal:: 

      kubectl apply -f <deployment name> -n <name space> 

      For example:

      kubectl apply -f k8scontroller.yaml -n <name space> 

#. Restart the controller.

   .. note::

      You can restart the controller by deleting the k8s-bigip-ctlr Pod. A new Pod deploys automatically, thanks to the `ReplicaSet <https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/>`_.

   .. parsed-literal::

      kubectl get pod --namespace=kube-system | grep bigip-ctlr
         k8s-bigip-ctlr-deployment-bf9c75877-zhzpp    1/1     Running             0          15d

      kubectl delete pod k8s-bigip-ctlr-deployment-bf9c75877-zhzpp --namespace=kube-system

----

.. _as3-device-san-cert:

Create a new BIG-IP device certificate using the configuration utility
----------------------------------------------------------------------

The BIG-IP system's configuration utility offers an easy way to renew, and if necessary, add an IP address to the SAN attribute of the device certificate.

In this procedure, you will renew the BIG-IP system's device certificate and add an IP address to both the CN, and SAN ceritificate attributes.

.. note::

   If the BIG-IP system has the DNS module license, connectivity to peer BIG-IP DNS systems will fail. You must exchange the new certificate with the BIG-IP DNS peers. For more inforation, refer to the **Sync group peer** section of `K16951115 Changing the BIG-IP DNS system device certificate using the Configuration utility`_.


#. Log in to the BIG-IP system configuration utility.

#. Navigate to **System > Certificate Management > Device Certificate Management > Device Certificate**.

#. Click **Renew**. 

#. Fill out the Certificate Properties. If you connect to the BIG-IP systems using an IP address, add the IP address to the **Common Name**, and **Subject Alternative Name** fields.

   For example:

   +------------------------------+------------------------+
   | **Common Name**              | **192.168.10.100**     |
   +------------------------------+------------------------+
   | **Subject Alternative Name** | **DNS:192.168.10.100** | 
   +------------------------------+------------------------+

#. Click **Finished**.
   
 
Additional information
----------------------

- `Overview of BIG-IP device certificates`_ 
