Python Pulsedive Client
===========================

A low-level client for Pulsedive that aims provide an easy and idiomatic way to interact with the Pulsedive API.


Installation
------------

Install the ``pulsedive`` package with `pip
<https://pypi.org/project/pulsedive/>`_::

    pip install pulsedive


Example use
-----------

Sample Code::

    import pulsedive
    # pud = pulsedive.Pulsedive('<API KEY>')
    pud = pulsedive.Pulsedive()

    # Getting a specific indicator
    ind = pud.indicator(value='pulsedive.com')
    pud.indicator.links(ind['iid'])

    # Searching for indicators
    pud.search('pulsedive', risk=['high', 'critical'], indicator_type=['ip'])

    # Pulling from feeds or threats
    pud.feed.links(1)
    pud.threat.links(1)

    # Searching for threats and feeds
    pud.search.threat('Zeus', risk=['high', 'critical'])
    pud.search.feed('Zeus')

    # Exporting a search
    pud.search.to_csv(filename="zues.csv", threat=['Zeus'], indicator_type=['ip'])

    # Analyzing
    # q = pud.analyze.encoded('Z29vZ2xlLmNvbQ==')
    q = pud.analyze('google.com')
    pud.analyze.results(q['qid'])

Contents
--------

.. toctree::
   :maxdepth: 2

   api
