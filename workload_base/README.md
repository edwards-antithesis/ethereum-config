Sources used to create the Python 3.8-based workload base image. 

The intention is that the base image has all the required libraries needed by the workload but excludes any workload directly. This allows the workload to be provided independently and volume mounted into the base image to run. Doing this avoids having the rebuild the workload base image every time there is a change in the workload.

To build:
```
$ buildah --registries-conf=registries.conf bud python38_workload_base
```

