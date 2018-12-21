from __future__ import unicode_literals

import newrelic.agent


def record_search_query_params(params):
    """
    Send search params to New Relic as "attributes" on each transaction.

    Only the first 255 characters of the value are retained and values must
    be str, int, float, or bool types.

    Disclaimer: If there are multiple values for a single key, only
    submit the first value to NewRelic as there is no way of submitting
    multiple values for a single attribute and submitting a list of values
    would not be condusive to data aggregation.


    :arg params: the request params to record
    :type params: webob.multidict.MultiDict
    """
    keys = [
        # Record usage of inefficient offset and it's alternative search_after.
        "offset",
        "search_after",
        "sort",
        # Record usage of url/uri (url is an alias of uri).
        "url",
        "uri",
        # Record usage of tags/tag (tags is an alias of tag).
        "tags",
        "tag",
        # Record usage of _separate_replies which will help distinguish client calls
        # for loading the sidebar annotations from other api calls.
        "_separate_replies",
        # Record group and user-these help in identifying slow queries.
        "group",
        "user",
        # Record usage of wildcard feature.
        "wildcard_uri",
    ]
    # The New Relic Query Language does not permit _ at the begining
    # and offset is a reserved key word.
    params = [("es_{}".format(k), params[k]) for k in keys if k in params]
    newrelic.agent.current_transaction().add_custom_parameters(params)
