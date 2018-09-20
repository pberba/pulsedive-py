# TODO: Finish Search Tests
class TestSearch:
    def test_call(self, pud):
        result = pud.search('afobal', lastseen='day', latest='latest')
        assert 'results' in result
        assert 'iid' in result['results'][0]

    def test_indicator(self, pud):
        result = pud.search.indicator('afobal')
        assert 'results' in result
        assert 'iid' in result['results'][0]

    def test_indicator_risk_filter(self, pud):
        result = pud.search.indicator(risk='critical')
        assert 'results' in result
        for e in result['results']:
            assert 'critical' == e['risk']

    def test_indicator_indicator_type_filter(self, pud):
        result = pud.search.indicator(indicator_type='ip')
        assert 'results' in result
        for e in result['results']:
            assert 'ip' == e['type']

    def test_export(self, pud):
        result = pud.search('afobal', export=True)
        assert not isinstance(result, dict)


