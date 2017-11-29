
def test_cache():
    from moon_utilities import cache
    c = cache.Cache()
    assert isinstance(c.authz_requests, dict)
