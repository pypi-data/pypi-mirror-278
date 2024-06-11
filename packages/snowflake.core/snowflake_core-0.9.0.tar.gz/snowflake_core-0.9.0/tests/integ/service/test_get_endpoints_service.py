#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


def test_get_endpoints(services, temp_service):
    res = services[temp_service.name].get_endpoints()
    endpoints = list(res)
    assert len(endpoints) == 1

    endpoint = endpoints[0]
    assert endpoint.name == "default"
    assert endpoint.port == 8080
    assert endpoint.protocol == "HTTP"
    assert not endpoint.is_public
