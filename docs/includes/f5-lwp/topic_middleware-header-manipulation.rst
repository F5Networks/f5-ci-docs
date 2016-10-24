Header Manipulation Module
~~~~~~~~~~~~~~~~~~~~~~~~~~

The header manipulation module allows you to manipulate HTTP headers for client request (``http.ClientRequest``) and server response (``http.serverResponse``) objects.

via the underlying Node.js header manipulation API. You can manipulate headers

This module provides functionality to manipulate HTTP headers (add,
remove, or modify) using the underlying Node.js header manipulation API
(``setHeader``, ``getHeader``, ``removeHeader``) on the http.ClientRequest and
http.serverResponse objects. LWP has the same semantics for adding
headers as the Node.js ``setHeader`` method, namely:

* Sets a single header value for implicit headers.
* If header already exists, its value will be replaced.
* Use an array of values if you need to send header with multiple values.

