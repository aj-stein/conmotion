# An Architecture for Mutual Monitoring of Cloud Infrastructures

**Author:** [A.J. Stein](mailto:astein38@gatech.edu)
<br/>
**Version:** [/develop](https://github.com/aj-stein/conmotion/tree//develop)
<br/>
**Modified at:** 2025-06-03

_The source code from [github.com/aj-stein/conmotion at the linked commit](https://github.com/aj-stein/conmotion/tree//develop) generated this copy of the specification, supporting documentation, and related code._

## Abstract

The transparency of cloud infrastructures is a systemic challenge to industry.

Internal or external stakeholders of a cloud infrastructure may want to publish or verify data about its operational, resiliency, or security properties. However, there are no specifications for common data structures, protocols, or measurement algorithms to transparently demonstrate evidence of those properties at once or over a time interval. This document proposes an architecture that specializes the transparency service architecture for providers of cloud infrastructures. The specialization of this architecture will enable them to publish evidence of security properties with verifiable digital signatures. Providers of cloud infrastructures, their consumers, or external auditors may also publish counter-signatures to verify multi-party evaluation and verification of this evidence, known as a mutual monitoring network.

## Introduction

Cloud infrastructures require their providers to design, implement, and document security properties against a threat model and actively monitor these properties for their efficacy. Moreover, cloud infrastructures have essential characteristics that uniquely distinguish them from other deployment models. They have measured services where the provider and consumer control components automatically and precisely through metering capabilities and on-demand self-services for consumers to unilaterally provision components [@mell11 p.  2]. 

Despite these essential characteristics and the proliferation of many differentiated, proprietary services for cloud infrastructures, there is no de-facto standard or vendor-agnostic solution to publish digitally-signed data for a cloud service infrastructure, counter-sign the data to acknowledge and verify its contents, and/or enrich a collection of this data with verifiable measurements. Different providers have monitoring capabilities for security properties of cloud infrastructures, but most are partial, proprietary, confidential, and do not permit scalable multi-party verification of data. Therefore, a transparency service architecture is needed for different parties to publish signed data, counter-sign acknowledgements, and publish follow-on measurements for parties to mutually monitor heavily interconnected infrastructures.

This specification specifies an architecture for a transparency service to concurrently monitor the security properties of one or more cloud infrastructures by multiple parties, both internal and external to the the infrastructure provider. Previously, experts drafted transparency service architectures for monitoring the lifecycle of TLS certificates for encrypted communications on the World Wide Web [@laurie21] and another for heterogenous data for software supply chain use cases [@scitt25]. An industry consortium deployed an emerging de-facto standard, Sigstore and Rekor, for monitoring published open-source software used industry-wide [@rekor]. Google's Android operating system developers deployed their own to verify the legitimacy of all compiled programs in their operating system releases [@androidtlog]. Although they represent similar use cases, the uniqueness of cloud infrastructure requires different design and implementation tradeoffs. Therefore, this specification will inventory use cases; describe the foundation and enhancements to the baseline transparency service architecture; the actors in a mutual monitoring network and their roles; specialized components of the architecture; and required protocols for actors to execute their roles with the architecture for given use cases.

## Use Cases

This specification addresses the needs of several use cases for mutual multi-party monitoring of security properties for cloud infrastructures.

### Monitoring System Inventory

Inventory management of systems that comprise components of a cloud infrastructure is a foundational requirement for many security control frameworks that organizations use whether or not they maintain a cloud infrastructure. Examples include control 5.9 in ISO 27001:2022 [-@iso27001_22], control PM-5 in the Special Publication 800-53 Risk Management Framework [@sp80053r5 p. 206], the control CCC-04 in the Cloud Controls Matrix [@ccm4_24 p.79], and numerous others. For a cloud infrastructure to satisfy these control requirements, they must maintain an inventory, often incredibly dynamic due to characteristics of cloud computing, for all systems the compromise the components of that infrastructure. Cloud infrastructure providers have different actors, performing different roles, where they must produce, consume, and/or verify data about the inventory of that infrastructure.

#### Cloud Infrastructure Provider

A cloud infrastructure provider uses bespoke asset management system(s) predominantly for internal use. The provider's staff can use a transparency service as a high-fidelity replica of the asset management system(s) data, tracking changes over time, or as the canonical source of inventory. The provider's staff will integrate inventory management automation to create new entries into the append-only log of the transparency service, adding digitally signed records one-by-one for the provisioning and deprovisioning of all systems in the infrastructure. The most recent record embeds a linkage by hash to the previous record in the append-only log. Staff can check the most recent record to now the latest changes or "replay the log" with the fully exported data of the append-only log to understand all changes over time and compose a realistic model of the services monitored. 

#### Cloud Infrastructure Customer

A customer of a cloud infrastructure uses the cloud infrastructure provider as a dependency to build their own application services or derivative cloud infrastructure, thereby creating its own need for an asset management system and inventory. By virtue of this architecture, the customer's staff must maintain their own inventory, but the assets they manage will be instances of cloud infrastructure systems provided by the upstream cloud infrastructure provider. The customer will use the upstream cloud infrastructure provider's transparency log, consuming digitally signed records and publishing digitally signed receipts to their own transparency log, acknowledging existence of the upstream infrastructure they use to provision an instance in their own infrastructure. This customer will also generate their own records for both internal and external use for their own downstream customers to confirm accurate inventory management.

#### Auditor

An auditor, accountable to the cloud infrastructure provider, their customer, or both, must review the efficacy of security control implementations through expert review of artifacts. In the case of inventory management, it is important for the auditor to use these artifacts as evidence. The auditor compares the evidence from the provider to their own artifacts they collect independently, and verify the provider's inventory is accurate and has no anomalies. Auditors can consume the append-only log of the transparency service to ascertain contemporary or historical view of the provider's inventory and thereby the efficacy of their inventory management techniques. Auditors can also digitally sign receipts and append them the transparency log to endorse inventory records, so that customers of the cloud infrastructure provider can analyze auditor endorsements in transparency log records to acquire cloud infrastructure or continue using it.

### Monitoring Configuration Management

Configuration management for systems that comprise components of a cloud infrastructure is a foundational requirement for many security control frameworks. Examples include control 8.9 in ISO 27001:2022 [-@iso27001_22], multiple controls in the Configuration Management (CM) control family for the Special Publication 800-53 Risk Management Framework [@sp80053r5 p. 96-114], the control CCC-03 in the Cloud Controls Matrix [@ccm4_24 p.77], and numerous others. For a cloud infrastructure to satisfy these control requirements, the provider's staff must have known configuration baselines for their inventory, apply them, and possibly prevent provisioning outside of approved processes and create or change assets to not conform to the baselines. Cloud infrastructure providers have different actors, performing different roles, where they must produce, consume, and/or verify data about the configuration management for that infrastructure.

#### Cloud Infrastructure Provider

#### Cloud Infrastructure Customer

#### Auditor

## Architecture

### Components

### Actors and Roles

### Flows

## Terminology

## Appendix

### References
