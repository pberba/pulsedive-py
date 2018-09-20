import pytest
import pulsedive


class TestIndicator:
    def test_call(self, pud):
        result = pud.indicator('1')
        assert result['iid'] == '1'
        assert result['indicator'] == 'afobal.cl'

    def test_get(self, pud):
        result = pud.indicator.get('1')
        assert result['iid'] == '1'
        assert result['indicator'] == 'afobal.cl'

    def test_no_schema(self, pud):
        result = pud.indicator('1')
        assert 'schema' not in result

    def test_with(self, pud):
        result = pud.indicator.get('1', schema=True)
        assert 'schema' in result

    def test_call_by_name(self, pud):
        result = pud.indicator(value='afobal.cl')
        assert result['indicator'] == 'afobal.cl'

    def test_get_by_name(self, pud):
        result = pud.indicator.get(value='afobal.cl')
        assert result['indicator'] == 'afobal.cl'

    def test_links(self, pud):
        result = pud.indicator.links('1')
        assert 'Active DNS' in result

    def test_properties(self, pud):
        result = pud.indicator.properties('1')
        assert 'dns' in result
        assert 'whois' in result

    def test_call_should_error_if_no_iid_or_value(self, pud):
        with pytest.raises(pulsedive.PulsediveException):
            pud.indicator()

    def test_get_should_error_if_no_iid_or_value(self, pud):
        with pytest.raises(pulsedive.PulsediveException):
            pud.indicator.get()


