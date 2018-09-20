import pytest
import pulsedive


class TestThreat:
    def test_call(self, pud):
        result = pud.threat('1')
        assert result['tid'] == '1'
        assert result['threat'] == 'Zeus'

    def test_get(self, pud):
        result = pud.threat.get('1')
        assert result['tid'] == '1'
        assert result['threat'] == 'Zeus'

    def test_call_by_name(self, pud):
        result = pud.threat(name='Zeus')
        assert result['tid'] == '1'
        assert result['threat'] == 'Zeus'

    def test_get_by_name(self, pud):
        result = pud.threat(name='Zeus')
        assert result['tid'] == '1'
        assert result['threat'] == 'Zeus'

    def test_links(self, pud):
        result = pud.threat.links('1')
        assert 'results' in result
        assert 'iid' in result['results'][0]

    def test_summary(self, pud):
        result = pud.threat.summary('1')
        assert result.keys() == {'risk', 'feeds', 'attributes', 'properties'}
        assert type(result['feeds'][0]['indicators']) != dict

    def test_summary_splitrisk(self, pud):
        result = pud.threat.summary('1', splitrisk=True)
        assert type(result['feeds'][0]['indicators']) == dict

    def test_call_should_error_if_no_iid_or_value(self, pud):
        with pytest.raises(pulsedive.PulsediveException):
            pud.threat()

    def test_get_should_error_if_no_iid_or_value(self, pud):
        with pytest.raises(pulsedive.PulsediveException):
            pud.threat.get()


