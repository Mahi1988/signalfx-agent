from functools import partial as p
from textwrap import dedent

import pytest

from tests.helpers.agent import Agent
from tests.helpers.assertions import (
    has_datapoint_with_dim,
    has_datapoint_with_metric_name,
    has_log_message,
    http_status,
)
from tests.helpers.util import container_ip, run_service, wait_for

pytestmark = [pytest.mark.collectd, pytest.mark.elasticsearch, pytest.mark.monitor_with_endpoints]


@pytest.mark.flaky(reruns=2)
def test_elasticsearch_without_cluster_option():
    with run_service("elasticsearch/6.4.2", environment={"cluster.name": "testCluster"}) as es_container:
        host = container_ip(es_container)
        assert wait_for(
            p(http_status, url=f"http://{host}:9200/_nodes/_local", status=[200]), 180
        ), "service didn't start"
        config = dedent(
            f"""
            monitors:
            - type: collectd/elasticsearch
              host: {host}
              port: 9200
              username: elastic
              password: testing123
            """
        )
        with Agent.run(config) as agent:
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "Didn't get elasticsearch datapoints"
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin_instance", "testCluster")
            ), "Cluster name not picked from read callback"
            assert not has_log_message(agent.output.lower(), "error"), "error found in agent output!"


@pytest.mark.flaky(reruns=2)
def test_elasticsearch_with_cluster_option():
    with run_service("elasticsearch/6.4.2", environment={"cluster.name": "testCluster"}) as es_container:
        host = container_ip(es_container)
        assert wait_for(
            p(http_status, url=f"http://{host}:9200/_nodes/_local", status=[200]), 180
        ), "service didn't start"
        config = dedent(
            f"""
            monitors:
            - type: collectd/elasticsearch
              host: {host}
              port: 9200
              username: elastic
              password: testing123
              cluster: testCluster1
            """
        )
        with Agent.run(config) as agent:
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "Didn't get elasticsearch datapoints"
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin_instance", "testCluster1")
            ), "Cluster name not picked from read callback"
            # make sure all plugin_instance dimensions were overridden by the cluster option
            assert not wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin_instance", "testCluster"), 10
            ), "plugin_instance dimension not overridden by cluster option"
            assert not has_log_message(agent.output.lower(), "error"), "error found in agent output!"


# To mimic the scenario where node is not up
@pytest.mark.flaky(reruns=2)
def test_elasticsearch_without_cluster():
    # start the ES container without the service
    with run_service(
        "elasticsearch/6.4.2", environment={"cluster.name": "testCluster"}, entrypoint="sleep inf"
    ) as es_container:
        host = container_ip(es_container)
        config = dedent(
            f"""
            monitors:
            - type: collectd/elasticsearch
              host: {host}
              port: 9200
              username: elastic
              password: testing123
            """
        )
        with Agent.run(config) as agent:
            assert not wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "datapoints found without service"
            # start ES service and make sure it gets discovered
            es_container.exec_run("/usr/local/bin/docker-entrypoint.sh eswrapper", detach=True)
            assert wait_for(
                p(http_status, url=f"http://{host}:9200/_nodes/_local", status=[200]), 180
            ), "service didn't start"
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "Didn't get elasticsearch datapoints"


@pytest.mark.flaky(reruns=2)
def test_elasticsearch_with_threadpool():
    with run_service("elasticsearch/6.2.0", environment={"cluster.name": "testCluster"}) as es_container:
        host = container_ip(es_container)
        assert wait_for(
            p(http_status, url=f"http://{host}:9200/_nodes/_local", status=[200]), 180
        ), "service didn't start"
        config = dedent(
            f"""
            monitors:
            - type: collectd/elasticsearch
              host: {host}
              port: 9200
              username: elastic
              password: testing123
              threadPools:
               - bulk
               - index
               - search
            """
        )
        with Agent.run(config) as agent:
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "Didn't get elasticsearch datapoints"
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "thread_pool", "bulk")
            ), "Didn't get bulk thread pool metrics"
            assert not has_log_message(agent.output.lower(), "error"), "error found in agent output!"


@pytest.mark.flaky(reruns=2)
def test_elasticsearch_with_additional_metrics():
    with run_service("elasticsearch/6.2.0", environment={"cluster.name": "testCluster"}) as es_container:
        host = container_ip(es_container)
        assert wait_for(
            p(http_status, url=f"http://{host}:9200/_nodes/_local", status=[200]), 180
        ), "service didn't start"
        config = dedent(
            f"""
            monitors:
            - type: collectd/elasticsearch
              host: {host}
              port: 9200
              username: elastic
              password: testing123
              additionalMetrics:
               - cluster.initializing-shards
               - thread_pool.threads
            """
        )
        with Agent.run(config) as agent:
            assert wait_for(
                p(has_datapoint_with_dim, agent.fake_services, "plugin", "elasticsearch")
            ), "Didn't get elasticsearch datapoints"
            assert wait_for(
                p(has_datapoint_with_metric_name, agent.fake_services, "gauge.cluster.initializing-shards")
            ), "Didn't get gauge.cluster.initializing-shards metric"
            assert wait_for(
                p(has_datapoint_with_metric_name, agent.fake_services, "gauge.thread_pool.threads")
            ), "Didn't get gauge.thread_pool.threads metric"
            assert not has_log_message(agent.output.lower(), "error"), "error found in agent output!"
