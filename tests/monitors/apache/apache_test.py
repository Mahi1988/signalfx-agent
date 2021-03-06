"""
Tests for the collectd/apache monitor
"""
import string
from functools import partial as p

import pytest
from tests.helpers.agent import Agent
from tests.helpers.assertions import has_datapoint_with_dim, tcp_socket_open
from tests.helpers.util import container_ip, run_service, wait_for

pytestmark = [pytest.mark.collectd, pytest.mark.apache, pytest.mark.monitor_with_endpoints]

APACHE_CONFIG = string.Template(
    """
monitors:
  - type: collectd/apache
    host: $host
    port: 80
"""
)


def test_apache():
    with run_service("apache") as apache_container:
        host = container_ip(apache_container)
        config = APACHE_CONFIG.substitute(host=host)
        assert wait_for(p(tcp_socket_open, host, 80), 60), "service didn't start"

        with Agent.run(config) as agent:
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "apache")
            ), "Didn't get apache datapoints"
