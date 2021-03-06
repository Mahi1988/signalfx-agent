import string
from functools import partial as p

import pytest
from tests.helpers.agent import Agent
from tests.helpers.assertions import has_datapoint_with_metric_name, tcp_socket_open
from tests.helpers.util import container_ip, run_service, wait_for

pytestmark = [pytest.mark.collectd, pytest.mark.cassandra, pytest.mark.monitor_with_endpoints]


CASSANDRA_CONFIG = string.Template(
    """
monitors:
  - type: collectd/cassandra
    host: $host
    port: 7199
    username: cassandra
    password: cassandra
"""
)


@pytest.mark.flaky(reruns=2)
def test_cassandra():
    with run_service("cassandra") as cassandra_cont:
        host = container_ip(cassandra_cont)
        config = CASSANDRA_CONFIG.substitute(host=host)

        # Wait for the JMX port to be open in the container
        assert wait_for(p(tcp_socket_open, host, 7199), 60), "Cassandra JMX didn't start"

        with Agent.run(config) as agent:
            assert wait_for(
                p(
                    has_datapoint_with_metric_name,
                    agent.fake_services,
                    "counter.cassandra.ClientRequest.Read.Latency.Count",
                ),
                60,
            ), "Didn't get Cassandra datapoints"
