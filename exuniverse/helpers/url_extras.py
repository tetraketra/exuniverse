from urllib.parse import urlparse, ParseResult


def url_has_allowed_host_and_scheme(
    url: str, allowed_hosts: str | set[str], require_https: bool = True
) -> bool:
    """
    Use this to validate the `next` url property on a redirection (such as
    after login) to protect against [open redirection](https://portswigger.net/kb/issues/00500100_open-redirection-reflected).
    """

    if url is not None:
        url = url.strip()
    if not url:
        return False
    if url.startswith('///'):
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}

    try:
        url_info: ParseResult = urlparse(url)
        if not url_info.netloc and url_info.scheme:
            return False
        if not url_info.scheme in (['https'] if require_https else ['http', 'https']):
            return False
        if not url_info.hostname in allowed_hosts:
            return False
    except:
        return False

    return True