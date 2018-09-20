class TestFeed:
    def test_call(self, pud):
        result = pud.feed('1')
        assert result['fid'] == '1'
        assert result['feed'] == 'Zeus Bad Domains'

    def test_get(self, pud):
        result = pud.feed.get('1')
        assert result['fid'] == '1'
        assert result['feed'] == 'Zeus Bad Domains'

    def test_links(self, pud):
        result = pud.feed.links('1')
        assert 'results' in result
        assert 'iid' in result['results'][0]


