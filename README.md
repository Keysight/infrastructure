# Network Infrastructure as a Graph

Modern AI systems, comprising diverse scale-up and scale-out interconnect topologies that integrate complex heterogeneous components, connected together via diverse means, face a lack of standardized overall infrastructure description. This hinders benchmarking, simulation, and emulation. [infra.proto](keysight_chakra/infra/infra.proto) introduces a graph-based schema to describe AI/HPC infrastructure.

To create an infrastructure as a graph one cna use messages from [infra.proto](keysight_chakra/infra/infra.proto). The messages allow a user to easily create logical infrastructure as vertexes and edges and scale it up and scale it out without duplicating content.

[infra.proto](keysight_chakra/infra/infra.proto) is a Protocol Buffers (Protobuf) message that serves as the core data model for defining and designing the infrastructure. Protobuf is a schema-based, strongly typed format that models data as messages with defined fields and types in a .proto file. This schema enables efficient serialization and deserialization of structured data.

While Protobuf itself uses a compact binary format, the data defined by the Protobuf message can be converted to more human-readable formats such as JSON and YAML. This conversion facilitates easier inspection, configuration, and integration with tools that prefer text-based formats.

In this README, we have extensively used YAML in the examples above due to its readability and suitability for configuration and data serialization tasks. YAML's clear syntax for nested structures and lists makes it an excellent complement to the Protobuf-defined data model.

## Table of Contents:

- [Introduction](#Network-Infrastructure-as-a-Graph)
- [Lets Build Infrastructure](#lets-build-infrastructure)
  - [Building Infrastructure: Creating Device Inventory](#building-infrastructure-creating-device-inventory)
  - [Designing a 4 port switch](#building-infrastructure-defining-a-4-port-switch)
  - [Designing a simple host](#building-infrastructure-design-host-with-a-single-nic)
  - [Defining Links](#building-infrastructure-defining-links)
  - [Creating Device Instances](#building-infrastructure-creating-device-instances)
  - [Connecting Device Instances](#building-infrastructure-connecting-device-instances)
  - [Complete Example](#building-infrastructure-complete-example)
- [Annotating Logical Infrastructure with Physical Attributes](#binding-logical-infrastructure-with-physical-attributes)

## Lets Build Infrastructure

The main steps in designing a network infrastructure using infra.proto is as follows:

- Creating Device Inventory: Here we define the devices and the external links
  - Defining Devices: Here we define a single device, its components and links inside
    - Define Component
    - Define Links to connect the components with-in the device
    - Create Connection between Components using Links
  - Defining Links: Here we define the external links connecting two devices
- Instantiating devices: The idea is using the device definition in the Inventory a blueprint or template create as many devices needed to describe the infrastructure.
- Defining Connections: Creating connections between device instances.

The steps below will guide you in designing a simple network infrastructure having 4 hosts connected to a single switch. For simplicity, we will be using a hypothetical Generic Switch and Host having minimal components architecture.

### Building Infrastructure: Creating Device Inventory

Device inventory is designed to define the type of devices needed to build the infrastructure. The components and links associated with each device type. This acts as a class or a blueprint whose objects/instances can be created and connected. The main motivation is to define once and use at multiple places. This is to optimize the infrastructure in terms of space complexity.

> Note that the entire device does not need to be described in full detail. The level of device detail should be dictated by the needs of the application.

To define a Device:

- use the `Component` message to define individual components (vertexes) that are present in a device
- use the `Component - count` field to scale up the number of components in the device
- use the `Link` message to define different links within the device
- use the `Device` message to contain `Component` and `Link` messages
- use the `Device - connections` field to connect components (vertexes) to each other with an associated link to form an edge
  - the format of a `connections` string is described in the infra.proto file

Now we will be designing a 4 port generic switch as a part of device inventory.

### Building Infrastructure: Defining a 4 port switch

Lets define a simple Generic Switch.
![generic_switch](resources/images/generic_switch_host_diagram/generic_switch.png)

This switch is made of one asic component and four front panel ports. Front panel ports connects with the asic though mii interface.

User can define this switch with two major components inside it:

- port
- asic

This switch uses one type of link to connect between asic and port :

- mii

The switch uses four mii links to connect four different ports with the same asic. So internally the switch has 4 connections.

We can think of these components as nodes in a graph these are connected to each other through an edge. We can generate the definition as:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
inventory:
  devices:
    generic_switch:
      name: generic_switch
      components:
        port-down:
          name: port
          count: 4
          nic:
            ethernet: {}
        asic:
          name: asic
          count: 1
          cpu:
            memory: MEM_RAM
      links:
        mii:
          name: mii
      connections:
        - port.0.mii.asic.0
        - port.1.mii.asic.0
        - port.2.mii.asic.0
        - port.3.mii.asic.0
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "inventory": {
    "devices": {
      "generic_switch": {
        "name": "generic_switch",
        "components": {
          "port-down": {
            "name": "port",
            "count": 4,
            "nic": {
              "ethernet": {}
            }
          },
          "asic": {
            "name": "asic",
            "count": 1,
            "cpu": {
              "memory": "MEM_RAM"
            }
          }
        },
        "links": {
          "mii": {
            "name": "mii"
          }
        },
        "connections": [
          "port.0.mii.asic.0",
          "port.1.mii.asic.0",
          "port.2.mii.asic.0",
          "port.3.mii.asic.0"
        ]
      }
    }
  }
}
```

</details>

<br>

Here, we have defined a generic_switch with two components: asic with a count of 1 and port with a count of 4. Once the components are defined, we can define connection between components with three parts:

`<source>.<link>.<destination>`

The `<source>` contains the source component and its index. The `<destination>` specifies the destination component and its index. The link joins the source and the destination. Therefore, the connection would look something like this:

```
<source>.<src_index>.<link>.<destination>.<dst_index>
```

### Building Infrastructure: Design host with a single nic

Let's design the Host in a similar manner as we designed Switch.

![generic_host](resources/images/generic_switch_host_diagram/generic_host.png)

Our Host has two interconnected components:

- nic
- npu

Again we can think of these components as node in a graph which are connected through an edge or pcie connection in our case. So the host definition will look as given below:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
inventory:
  devices:
    generic_host:
      name: generic_host
      components:
        nic:
          name: nic
          count: 1
          nic:
            ethernet: {}
        npu:
          name: npu
          count: 1
          npu:
            memory: MEM_UNSPECIFIED
      links:
        pcie:
          name: pcie
      connections:
        - npu.0.pcie.nic.0
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "inventory": {
    "devices": {
      "generic_host": {
        "name": "generic_host",
        "components": {
          "nic": {
            "name": "nic",
            "count": 1,
            "nic": {
              "ethernet": {}
            }
          },
          "npu": {
            "name": "npu",
            "count": 1,
            "npu": {
              "memory": "MEM_UNSPECIFIED"
            }
          }
        },
        "links": {
          "pcie": {
            "name": "pcie"
          }
        },
        "connections": ["npu.0.pcie.nic.0"]
      }
    }
  }
}
```

</details>

<br>

### Building Infrastructure: Defining Links

Now our objective is to define a infrastructure build using the switch and hose that we have defined earlier. We want to build an infrastructure that as one switch and four hosts are directly connected to the switch over 100G Ethernet.

![1 rack 4 hosts](resources/images/generic_switch_host_diagram/connected_diagram.png)

So far we have defined a switch and a host. We have not defined the 100G links. So first we define a 100G ethernet link. We can define a link in the following manner:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
inventory:
  links:
  100Gbps:
    name: 100Gbps
    description: 100Gbps ethernet link.
    bandwidth:
      gbps: 100
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "inventory": {
    "links": {
      "100Gbps": {
        "name": "100Gbps",
        "description": "100Gbps ethernet link.",
        "bandwidth": {
          "gbps": 100
        }
      }
    }
  }
}
```

</details>

<br>

Here, we have defined the link with the `name: 100Gbps` which has a bandwidth set to a 100 gbps. Later 4 such links will be used in connecting 4 devices with 4 switch ports, as show in the above picture.

### Building Infrastructure: Creating Device Instances

We can scale the infrastructure by using the `device instance` message. In our example, we would want to connect 4 generic_hosts to a single generic_switch. The idea is to instantiate each of them with a count, so to instantiate 4 `generic_host` as `host`, and one `generic_switch` as a `rack_switch`. We can define the data model as:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
device_instances:
  rack_switch:
    name: rack_switch
    device: generic_switch
    count: 1
  host:
    name: host
    device: generic_host
    count: 4
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "device_instances": {
    "rack_switch": {
      "name": "rack_switch",
      "device": "generic_switch",
      "count": 1
    },
    "host": {
      "name": "host",
      "device": "generic_host",
      "count": 4
    }
  }
}
```

</details>

<br>

The idea is that we have defined the devices under `inventory - devices` section, which acts as a blueprint or template. We need to instantiate them to crate the whole infrastructure - like the way we create objects of a class. With the count specified, it creates multiple copies of the devices starting from index 0.

Now we need to connect these device instances together over 100G ethernet links as shown in the picture above.

### Building Infrastructure: Connecting Device Instances

Connections between the devices are made by the components of the device and links defined. Therefore, to connect two devices together, we need to define the connection in the following format:

```
<src_device>.<dev_index><src_component><comp_index>.<link>.<dst_device>.<dev_index><dst_component><comp_index>
```

The `<src_device>.<dev_index><src_component><comp_index>` contains the source device, index of the device, component within the device, and the index of the component. Same goes for the destination. The Link mainly defines the link between the source and destination.

A "." separator is used to separate between two infrastructure elements. Now to connect a `host` with the `rack_switch` we can define the connection as:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
connections:
  - host.0.nic.0.100Gbps.rack_switch.0.port.0
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "connections": ["host.0.nic.0.100Gbps.rack_switch.0.port.0"]
}
```

</details>

<br>

This means that the host at index 0, through its nic component 0 is connected to port 0 of rack_switch 0. The link between this sour and destination is of 100Gbps. This represents the first link in the above picture.

All 4 link definitions will look like below:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
connections:
  - host.0.nic.0.100Gbps.rack_switch.0.port.0
  - host.1.nic.0.100Gbps.rack_switch.0.port.1
  - host.2.nic.0.100Gbps.rack_switch.0.port.2
  - host.3.nic.0.100Gbps.rack_switch.0.port.3
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "connections": [
    "host.0.nic.0.100Gbps.rack_switch.0.port.0",
    "host.1.nic.0.100Gbps.rack_switch.0.port.1",
    "host.2.nic.0.100Gbps.rack_switch.0.port.2",
    "host.3.nic.0.100Gbps.rack_switch.0.port.3"
  ]
}
```

</details>

<br>

## Building Infrastructure: Complete Example

After combining all the definitions, we can arrive at the final design:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
inventory:
  devices:
    generic_host:
      name: generic_host
      components:
        nic:
          name: nic
          count: 1
          nic:
            ethernet: {}
        npu:
          name: npu
          count: 1
          npu:
            memory: MEM_UNSPECIFIED
      links:
        pcie:
          name: pcie
      connections:
        - npu.0.pcie.nic.0
    generic_switch:
      name: generic_switch
      components:
        port-down:
          name: port
          count: 4
          nic:
            ethernet: {}
        asic:
          name: asic
          count: 1
          cpu:
            memory: MEM_RAM
      links:
        mii:
          name: mii
      connections:
        - port.0.mii.asic.0
        - port.1.mii.asic.0
        - port.2.mii.asic.0
        - port.3.mii.asic.0
  links:
    100Gbps:
      name: 100Gbps
      description: 100Gbps ethernet link.
      bandwidth:
        gbps: 100
device_instances:
  rack_switch:
    name: rack_switch
    device: generic_switch
    count: 1
  host:
    name: host
    device: generic_host
    count: 4
connections:
  - host.0.nic.0.100Gbps.rack_switch.0.port.0
  - host.1.nic.0.100Gbps.rack_switch.0.port.1
  - host.2.nic.0.100Gbps.rack_switch.0.port.2
  - host.3.nic.0.100Gbps.rack_switch.0.port.3
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
{
  "inventory": {
    "devices": {
      "generic_host": {
        "name": "generic_host",
        "components": {
          "nic": {
            "name": "nic",
            "count": 1,
            "nic": {
              "ethernet": {}
            }
          },
          "npu": {
            "name": "npu",
            "count": 1,
            "npu": {
              "memory": "MEM_UNSPECIFIED"
            }
          }
        },
        "links": {
          "pcie": {
            "name": "pcie"
          }
        },
        "connections": ["npu.0.pcie.nic.0"]
      },
      "generic_switch": {
        "name": "generic_switch",
        "components": {
          "port-down": {
            "name": "port",
            "count": 4,
            "nic": {
              "ethernet": {}
            }
          },
          "asic": {
            "name": "asic",
            "count": 1,
            "cpu": {
              "memory": "MEM_RAM"
            }
          }
        },
        "links": {
          "mii": {
            "name": "mii"
          }
        },
        "connections": [
          "port.0.mii.asic.0",
          "port.1.mii.asic.0",
          "port.2.mii.asic.0",
          "port.3.mii.asic.0"
        ]
      }
    },
    "links": {
      "100Gbps": {
        "name": "100Gbps",
        "description": "100Gbps ethernet link.",
        "bandwidth": {
          "gbps": 100
        }
      }
    }
  },
  "device_instances": {
    "rack_switch": {
      "name": "rack_switch",
      "device": "generic_switch",
      "count": 1
    },
    "host": {
      "name": "host",
      "device": "generic_host",
      "count": 4
    }
  },
  "connections": [
    "host.0.nic.0.100Gbps.rack_switch.0.port.0",
    "host.1.nic.0.100Gbps.rack_switch.0.port.1",
    "host.2.nic.0.100Gbps.rack_switch.0.port.2",
    "host.3.nic.0.100Gbps.rack_switch.0.port.3"
  ]
}
```

</details>

<br>

## Binding Logical Infrastructure with Physical Attributes

The main intent of infra.proto is to define and design a logical network fabric. This allows end users to define the devices as nodes and links as edges. The data model also allows us to define and design devices by allowing us to add links and components present in the device. This also models the device internals as a subgraph.

Another data model: annotate.proto allow to define and bind various physical network parameters with the logical infrastructure. The user can bind:

- Vendor specific data
- More qualities of the infrastructure
- Attach certain device performance attributes, like: - Latency - Routing tables
  and helps add more context and content to infrastructure elements.

The core intent is to decouple various bindings with infrastructure, separating the concerns of designing the logical infrastructure with additional data which may not be relevant to external use-cases. This allows the ability to share the infrastructure without the worry and hassle to separate unwanted data or data.

Lets annotate device type to our previous example:

The idea is to add a `Device Type` to our infra devices with the types being `physical_switch`, `physical_host`, `vm_host`, `vm_switch`. This would provide some more insights on what the device type is. Annotating the infrastructure:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
- targets:
    - infrastructure: Infrastructure
  data:
    name: DeviceTypes
    value:
      "@type": type.googleapis.com/google.protobuf.ListValue
      value:
        - device_instance: host
          device_type: physical_host
        - device_instance: rack_switch
          device_type: physical_switch
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
[
  {
    "targets": [
      {
        "infrastructure": "Infrastructure"
      }
    ],
    "data": {
      "name": "DeviceTypes",
      "value": {
        "@type": "type.googleapis.com/google.protobuf.ListValue",
        "value": [
          {
            "device_instance": "host",
            "device_type": "physical_host"
          },
          {
            "device_instance": "rack_switch",
            "device_type": "physical_switch"
          }
        ]
      }
    }
  }
]
```

</details>

<br>

Here, we need to set the target and provide a value. The target is a list of elements defined in the infrastructure. Here we are applying it to the overall infrastructure and the value contains a special schema which defines the device_instance and associates it with a device_type.

> Note: The schema can be internal to an organization.

Another example is to define an `OpenConfigInterface` for our `rack_switch`:

<details open>
<summary><strong>YAML Definition</strong></summary>

```yaml
- targets:
    - device_instance: rack_switch
  data:
    name: OpenConfigInterface
    value:
      "@type": type.googleapis.com/google.protobuf.Struct
      value:
        config:
          type: ...
          mtu: ...
          loopback-mode: ...
          enabled: ...
```

</details>

<br>

<details>
<summary><strong>JSON Definition</strong></summary>

```json
[
  {
    "targets": [
      {
        "device_instance": "rack_switch"
      }
    ],
    "data": {
      "name": "OpenConfigInterface",
      "value": {
        "@type": "type.googleapis.com/google.protobuf.Struct",
        "value": {
          "config": {
            "type": [],
            "mtu": [],
            "loopback-mode": [],
            "enabled": []
          }
        }
      }
    }
  }
]
```

</details>

<br>
