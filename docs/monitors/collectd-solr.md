<!--- GENERATED BY gomplate from scripts/docs/monitor-page.md.tmpl --->

# collectd/solr

Monitors Solr instances.

See https://github.com/signalfx/collectd-solr and
https://github.com/signalfx/integrations/tree/master/collectd-solr

Sample YAML configuration:

```yaml
monitors:
- type: collectd/solr
  host: 127.0.0.1
  port: 8983
```


Monitor Type: `collectd/solr`

[Monitor Source Code](https://github.com/signalfx/signalfx-agent/tree/master/internal/monitors/collectd/solr)

**Accepts Endpoints**: **Yes**

**Multiple Instances Allowed**: Yes

## Configuration

| Config option | Required | Type | Description |
| --- | --- | --- | --- |
| `host` | **yes** | `string` |  |
| `port` | **yes** | `integer` |  |
| `cluster` | no | `string` | Cluster name of this solr cluster. |
| `enhancedMetrics` | no | `bool` | EnhancedMetrics boolean to indicate whether stats from /metrics are needed (**default:** `false`) |
| `includeMetrics` | no | `list of strings` | IncludeMetrics metric names from the /admin/metrics endpoint to include (valid when EnhancedMetrics is "false") |
| `excludeMetrics` | no | `list of strings` | ExcludeMetrics metric names from the /admin/metrics endpoint to exclude (valid when EnhancedMetrics is "true") |




## Metrics

The following table lists the metrics available for this monitor. Metrics that are marked as Included are standard metrics and are monitored by default.

| Name | Type | Included | Description |
| ---  | ---  | ---    | ---         |
| `counter.solr.http_2xx_responses` | counter | ✔ | Total number of 2xx http responses |
| `counter.solr.http_4xx_responses` | counter | ✔ | Total number of 4xx http responses |
| `counter.solr.http_5xx_responses` | counter | ✔ | Total number of 5xx http responses |
| `counter.solr.jvm_classes_loaded` | counter |  | Number of JVM classes loaded |
| `counter.solr.node_collections_requests` | counter | ✔ | Number of collection level requets to Solr node |
| `counter.solr.node_cores_requests` | counter | ✔ | Number of core level requets to Solr node |
| `counter.solr.node_metric_request_count` | counter |  | Number of metric requests |
| `counter.solr.node_metrics_requests` | counter | ✔ | Number of metrics level requets to Solr node |
| `counter.solr.node_zookeeper_requests` | counter | ✔ | Number of zookeeper level requets to Solr node |
| `counter.solr.openFileDescriptorCount` | counter |  | Number of open file descriptors |
| `counter.solr.replication_handler_requests` | counter |  | Number of replication handler requets |
| `counter.solr.search_query_requests` | counter | ✔ | Number of search query requests |
| `counter.solr.update_handler_requests` | counter | ✔ | Number of update handler requets |
| `counter.solr.zookeeper_errors` | counter |  | Number of failures/error at Zookeeper |
| `gauge.solr.core_deleted_docs` | gauge | ✔ | Number of deleted docs in Solr core |
| `gauge.solr.core_index_size` | gauge | ✔ | Size of a core index |
| `gauge.solr.core_max_docs` | gauge | ✔ | Total number of docs in Sor core |
| `gauge.solr.core_num_docs` | gauge | ✔ | Total number of indexed docs in Sor core |
| `gauge.solr.core_totalspace` | gauge | ✔ | Total space allocated for core |
| `gauge.solr.core_usablespace` | gauge | ✔ | Usable space available in core |
| `gauge.solr.document_cache_cumulative_hitratio` | gauge | ✔ | Cummulative hit ration of document cache |
| `gauge.solr.field_value_cache_cumulative_hitratio` | gauge | ✔ | Cummulative hit ration of filed value cache |
| `gauge.solr.http_active_requests` | gauge |  | Number of http active requests |
| `gauge.solr.jetty_get_request_latency` | gauge |  | Time to process http get request |
| `gauge.solr.jetty_post_request_latency` | gauge |  | Time to process http post request |
| `gauge.solr.jetty_request_latency` | gauge | ✔ | Http request response time |
| `gauge.solr.jvm_gc_cms_count` | gauge | ✔ | JVM Garbage Collector - CMS invocation count |
| `gauge.solr.jvm_gc_cms_time` | gauge | ✔ | JVM Garbage Collector - CMS prcoess time |
| `gauge.solr.jvm_gc_parnew_count` | gauge | ✔ | JVM Garbage Collector - Parnew invocation count |
| `gauge.solr.jvm_gc_parnew_time` | gauge | ✔ | JVM Garbage Collector - Parnew process time |
| `gauge.solr.jvm_heap_usage` | gauge | ✔ | JVM Heap usage |
| `gauge.solr.jvm_mapped_memory_capacity` | gauge |  | Total JVM mapped memory capacity |
| `gauge.solr.jvm_mapped_memory_used` | gauge |  | Total JVM mapped memory used |
| `gauge.solr.jvm_memory_pools_Code-Cache_usage` | gauge | ✔ | JVM memory pools - PCode Cache usage |
| `gauge.solr.jvm_memory_pools_Metaspace_usage` | gauge | ✔ | JVM memory pools - Metaspace usage |
| `gauge.solr.jvm_memory_pools_Par-Eden-Space_usage` | gauge | ✔ | JVM memory pools - Par Eden space usage |
| `gauge.solr.jvm_memory_pools_Par-Survivor-Space_usage` | gauge | ✔ | JVM memory pools - Par Survivor space usage |
| `gauge.solr.jvm_total_memory` | gauge | ✔ | JVM total memory allocated |
| `gauge.solr.jvm_total_memory_used` | gauge | ✔ | JVM memory used |
| `gauge.solr.node_metric_request_time` | gauge |  | Time to process a metric request |
| `gauge.solr.query_result_cache_cumulative_hitratio` | gauge | ✔ | Cummulative hit ration of query cache |
| `gauge.solr.replication_handler_response` | gauge |  | Resplication handler response time |
| `gauge.solr.search_query_response` | gauge | ✔ | Search query response time |
| `gauge.solr.searcher_warmup` | gauge | ✔ | Time to new searcher to warm up |
| `gauge.solr.update_request_handler_response` | gauge | ✔ | Update request handler response time |
| `gauge.solr.zookeeper_request_time` | gauge |  | Time to process a request at zookeeper |


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
    - counter.solr.jvm_classes_loaded
    - counter.solr.node_metric_request_count
    - counter.solr.openFileDescriptorCount
    - counter.solr.replication_handler_requests
    - counter.solr.zookeeper_errors
    - gauge.solr.http_active_requests
    - gauge.solr.jetty_get_request_latency
    - gauge.solr.jetty_post_request_latency
    - gauge.solr.jvm_mapped_memory_capacity
    - gauge.solr.jvm_mapped_memory_used
    - gauge.solr.node_metric_request_time
    - gauge.solr.replication_handler_response
    - gauge.solr.zookeeper_request_time
    monitorType: collectd/solr
```




