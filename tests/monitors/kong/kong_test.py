from functools import partial as p
from textwrap import dedent

import pytest
from tests.helpers.agent import Agent
from tests.helpers.assertions import container_cmd_exit_0, has_datapoint_with_dim, http_status, tcp_socket_open
from tests.helpers.util import container_ip, run_container, run_service, wait_for

pytestmark = [pytest.mark.collectd, pytest.mark.kong, pytest.mark.monitor_with_endpoints]


@pytest.mark.flaky(reruns=2, reruns_delay=5)
@pytest.mark.parametrize("kong_version", ["0.13-centos", "0.14-centos", "0.15-centos", "1.0.0-centos"])
def test_kong(kong_version):  # pylint: disable=redefined-outer-name
    pg_env = dict(POSTGRES_USER="kong", POSTGRES_PASSWORD="kong", POSTGRES_DB="kong")
    kong_env = dict(
        KONG_ADMIN_LISTEN="0.0.0.0:8001",
        KONG_LOG_LEVEL="warn",
        KONG_DATABASE="postgres",
        KONG_PG_DATABASE=pg_env["POSTGRES_DB"],
        KONG_PG_PASSWORD=pg_env["POSTGRES_PASSWORD"],
    )

    with run_container("postgres:9.5", environment=pg_env) as db:
        db_ip = container_ip(db)
        kong_env["KONG_PG_HOST"] = db_ip

        assert wait_for(p(tcp_socket_open, db_ip, 5432))

        with run_service(
            "kong", buildargs={"KONG_VERSION": kong_version}, environment=kong_env, command="sleep inf"
        ) as migrations:
            if kong_version in ["0.15-centos", "1.0.0-centos"]:
                assert container_cmd_exit_0(migrations, "kong migrations bootstrap")
            else:
                assert container_cmd_exit_0(migrations, "kong migrations up")

        with run_service("kong", buildargs={"KONG_VERSION": kong_version}, environment=kong_env) as kong:
            kong_ip = container_ip(kong)
            assert wait_for(p(http_status, url=f"http://{kong_ip}:8001/signalfx", status=[200]))
            config = dedent(
                f"""
            monitors:
              - type: collectd/kong
                host: {kong_ip}
                port: 8001
                metrics:
                  - metric: connections_handled
                    report: true
            """
            )
            with Agent.run(config) as agent:
                assert wait_for(
                    p(has_datapoint_with_dim, agent.fake_services, "plugin", "kong")
                ), "Didn't get Kong data point"
