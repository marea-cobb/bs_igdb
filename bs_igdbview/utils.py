from urlparse import urlparse, urlunparse
from django.http import QueryDict


def url_append_parameter(url, attr, val):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[attr] = val
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))


def build_orderby_urls(url, attributes):
    print url
    urls = {}
    for attr in attributes:
        urls[attr] = url_append_parameter(url, "order_by", attr)
    return urls