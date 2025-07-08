# Describing Cluster Infrastructure as a Graph

Modern AI systems, comprising diverse scale-up and scale-out interconnect topologies that integrate complex heterogeneous components, connected together via diverse means, face a lack of standardized overall infrastructure description. This hinders benchmarking, simulation, and emulation. [infra.proto](keysight_chakra/infra/infra.proto) introduces a graph-based schema to describe AI/HPC infrastructure.

To create an infrastructure as a graph one can use messages from [infra.proto](keysight_chakra/infra/infra.proto). The messages allow a user to easily create logical infrastructure as vertexes and edges. This can be scale up further to describe a massive infrastructure without duplicating content.

[infra.proto](keysight_chakra/infra/infra.proto) is a Protocol Buffers (Protobuf) message that serves as the core data model for defining and designing the infrastructure. Protobuf is a schema-based, strongly typed format that models data as messages with defined fields and types in a .proto file. This schema enables efficient serialization and deserialization of structured data.

While Protobuf itself uses a compact binary format, protobuf data can be converted to human-readable formats like JSON and YAML for easier inspection, configuration, and integration with text-based tools. Our [wiki](https://keysight.github.io/infrastructure.github.io/) uses YAML for its readability and suitability for configuration and data serialization tasks. YAML's clear syntax for nested structures and lists complements the Protobuf-defined data model.

For a comprehensive understanding of the infrastructure model and to gain insights into its capabilities please visit our [wiki](https://keysight.github.io/infrastructure.github.io/)

## Contributing

We welcome contributions from anyone interested in AI/ML Network Infrastructure design. Our repository focuses on representing network topologies, devices, and connections as graphs, enabling precise visualization, analysis, and resource allocation within complex infrastructures. Whether you want to add new graph features, improve algorithms for mapping or visualization, enhance documentation, or share use cases, your input is valuable. To contribute, please review our guidelines, fork the repository, and submit your changes via pull request. Collaborate with us to advance the state of network infrastructure design and make graph-based approaches more accessible to the broader community.
