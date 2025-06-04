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

This specification specifies an architecture for a transparency service for currently monitoring the security properties of one or more cloud infrastructures by multiple parties internal or external to the provider. Previously, experts drafted transparency service architectures for monitoring the lifecycle of TLS certificates for encrypted communications on the World Wide Web [@laurie21] and another for heterogenous data for software supply chain use cases [@scitt25]. An industry consortium deployed an emerging de-facto standard, Sigstore and Rekor, for monitoring published open-source software used industry-wide [@rekor]. Google's Android operating system developers deployed their own to verify the legitimacy of all compiled programs in their operating system releases [@androidtlog]. Although they represent similar use cases, the uniqueness of cloud infrastructure requires different design and implementation tradeoffs. Therefore, this specification will inventory use cases; describe the foundation and enhancements to the baseline transparency service architecture; the actors in a mutual monitoring network and their roles; specialized components of the architecture; and required protocols for actors to execute their roles with the architecture for given use cases.

## Architecture

### Use Cases

### Actors and Roles

### Components

## Terminology

## Appendix

### References
