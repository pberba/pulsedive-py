import base64
import shutil
import requests

from .exceptions import PulsediveException

PULSEDIVE_URL = 'https://pulsedive.com/api'

CATEGORIES = ['general', 'abuse', 'apt', 'attack', 'botnet', 'crime',
              'exploitkit', 'fraud', 'group', 'malware', 'proxy', 'pup',
              'reconnaissance', 'spam', 'terrorism', 'phishing', 'vulnerability']
INDICATOR_TYPES = ['ip', 'ipv6', 'url', 'domain', 'artifact']
RISKS = ['unknown', 'none', 'low', 'medium', 'high', 'critical', 'retired']


class IndicatorClient:
    """
    This exposes the Pulsedive `Indicator API
    <https://pulsedive.com/api/?q=indicators>`_
    """
    def __init__(self, pulsedive_client):
        self.pud = pulsedive_client

    def __call__(self, iid=None, value=None, schema=False, **kwargs):
        """
        Queries for an indicator by either indicator id or by value.
        An alias to ``pud.indicator.get()``
        """
        return self.get(iid=iid, value=value, schema=schema, **kwargs)

    def get(self, iid=None, value=None, schema=False, **kwargs):
        """
        Queries for an indicator by either indicator id or by value.

        :arg iid: Used when retrieving by indicator ID
        :arg value: Used when retrieving by value
        :arg schema: `schema` is an optional boolean parameter.
            It's a flag to return associated attributes of the indicator.
            Default: False
        """
        params = {'schema': int(schema)}

        if iid is not None:
            params['iid'] = iid
        elif value is not None:
            params['indicator'] = value
        else:
            raise PulsediveException('"iid" or "value" has to be set')

        return self.pud.get('info.php', params, **kwargs)

    def properties(self, iid, **kwargs):
        """
        Returns historical properties of indicator

        :arg iid: Indicator ID
        """
        params = {
            'iid': iid,
            'get': 'properties'
        }
        return self.pud.get('info.php', params, **kwargs)

    def links(self, iid, **kwargs):
        """
        Returns historical links of indicator

        :arg iid: Indicator ID
        """
        params = {
            'iid': iid,
            'get': 'links'
        }
        return self.pud.get('info.php', params, **kwargs)


class ThreatClient:
    """
    This exposes the Pulsedive `Threat API
    <https://pulsedive.com/api/?q=threats>`_
    """
    def __init__(self, pulsedive_client):
        self.pud = pulsedive_client

    def __call__(self, tid=None, name=None, **kwargs):
        """
        Queries threats by either threat id or by name.
        An alias to ``pud.threat.get()``
        """
        return self.get(tid=tid, name=name, **kwargs)

    def get(self, tid=None, name=None, **kwargs):
        """
        Queries threats by either threat id or by name.

        :arg tid: Used when retrieving by threat ID
        :arg name: Used when retrieving by threat name
        """
        params = {}

        if tid is not None:
            params['tid'] = tid
        elif name is not None:
            params['tname'] = name
        else:
            raise PulsediveException('"tid" or "name" has to be set')

        return self.pud.get('info.php', params, **kwargs)

    def summary(self, tid, splitrisk=False, **kwargs):
        """
        Gives a summary of a threat that gives counts of
        indicators per feed, attribute, etc.

        :arg tid: Threat ID
        :arg splitrisk: Whether to split each indicator count by risk
            categories (none, low, medium, etc.). Default: False
        """
        params = {
            'tid': tid,
            'get': 'links',
            'summary': 1,
            'splitrisk': int(splitrisk)
        }
        return self.pud.get('info.php', params, **kwargs)

    def links(self, tid, **kwargs):
        """
        Returns the linked indicators for the threat

        :arg tid: Threat ID
        """
        params = {
            'tid': tid,
            'get': 'links',
        }
        return self.pud.get('info.php', params, **kwargs)


class FeedClient:
    """
    This exposes the Pulsedive `Feed API
    <https://pulsedive.com/api/?q=feeds>`_
    """
    def __init__(self, pulsedive_client):
        self.pud = pulsedive_client

    def __call__(self, fid=None, feed=None, organization=None, **kwargs):
        """
       Gets data of a feed through its feed ID.
       This is an alias to ``pud.feed.get()``

       :arg fid: Feed ID used when retrieving by fid
       :arg feed: name of the feed used when retrieving by name.
            This has to be the complete name of the field but is not case sensitive.
       :arg organization: optional field when retrieving by name
       """
        return self.get(fid=fid, feed=feed, organization=organization **kwargs)

    def get(self, fid=None, feed=None, organization=None, **kwargs):
        """
        Gets data of a feed through its feed ID.

        This is aliased by the ``__call__`` method so the following lines are equivalent::

            pud.feed.get(1)
            pud.feed(1)
            pud.feed.get(feed='zeus bad domains')
            pud.feed.get(
                feed='Zeus Bad Domains',
                organization='abuse.ch'
            )

        :arg fid: Feed ID used when retrieving by fid
        :arg feed: name of the feed used when retrieving by name.
            This has to be the complete name of the field but is not case sensitive.
        :arg organization: optional field when retrieving by name

        """
        params = {}

        if fid is not None:
            params['fid'] = fid
        elif feed is not None:
            params['feed'] = feed
        else:
            raise PulsediveException('"fid" or "feed" has to be set')

        if organization is not None:
            params['organization'] = organization

        return self.pud.get('info.php', params, **kwargs)

    def links(self, fid, **kwargs):
        """
        Returns the linked indicators for the feed

        :arg fid: Feed ID
        """
        params = {
            'fid': fid,
            'get': 'links',
        }
        return self.pud.get('info.php', params, **kwargs)


class SearchClient:
    """
    Exposes the Pulsedive `Search API
    <https://pulsedive.com/api/?q=search>`_

     .. warning::
        The use of ``properties`` is not yet stable, and untested.

    """
    def __init__(self, pulsedive_client):
        self.pud = pulsedive_client

    # TODO: Lookup default behavior of latest
    # TODO: Lookup how to use property
    def __call__(self, value='', risk=RISKS, indicator_type=INDICATOR_TYPES,
                 lastseen=None, latest=None, limit='hundred', properties=None,
                 attribute=None, feed=None, threat=None, export=False,
                 **kwargs):
        """
        Searches for indicators, an alias of the `.get()` method
        """
        return self.indicator(value=value, risk=risk,
                              indicator_type=indicator_type,
                              lastseen=lastseen, latest=latest, limit=limit,
                              export=export, properties=properties,
                              attribute=attribute, feed=feed,
                              threat=threat, **kwargs)

    def indicator(self, value='', risk=RISKS, indicator_type=INDICATOR_TYPES,
                  lastseen=None, latest=None, limit='hundred', export=False,
                  properties=None, attribute=None, feed=None, threat=None, **kwargs):
        """
        Searches for indicators, similar to how searches are
        done in the Pulsedive Site.

        This is aliased by the ``__call__`` method so the following lines are equivalent::

            pud.search.indicator('Zues')
            pud.search('Zeus')

        :arg value: Search value for the indicator
        :arg risk: Either a value or list of values from the risk types to include
            to include in the search. Defaults to all risk types.
        :arg indicator_type: Either a value or list of values from the indicator
            categories. Defaults to all categories.
        :arg lastseen: Defaults none (All time). Valid values are: 'day',
            'week', 'month' or None (All time)
        :arg latest: Reflects whether to search all properties or just the
            latest properties and can be either latest or historical.
            Defaults to _____??
        :arg properties: List of properties to search for in the indicator.
            Defaults to none.
        :arg attribute: List of attributes to search for in the indicator.
            Defaults to none
        :arg feed: List of feeds to search in. Defaults none
        :arg threat: List of threats to search in. Defaults none.
        :arg limit: Limit on the number of indicators returned by search.
            Defaults to 'hundred'. Valid values are 'hundred', 'thousand',
            'tenthousand', or None. If set to None, the results will be
            paged if too large for one request.
        :arg export: Optional boolean value to convert results to CSV format.
            If set to true, this function will return a `str`, instead of a `dict`
            Defaults False.
        """
        params = {
            'value': value,
            'export': int(export),
            'type[]': indicator_type,
            'risk[]': risk,
            'feed[]': feed or [],
            'threat[]': threat or [],
            'property[]': properties or [],
            'attribute[]': attribute or []
        }

        if lastseen is not None:
            params['lastseen'] = lastseen
        if limit is not None:
            params['limit'] = limit
        if latest is not None:
            params['latest'] = latest

        if export and not kwargs.get('raw', False):
            return self.pud.get('search.php', params=params, raw=True, **kwargs).text
        return self.pud.get('search.php', params=params, **kwargs)

    def threat(self, value='', risk=RISKS, category=CATEGORIES, properties=None,
               attribute=None, splitrisk=False, **kwargs):
        """
        Searches for threats, similar to how searches are done in the Pulsedive Site.

        :arg value: Search value for the threat
        :arg risk: Either a value or list of values from the risk types to include
            to include in the search. Defaults to all risk types.
        :arg category: Either a value or list of values from the threat categories
            to include in the search. Defaults to all threat categories.
        :arg properties: List of properties to search for in the threats. Defaults to none
        :arg attribute: List of attributes to search for in the threats. Defaults to none
        :arg splitrisk: Whether to split each indicator count by risk
            categories (none, low, medium, etc.). Defaults to False
        """
        params = {
            'search': 'threat',
            'value': value,
            'category[]': category,
            'risk[]': risk,
            'property[]': properties or [],
            'attribute[]': attribute or [],
            'splitrisk': int(splitrisk)
        }
        return self.pud.get('search.php', params=params, **kwargs)

    def feed(self, value='', category=CATEGORIES, splitrisk=False, **kwargs):
        """
        Searches for feeds, similar to how searches are done in the Pulsedive Site.

        :arg value: Search value for the feed
        :arg category: Either a value or list of values from the threat categories
            to include in the search. Defaults to all threat categories.
        :arg splitrisk: Whether to split each indicator count by risk
            categories (none, low, medium, etc.). Defaults to False
        """
        params = {
            'search': 'feed',
            'value': value,
            'category[]': category,
            'splitrisk': int(splitrisk)
        }
        return self.pud.get('search.php', params=params, **kwargs)

    def to_csv(self, value='', filename=None, **kwargs):
        """
        Searches for indicators and saves the result to ``filename``.

        All arguments aside from ``filename`` will be passed to ``pud.search.indicator()`` with ``export=True``.

        :arg value: Search value for the indicator
        :arg filename: Destination filename of the csv
        """
        res = self(value=value, raw=True, stream=True, export=True, **kwargs)
        res.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(res.raw, f)


class AnalyzeClient:
    """
    This exposes the Pulsedive `Analyze API
    <https://pulsedive.com/api/?q=analyze>`_
    """
    def __init__(self, pulsedive_client):
        self.pud = pulsedive_client

    def __call__(self, value, enrich=True, probe=False, **kwargs):
        """
        Encodes ``value`` in base64 and submits this encoded value
        to be added to the analyze queue for processing using the
        :meth:`pulsedive.client.AnalyzeClient.encoded`

        `encrich` and `probe` determine whether or note to probe
        the indicator and enrich with Shodan and VirusTotal.

        :param value: Value to be encoded and processed
        :param enrich: Whether to enrich the indicator
        :param probe: Whether to probe the indicator
        """
        encoded = base64.b64encode(value.encode('utf-8'))
        return self.encoded(encoded)

    def encoded(self, value, enrich=True, probe=False, **kwargs):
        """
        Submits ``value``, a base64 encoding of the indicator,
        to be added to the analyze queue for processing.

        `encrich` and `probe` determine whether or note to probe
        the indicator and enrich with Shodan and VirusTotal.

        :param value: Value of your indicator in base64 encoding
        :param enrich: Whether to enrich the indicator
        :param probe: Whether to probe the indicator
        """
        data = {
            'ioc': value,
            'enrich': int(enrich),
            'probe': int(probe)
        }

        return self.pud.post('analyze.php', data=data, **kwargs)

    def results(self, qid, **kwargs):
        """
        Returns the result of the analysis when the indicator has been
        processed.

        If the results are not yet ready, this will raise a
        :class:`~pulsedive.PulsediveException`


        :param qid: Queue ID
        """
        params = {'qid': qid}
        return self.pud.get('analyze.php', params=params, **kwargs)


class Pulsedive:
    """
    Pulsedive low-level client. Provides a straightforward mapping from
    Python to the Pulsedive API.

    `<https://pulsedive.com/api>`_

    The instance has attributes ``indicator``, ``threat``, ``feed``, ``search``,
    and ``analyze`` that provide access to instances of
    :class:`~pulsedive.client.IndicatorClient`,
    :class:`~pulsedive.client.ThreatClient`,
    :class:`~pulsedive.client.FeedClient`,
    :class:`~pulsedive.client.SearchClient`,
    and :class:`~pulsedive.client.AnalyzeClient`, respectively. This is the
    preferred (and only supported) way to get access to those classes and their
    methods.



    :param api_key: This parameter is optional. Pulsedive allows access to
        the API without a key
    :param sanitize: Sets the default `sanitize` option for all requests
    :param pretty: Sets the default `pretty` option for all requests
    :param raw: If set to True, the raw requests
    :param kwargs: Other parameters that will be passed on to all calls to ``Request.get()``
        and ``Request.post()``. Some Request keyword examples are `proxies` and `cert`
    """

    def __init__(self, api_key=None, sanitize=True, pretty=False, raw=False, **kwargs):

        self.api_key = api_key
        self.pretty = pretty
        self.sanitize = sanitize
        self.args = kwargs
        self.raw = raw

        self.indicator = IndicatorClient(self)
        self.threat = ThreatClient(self)
        self.feed = FeedClient(self)
        self.search = SearchClient(self)
        self.analyze = AnalyzeClient(self)

    def __send(self, method, path, params, **kwargs):
        url = '{}/{}'.format(PULSEDIVE_URL, path)
        params['pretty'] = int(kwargs.pop('pretty', self.pretty))
        params['sanitize'] = int(kwargs.pop('sanitize', self.sanitize))
        if self.api_key is not None:
            params['key'] = self.api_key
        if 'page' in kwargs:
            params['page'] = kwargs.pop('page')

        is_raw = kwargs.pop('raw', self.raw)

        args = self.args.copy()
        args.update(kwargs)

        if method == 'GET':
            r = requests.get(url, params=params, **args)
        else:
            r = requests.post(url, data=params, **args)

        if is_raw:
            return r

        r.raise_for_status()
        ret = r.json()
        if 'error' in ret:
            raise PulsediveException('Error encountered with the API with error "{}'.format(ret['error']))
        return ret

    def get(self, path, params, **kwargs):
        return self.__send('GET', path, params, **kwargs)

    def post(self, path, data, **kwargs):
        return self.__send('POST', path, data, **kwargs)
