from autowork_cli.util.apikeyutil import ApiKeyUtil


def test_safe_display_none():
    api_key = None
    safe_api_key = ApiKeyUtil.safe_display(api_key)
    assert safe_api_key is None


def test_safe_display_len_grreat6():
    api_key = 'abcdefghijklmn'
    safe_api_key = ApiKeyUtil.safe_display(api_key)
    assert safe_api_key == 'abcdef**********'


def test_safe_display_len_less6():
    api_key = 'abcd'
    safe_api_key = ApiKeyUtil.safe_display(api_key)
    assert safe_api_key == 'a**********'
