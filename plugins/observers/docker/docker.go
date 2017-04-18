package docker

import (
	"sort"
	"strconv"
	"time"

	"github.com/docker/engine-api/client"
	"github.com/docker/engine-api/types"
	"github.com/signalfx/neo-agent/plugins"
	"github.com/signalfx/neo-agent/services"
	"github.com/spf13/viper"
	"golang.org/x/net/context"
)

const (
	pluginType     = "observers/docker"
	defaultHostURL = "unix:///var/run/docker.sock"
	userAgent      = "signalfx-agent"
	version        = "v1.22"
)

// Docker observer plugin
type Docker struct {
	plugins.Plugin
	client *client.Client
}

func init() {
	plugins.Register(pluginType, NewDocker)
}

// NewDocker constructor
func NewDocker(name string, config *viper.Viper) (plugins.IPlugin, error) {
	plugin, err := plugins.NewPlugin(name, pluginType, config)
	if err != nil {
		return nil, err
	}

	docker := &Docker{plugin, nil}
	if err := docker.load(); err != nil {
		return nil, err
	}

	return docker, nil
}

// Reload the docker client
func (docker *Docker) Reload(config *viper.Viper) error {
	docker.Config = config
	return docker.load()
}

func (docker *Docker) load() (err error) {
	defaultHeaders := map[string]string{"User-Agent": userAgent}
	hostURL := defaultHostURL
	if configVal := docker.Config.GetString("hosturl"); configVal != "" {
		hostURL = configVal
	}

	docker.client, err = client.NewClient(hostURL, version, nil, defaultHeaders)
	return err
}

// Discover services from querying docker api
func (docker *Docker) Read() (services.Instances, error) {
	options := types.ContainerListOptions{All: true}
	containers, err := docker.client.ContainerList(context.Background(), options)
	if err != nil {
		return nil, err
	}

	instances := make(services.Instances, 0)

	for _, c := range containers {
		if c.State == "running" {
			serviceContainer := services.NewContainer(c.ID, c.Names, c.Image, "", c.Command, c.State, c.Labels)
			for _, port := range c.Ports {
				servicePort := services.NewPort("", "127.0.0.1", services.PortType(port.Type), uint16(port.PrivatePort), uint16(port.PublicPort))
				id := docker.String() + c.ID + "-" + strconv.Itoa(port.PrivatePort)
				service := services.NewService(id, services.UnknownService, "")
				dims := map[string]string{
					"container_name":  c.Names[0],
					"container_image": c.Image,
				}
				orchestration := services.NewOrchestration("docker", services.DOCKER, dims, services.PUBLIC)
				si := services.NewInstance(id, service, serviceContainer, orchestration, servicePort, time.Now())
				instances = append(instances, *si)
			}
		}
	}

	sort.Sort(instances)

	return instances, nil
}
