.. _api:

API Documentation
=================

The API calls tries to map the raw API with reasonable default values
to make it easier for the developers. Some of the default values in the API
are not the default behavior in the actual API. This most evident in the
:class:`~pulsedive.client.SearchClient`

For example, the default behavior of ``limit='hundred'`` is not the default
behavior when no limit is defined. To get all the results set this to None.

Other fields that have default values are ``risk``, ``category``,
``indicator_type``, and ``sanitize``.

.. note::

    For compatibility with the Python ecosystem we use ``properties`` instead of
    ``property``


Global parameters
-----------------

The ``raw``, ``sanitize`` and ``pretty`` parameters can be set
on the instantiation of a
:class:`~pulsedive.Pulsedive`.  This will be set as the default but they can
be overridden in the individual methods calls.

Raw Requests
~~~~~~~~~~~~

For most API calls, the client will return the json of the response.
However, if there is any need for you to handle the raw response, you
can set the `raw` parameter::

    from pulsedive import Pulsedive
    pud = Pulsedive()

    pud.indicator('1', raw=True)
    # <Response [200]>

HTML-Ready Output
~~~~~~~~~~~~~~~~~

You can return HTML-ready results from the API by
including and setting the ``sanitize`` parameter to 1.
By default sanitize is set to 1.

Pretty-Printing
~~~~~~~~~~~~~~~

You can pretty-print results from the API by including and setting the
``pretty`` parameter to 1::

    from pulsedive import Pulsedive
    pud = Pulsedive()

    pud.indicator('1').text
    #{"page_current": 0,"results": [...

    pud.indicator('1', pretty=True).text
    #{
    #   "page_current": 0,
    #   "results": [
    #       {
    #           "iid": "1",
    #           "indicator": "afobal.cl",
    # ....


Pagination
~~~~~~~~~~

Some requests might require going through pages of results.
Described `here.
<https://pulsedive.com/api/?q=paging>`_

In that case, you can set the ``page`` keyword in the method calls::

    from pulsedive import Pulsedive
    pud = Pulsedive(raw=True)

    pud.search(risk=['high', 'critical'], limit=None)
    #{'page_current': 0,
    # 'page_next': 1,
    # 'results': [{'attributes': ['25',
    #    '80',
    # ...

    pud.search(risk=['high', 'critical'], limit=None, page=1)


Pulsedive
---------

.. autoclass:: pulsedive.Pulsedive
   :members:

.. py:module:: pulsedive.client

Indicators
----------

.. autoclass:: IndicatorClient
   :members:

Threats
-------

.. autoclass:: ThreatClient
   :members:

Feeds
-----

.. autoclass:: FeedClient
   :members:

Search
------

.. autoclass:: SearchClient
   :members:

Analyze
-------

.. autoclass:: AnalyzeClient
   :members: __call__, encoded, results

