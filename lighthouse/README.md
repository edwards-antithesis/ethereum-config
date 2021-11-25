# Overview

This folder has a collection of configuration files and start up scripts for launching a network of containers for testing the Lighthouse Ethereum client.

The configuration in the `docker-compose.yml` file describes the following configuration:

* [Ganache](https://www.trufflesuite.com/ganache) as the underlying Ethereum 1 chain;
* A network of 20 Lighthouse Ethereum nodes – each node is running a validator and a beacon; and
* A workload that exercises the whole system.

# Building the configuration image

## buildah

```
> buildah bud --tag lighthouse-config:latest
```

