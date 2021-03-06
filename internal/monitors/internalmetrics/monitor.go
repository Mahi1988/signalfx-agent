package internalmetrics

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/signalfx/golib/datapoint"
	"github.com/signalfx/signalfx-agent/internal/core/config"
	"github.com/signalfx/signalfx-agent/internal/core/meta"
	"github.com/signalfx/signalfx-agent/internal/monitors"
	"github.com/signalfx/signalfx-agent/internal/monitors/types"
	"github.com/signalfx/signalfx-agent/internal/utils"
	log "github.com/sirupsen/logrus"
)

// Config for internal metric monitoring
type Config struct {
	config.MonitorConfig `yaml:",inline" acceptsEndpoints:"true"`

	// Defaults to the top-level `internalStatusHost` option
	Host string `yaml:"host"`
	// Defaults to the top-level `internalStatusPort` option
	Port uint16 `yaml:"port" noDefault:"true"`
	// The HTTP request path to use to retrieve the metrics
	Path string `yaml:"path" default:"/metrics"`
}

// Monitor for collecting internal metrics from the simple server that dumps
// them.
type Monitor struct {
	Output    types.Output
	AgentMeta *meta.AgentMeta
	cancel    func()
}

func init() {
	monitors.Register(monitorType, func() interface{} { return &Monitor{} }, &Config{})
}

// Configure and kick off internal metric collection
func (m *Monitor) Configure(conf *Config) error {

	var ctx context.Context
	ctx, m.cancel = context.WithCancel(context.Background())

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	utils.RunOnInterval(ctx, func() {
		// Derive the url each time since the AgentMeta data can change but
		// there is no notification system for it.
		host := conf.Host
		if host == "" {
			host = m.AgentMeta.InternalStatusHost
		}

		port := conf.Port
		if port == 0 {
			port = m.AgentMeta.InternalStatusPort
		}

		url := fmt.Sprintf("http://%s:%d%s", host, port, conf.Path)

		logger := log.WithFields(log.Fields{
			"monitorType": monitorType,
			"url":         url,
		})

		resp, err := client.Get(url)
		if err != nil {
			logger.WithError(err).Error("Could not connect to internal metric server")
			return
		}
		defer resp.Body.Close()

		dps := make([]*datapoint.Datapoint, 0)
		err = json.NewDecoder(resp.Body).Decode(&dps)
		if err != nil {
			logger.WithError(err).Error("Could not parse metrics from internal metric server")
			return
		}

		for _, dp := range dps {
			m.Output.SendDatapoint(dp)
		}
	}, time.Duration(conf.IntervalSeconds)*time.Second)

	return nil
}

// Shutdown the internal metric collection
func (m *Monitor) Shutdown() {
	if m.cancel != nil {
		m.cancel()
	}
}
