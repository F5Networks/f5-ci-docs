.. list-table:: HTTP Stats
    :header-rows: 1

    * - Name
      - Description
    * - ``client_ip``
      - IP address of the connection associated with this request
    * - ``client_port``
      - TCP port of the connection associated with this request
    * - ``client_user``
      - HTTP basic authentication user
    * - ``ttfb``
      - time-to-first-byte; Time (in milliseconds) between receiving the request and starting to write out the response headers
    * - ``ttlb``
      - time-to-last-byte; time (in milliseconds) between receiving the request and writing out the last byte of the response body
    * - ``response_status_code``
      -  HTTP response code (e.g. 200)
    * - ``http_version``
      - HTTP protocol version used by the client (e.g. "1.1")
    * - ``method_name``
      - HTTP method for this request (e.g., "POST")
    * - ``request_date``
      - Time (in milliseconds) the request was received
    * - ``pool_member_name``
      - ID of the particular server pool member (embeds the server name)
    * - ``pool_member_ip``
      - IP address for the particular server pool member
    * - ``pool_member_port``
      - TCP port of the particular server pool member
    * - ``url``
      - URL for the HTTP request
    * - ``user_agent``
      -  HTTP user agent of the client
    * - ``referrer``
      - HTTP referrer (indicates the originating URI)
    * - ``request_headers_size``
      - Size (in bytes) of the request headers
    * - ``request_body_size``
      - Size (in bytes) of the request body
    * - ``response_headers_size``
      - Size (in bytes) of the response headers
    * - ``response_body_size``
      -  Size (in bytes) of the response body
    * - ``app``
      -  Application name
    * - ``appComponent``
      -  Application component

