import time
import pytest
import pulsedive


class TestAnalyze:
    def test_call(self, pud):
        q = pud.analyze('pulsedive.com')
        assert 'qid' in q

        # If too early, should error
        with pytest.raises(pulsedive.PulsediveException):
            pud.analyze.results(q['qid'])

        time.sleep(10)

        result = pud.analyze.results(q['qid'])
        assert 'success' in result
        assert result['data']['indicator'] == 'pulsedive.com'

    def test_encoded(self, pud):
        # Encoding of google.com
        q = pud.analyze.encoded('Z29vZ2xlLmNvbQ==')
        assert 'qid' in q

        # If too early, should error
        with pytest.raises(pulsedive.PulsediveException):
            pud.analyze.results(q['qid'])

        # time.sleep(10)
        #
        # result = pud.analyze.results(q['qid'])
        # assert 'success' in result
        # assert result['data']['indicator'] == 'google.com'

