# Network Infrastructure as a Graph

Modern AI systems, comprising diverse scale-up and scale-out interconnect topologies that integrate complex heterogeneous components, connected together via diverse means, face a lack of standardized overall infrastructure description. This hinders benchmarking, simulation, and emulation. [infra.proto](keysight_chakra/infra/infra.proto) introduces a graph-based schema to describe AI/HPC infrastructure.

To create an infrastructure as a graph one can use messages from [infra.proto](keysight_chakra/infra/infra.proto). The messages allow a user to easily create logical infrastructure as vertexes and edges. This can be scale up further to describe a massive infrastructure without duplicating content.

[infra.proto](keysight_chakra/infra/infra.proto) is a Protocol Buffers (Protobuf) message that serves as the core data model for defining and designing the infrastructure. Protobuf is a schema-based, strongly typed format that models data as messages with defined fields and types in a .proto file. This schema enables efficient serialization and deserialization of structured data.

While Protobuf itself uses a compact binary format, protobuf data can be converted to human-readable formats like JSON and YAML for easier inspection, configuration, and integration with text-based tools. This README uses YAML for its readability and suitability for configuration and data serialization tasks. YAML's clear syntax for nested structures and lists complements the Protobuf-defined data model.

## Table of Contents:

- [Lets Build Infrastructure](#lets-build-infrastructure)
  - [Creating Device Inventory](#building-infrastructure-creating-device-inventory)
  - [Designing a 4 port switch](#building-infrastructure-defining-a-4-port-switch)
  - [Designing a simple host](#building-infrastructure-design-host-with-a-single-nic)
  - [Defining Links](#building-infrastructure-defining-links)
  - [Creating Device Instances](#building-infrastructure-creating-device-instances)
  - [Connecting Device Instances](#building-infrastructure-connecting-device-instances)
  - [Complete Example](#building-infrastructure-complete-example)
- [Annotating Logical Infrastructure with Physical Attributes](#binding-logical-infrastructure-with-physical-attributes)

## Lets Build Infrastructure

The main steps in designing a network infrastructure using infra.proto is as follows:

- Creating Inventory: Here we define the devices type and the external links type that will be used to describe the infrastructure. 
  - Defining Devices: Here we define a single device for each device type that is present in the infrastructure, its inside  components and links inside
    - Define Component 
    - Define Links to connect the components with-in the device
    - Create Connection between Components using Links
  - Defining External Links: Here we define the external link type that connects two devices

- Building the infrastructure as graph
  - Instantiating devices: Use the device definition in the inventory as a template to create multiple devices for the infrastructure.
  - Defining connections: Use the external link definition to create connections between device instances.
  

Follow these steps to design a basic network with 4 hosts connected to one switch. For simplicity we will use a basic Generic Switch and Host architecture for simplicity.

### Creating Device Inventory

Device inventory outlines the necessary devices for infrastructure, including components and links. It acts as a blueprint to create and connect instances, aiming to define once and reuse multiple times for optimal space complexity. For example, in a network with 100 switches (50 each of 2 types) connected by 100G Ethernet links, the inventory will only specify the 2 switch types and the 100G Ethernet link type.

> Note that the entire device does not need to be described in full detail. The level of device detail should be dictated by the needs of the application.

To define a Device:

- use the `Component` message to define individual components (vertexes) that are present in a device
- use the `Component - count` field to scale up the number of components in the device
- use the `Link` message to define different link types within the device
- use the `Device` message to contain `Component` and `Link` messages
- use the `Device - connections` field to connect components (vertexes) to each other with an associated link to form an edge
  - the format of a `connections` string is described in the infra.proto file

Now we will be designing a 4 port generic switch as a part of device inventory.

### Defining a 4 port switch

Lets define a simple Generic Switch.
![generic_switch](resources/images/generic_switch_host_diagram/generic_switch.png)

This switch is made of one asic component and four front panel ports. Front panel ports connects with the asic though mii interface.

User can define this switch with two major components inside it:

- port
- asic

These components can be viewed as nodes in a graph, connected by edges. The definition is:

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

We have specified a generic switch comprising two elements: an ASIC with a count of one and a port with a count of four. After establishing these components, we proceed to define the connections between them, which involve three distinct aspects: the source, the destination and the connecting link.

`<source>.<link>.<destination>`

The `<source>` contains the source component and its index. The `<destination>` specifies the destination component and its index. The link joins the source and the destination. Therefore, the connection would look something like this:

```
<source>.<src_index>.<link>.<destination>.<dst_index>
```

### Design host with a single nic

Let's design the Host like we did the Switch.

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

### Defining Links

The objective is to define an infrastructure build using the switch and hosts defined earlier. The goal is to build an infrastructure where one switch is directly connected to four hosts via 100G Ethernet.

![1 rack 4 hosts](resources/images/generic_switch_host_diagram/connected_diagram.png)

We have defined a switch and a host in the inventory, but not the 100G links. Let's define a 100G ethernet link as follows:

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

In this example, we have defined a link `name: 100Gbps` with a bandwidth of 100 gbps. Subsequently, four such links will be utilized to connect four devices to four switch ports, as illustrated in the above image.

### Creating Device Instances
We can scale the infrastructure by using the `device instance` message. For example, to connect 4 `generic_hosts` to one `generic_switch` by instantiating each with a count: 
- 4 `generic_hosts` as host, and 
- 1 `generic_switch` as `rack_switch`. 

The data model can be defined as follows:


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

The devices are defined under the `inventory - devices` section, serving as a blueprint or template. These devices need to be instantiated to create the entire infrastructure, similar to creating objects of a class. With the specified count, multiple copies of the devices are created starting from index 0.

Next, these device instances need to be connected over 100G ethernet links as illustrated in the picture above.


### Connecting Device Instances

Connections between the devices are made by the components of the device and links defined. Therefore, to connect two devices together, we need to define the connection in the following format:

```
<src_device>.<dev_index><src_component><comp_index>.<link>.<dst_device>.<dev_index><dst_component><comp_index>
```
The `<src_device>.<dev_index><src_component><comp_index>` specifies the source device, its index, component, and the component's index. The same format applies to the destination. The link defines the connection between source and destination.

A "." separator separates infrastructure elements. To connect a `host` with the `rack_switch`, define the connection as:


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

The host at index 0, via its nic component 0, is connected to port 0 of rack_switch 0. The link between this source and destination has a bandwidth of 100Gbps. This describes the first link shown in the above picture.

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

## The Complete Example

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

## Binding Logical Infrastructure with Custom Attributes
The primary purpose of infra.proto is to define and design a generic network fabric. This enables end users to specify the devices as nodes and links as edges. The data model also allows for the definition and design of devices by adding links and components within the device, modeling the device internals as a subgraph.
Another data model, annotate.proto, allows for the definition and binding of various vendor-specific parameters within the generic infrastructure. Users can bind:
- Vendor-specific data
- Additional qualities of the infrastructure
- Specific device performance attributes, such as:
  -	Latency
  -	Routing tables

This helps to add more context and content to infrastructure elements.

The main objective is to decouple various bindings from the infrastructure, separating the concerns of designing the logical infrastructure from the additional data needed for specific use-cases.

Lets annotate device type to our previous example:

The proposal is to include a `Device Type` for our infrastructure devices, with the types being `physical_switch`, `physical_host`, `vm_host`, and `vm_switch`. This categorization would offer additional insights into the nature of the device. Annotating the infrastructure:



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

We need to set the target, a list of elements defined in the infrastructure, and provide a value. The value contains a schema defining the `device_instance` and its associated `device_type`.

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
