:orphan: true

Glossary
========

.. glossary::
    :sorted:

    middleware
        In the context of the lightweight proxy, 'middleware' refers to functions that run in the Express routing layer, thus sitting between the request and response. [#]_ See :term:`Express middleware`.

    Express
        A web framework for Node.js; see https://expressjs.com/.

    Express middleware
        Express middleware consists of functions that have access to the request object (req), the response object (res), and the next middleware function in the application’s request-response cycle. [#]_

    built-in middleware
        Middleware functions that are built in to an application.


.. rubric:: Footnotes
.. [#] http://expressjs.com/en/resources/glossary.html
.. [#] https://expressjs.com/en/guide/using-middleware.html
