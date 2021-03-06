<!--- GENERATED BY gomplate from scripts/docs/monitor-page.md.tmpl --->

# appmesh

This monitor starts a StatsD monitor to listen to StatsD metrics emitted
by AWS AppMesh Envoy Proxy.

To report AppMesh Envoy metrics, you need to enable Envoy StatsD sink on AppMesh
and deploy the agent as a sidecar in the services that need to be monitored.


Sample Envoy StatsD configuration:

```yaml
stats_sinks:
 -
  name: "envoy.statsd"
  config:
   address:
    socket_address:
     address: "127.0.0.1"
     port_value: 8125
     protocol: "UDP"
   prefix: statsd.appmesh
```
Please remember to provide the prefix to the agent monitor configuration.

See [Envoy API reference](https://www.envoyproxy.io/docs/envoy/latest/api-v2/config/metrics/v2/stats.proto#envoy-api-msg-config-metrics-v2-statsdsink) for more info

Sample SignalFx SmartAgent configuration:

```yaml
monitors:
 - type: appmesh
   listenAddress: 0.0.0.0
   listenPort: 8125
   metricPrefix: statsd.appmesh
```


Monitor Type: `appmesh`

[Monitor Source Code](https://github.com/signalfx/signalfx-agent/tree/master/internal/monitors/appmesh)

**Accepts Endpoints**: No

**Multiple Instances Allowed**: Yes

## Configuration

| Config option | Required | Type | Description |
| --- | --- | --- | --- |
| `listenAddress` | no | `string` | The host/address on which to bind the UDP listener that accepts statsd datagrams (**default:** `localhost`) |
| `listenPort` | no | `integer` | The port on which to listen for statsd messages (**default:** `8125`) |
| `metricPrefix` | no | `string` | A prefix in metric names that needs to be removed before metric name conversion |




## Metrics

The following table lists the metrics available for this monitor. Metrics that are marked as Included are standard metrics and are monitored by default.

| Name | Type | Included | Description |
| ---  | ---  | ---    | ---         |
| `circuit_breakers.<priority>.cx_open` | gauge |  | Whether the connection circuit breaker is closed (0) or open (1) |
| `circuit_breakers.<priority>.cx_pool_open` | gauge |  | Whether the connection pool circuit breaker is closed (0) or open (1) |
| `circuit_breakers.<priority>.remaining_cx` | gauge |  | Number of remaining connections until the circuit breaker opens |
| `circuit_breakers.<priority>.remaining_pending` | gauge |  | Number of remaining pending requests until the circuit breaker opens |
| `circuit_breakers.<priority>.remaining_retries` | gauge |  | Number of remaining retries until the circuit breaker opens |
| `circuit_breakers.<priority>.remaining_rq` | gauge |  | Number of remaining requests until the circuit breaker opens |
| `circuit_breakers.<priority>.rq_open` | gauge |  | Whether the requests circuit breaker is closed (0) or open (1) |
| `circuit_breakers.<priority>.rq_pending_open` | gauge |  | Whether the pending requests circuit breaker is closed (0) or open (1) |
| `circuit_breakers.<priority>.rq_retry_open` | gauge |  | Whether the retry circuit breaker is closed (0) or open (1) |
| `external.upstream_rq_<_>` | cumulative |  | External origin specific HTTP response codes |
| `external.upstream_rq_<_xx>` | cumulative |  | External origin aggregate HTTP response codes |
| `external.upstream_rq_completed` | cumulative |  | Total external origin requests completed |
| `external.upstream_rq_time` | gauge |  | External origin request time milliseconds |
| `internal.upstream_rq_<_>` | cumulative |  | Internal origin specific HTTP response codes |
| `internal.upstream_rq_<_xx>` | cumulative |  | Internal origin aggregate HTTP response codes |
| `internal.upstream_rq_completed` | cumulative |  | Total internal origin requests completed |
| `internal.upstream_rq_time` | gauge |  | Internal origin request time milliseconds |
| `membership_change` | cumulative |  | Total cluster membership changes |
| `membership_degraded` | gauge |  | Current cluster degraded total |
| `membership_healthy` | gauge | ✔ | Current cluster healthy total (inclusive of both health checking and outlier detection) |
| `membership_total` | gauge | ✔ | Current cluster membership total |
| `upstream_cx_active` | gauge |  | Total active connections |
| `upstream_cx_close_notify` | cumulative |  | Total connections closed via HTTP/1.1 connection close header or HTTP/2 GOAWAY |
| `upstream_cx_connect_attempts_exceeded` | cumulative |  | Total consecutive connection failures exceeding configured connection attempts |
| `upstream_cx_connect_fail` | cumulative |  | Total connection failures |
| `upstream_cx_connect_ms` | gauge |  | Connection establishment milliseconds |
| `upstream_cx_connect_timeout` | cumulative |  | Total connection connect timeouts |
| `upstream_cx_destroy` | cumulative |  | Total destroyed connections |
| `upstream_cx_destroy_local` | cumulative |  | Total connections destroyed locally |
| `upstream_cx_destroy_local_with_active_rq` | cumulative |  | Total connections destroyed locally with 1+ active request |
| `upstream_cx_destroy_remote` | cumulative |  | Total connections destroyed remotely |
| `upstream_cx_destroy_remote_with_active_rq` | cumulative |  | Total connections destroyed remotely with 1+ active request |
| `upstream_cx_destroy_with_active_rq` | cumulative |  | Total connections destroyed with 1+ active request |
| `upstream_cx_http1_total` | cumulative |  | Total HTTP/1.1 connections |
| `upstream_cx_http2_total` | cumulative |  | Total HTTP/2 connections |
| `upstream_cx_idle_timeout` | cumulative |  | Total connection idle timeouts |
| `upstream_cx_length_ms` | gauge |  | Connection length milliseconds |
| `upstream_cx_max_requests` | cumulative |  | Total connections closed due to maximum requests |
| `upstream_cx_none_healthy` | cumulative |  | Total times connection not established due to no healthy hosts |
| `upstream_cx_overflow` | cumulative |  | Total times that the cluster’s connection circuit breaker overflowed |
| `upstream_cx_pool_overflow` | cumulative |  | Total times that the cluster’s connection pool circuit breaker overflowed |
| `upstream_cx_protocol_error` | cumulative |  | Total connection protocol errors |
| `upstream_cx_rx_bytes_buffered` | gauge |  | Received connection bytes currently buffered |
| `upstream_cx_rx_bytes_total` | cumulative | ✔ | Total received connection bytes |
| `upstream_cx_total` | cumulative |  | Total connections |
| `upstream_cx_tx_bytes_buffered` | gauge |  | Send connection bytes currently buffered |
| `upstream_cx_tx_bytes_total` | cumulative |  | Total sent connection bytes |
| `upstream_rq_<_>` | cumulative | ✔ | Specific HTTP response codes (e.g., 201, 302, etc.) |
| `upstream_rq_<_xx>` | cumulative | ✔ | Aggregate HTTP response codes (e.g., 2xx, 3xx, etc.) |
| `upstream_rq_active` | gauge |  | Total active requests |
| `upstream_rq_cancelled` | cumulative |  | Total requests cancelled before obtaining a connection pool connection |
| `upstream_rq_completed` | cumulative | ✔ | Total upstream requests completed |
| `upstream_rq_maintenance_mode` | cumulative |  | Total requests that resulted in an immediate 503 due to maintenance mode |
| `upstream_rq_pending_active` | gauge |  | Total active requests pending a connection pool connection |
| `upstream_rq_pending_failure_eject` | cumulative |  | Total requests that were failed due to a connection pool connection failure |
| `upstream_rq_pending_overflow` | cumulative |  | Total requests that overflowed connection pool circuit breaking and were failed |
| `upstream_rq_pending_total` | cumulative |  | Total requests pending a connection pool connection |
| `upstream_rq_per_try_timeout` | cumulative |  | Total requests that hit the per try timeout |
| `upstream_rq_retry` | cumulative | ✔ | Total request retries |
| `upstream_rq_retry_overflow` | cumulative |  | Total requests not retried due to circuit breaking |
| `upstream_rq_retry_success` | cumulative | ✔ | Total request retry successes |
| `upstream_rq_rx_reset` | cumulative |  | Total requests that were reset remotely |
| `upstream_rq_time` | gauge | ✔ | Request time milliseconds |
| `upstream_rq_timeout` | cumulative |  | Total requests that timed out waiting for a response |
| `upstream_rq_total` | cumulative |  | Total requests |
| `upstream_rq_tx_reset` | cumulative |  | Total requests that were reset locally |


To specify custom metrics you want to monitor, add a `metricsToInclude` filter
to the agent configuration, as shown in the code snippet below. The snippet
lists all available custom metrics. You can copy and paste the snippet into
your configuration file, then delete any custom metrics that you do not want
sent.

Note that some of the custom metrics require you to set a flag as well as add
them to the list. Check the monitor configuration file to see if a flag is
required for gathering additional metrics.

```yaml

metricsToInclude:
  - metricNames:
    - circuit_breakers.<priority>.cx_open
    - circuit_breakers.<priority>.cx_pool_open
    - circuit_breakers.<priority>.remaining_cx
    - circuit_breakers.<priority>.remaining_pending
    - circuit_breakers.<priority>.remaining_retries
    - circuit_breakers.<priority>.remaining_rq
    - circuit_breakers.<priority>.rq_open
    - circuit_breakers.<priority>.rq_pending_open
    - circuit_breakers.<priority>.rq_retry_open
    - external.upstream_rq_<_>
    - external.upstream_rq_<_xx>
    - external.upstream_rq_completed
    - external.upstream_rq_time
    - internal.upstream_rq_<_>
    - internal.upstream_rq_<_xx>
    - internal.upstream_rq_completed
    - internal.upstream_rq_time
    - membership_change
    - membership_degraded
    - upstream_cx_active
    - upstream_cx_close_notify
    - upstream_cx_connect_attempts_exceeded
    - upstream_cx_connect_fail
    - upstream_cx_connect_ms
    - upstream_cx_connect_timeout
    - upstream_cx_destroy
    - upstream_cx_destroy_local
    - upstream_cx_destroy_local_with_active_rq
    - upstream_cx_destroy_remote
    - upstream_cx_destroy_remote_with_active_rq
    - upstream_cx_destroy_with_active_rq
    - upstream_cx_http1_total
    - upstream_cx_http2_total
    - upstream_cx_idle_timeout
    - upstream_cx_length_ms
    - upstream_cx_max_requests
    - upstream_cx_none_healthy
    - upstream_cx_overflow
    - upstream_cx_pool_overflow
    - upstream_cx_protocol_error
    - upstream_cx_rx_bytes_buffered
    - upstream_cx_total
    - upstream_cx_tx_bytes_buffered
    - upstream_cx_tx_bytes_total
    - upstream_rq_active
    - upstream_rq_cancelled
    - upstream_rq_maintenance_mode
    - upstream_rq_pending_active
    - upstream_rq_pending_failure_eject
    - upstream_rq_pending_overflow
    - upstream_rq_pending_total
    - upstream_rq_per_try_timeout
    - upstream_rq_retry_overflow
    - upstream_rq_rx_reset
    - upstream_rq_timeout
    - upstream_rq_total
    - upstream_rq_tx_reset
    monitorType: appmesh
```




