
def test_cache():
    from moon_utilities import cache
    c = cache.Cache()
    r = c.authz_requests()
    assert isinstance(r, dict)
