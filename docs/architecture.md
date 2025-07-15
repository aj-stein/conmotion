# An Architecture for Mutual Monitoring of Cloud Infrastructures

**Author:** [A.J. Stein](mailto:astein38@gatech.edu)
<br/>
**Version:** [/develop](https://github.com/aj-stein/conmotion/tree//develop)
<br/>
**Modified at:** 2025-07-15

_The source code from [github.com/aj-stein/conmotion at the linked commit](https://github.com/aj-stein/conmotion/tree//develop) generated this copy of the specification, supporting documentation, and related code. You can [click this link](./architecture.pdf) to download this specification as a PDF document._

## Abstract

Transparently proving the security of cloud infrastructures is a systemic challenge to industry.

Internal or external stakeholders of a cloud infrastructure may want to publish or verify data about its operational, resiliency, or security properties. However, there are no specifications for common data structures, protocols, or measurement algorithms to transparently demonstrate evidence of those properties at once or over a time intervals. This document proposes an architecture that specializes the Transparency Service architecture for providers of cloud infrastructures. The specialization of this architecture will enable them to publish evidence of security properties with verifiable digital signatures. Providers of cloud infrastructures, their consumers, or external auditors may also publish counter-signatures to verify multi-party evaluation and verification of this evidence, known as a mutual monitoring network.

## Conventions

This specification conforms to IETF's best practice [in RFC 2119](https://datatracker.ietf.org/doc/rfc2119/) to capitalize all letters in key words to indicate requirement levels [@rfc2119].

This specification also capitalizes certain words or phrases with common meaning when this specification gives them a precise normative definition. See the [Terminology section](#terminology) for a complete listing of these terms.

## Introduction

Cloud infrastructures require their providers to design, implement, and document security properties against a threat model. The providers must also actively monitor these properties for their efficacy in mitigating threats. Although these strategies are common to many complex systems, cloud infrastructures have essential characteristics that uniquely distinguish them from other deployment models. They have measured services where the provider and consumer control components automatically and precisely through metering capabilities and on-demand self-services for consumers to unilaterally provision components [@mell11 p.  2].

Despite these essential characteristics and the proliferation of many differentiated, proprietary services for cloud infrastructures, there is no de-facto standard or vendor-agnostic solution to publish digitally-signed data for a cloud service infrastructure, counter-sign the data to acknowledge and verify its contents, and/or enrich a collection of this data with verifiable measurements. Different providers have monitoring capabilities for security properties of cloud infrastructures, but most are partial, proprietary, confidential, and do not permit scalable multi-party verification of data. Therefore, a Transparency Service architecture is needed for different parties to publish signed data, counter-sign acknowledgements, and publish follow-on measurements for parties to mutually monitor heavily interconnected infrastructures.

This document specifies an architecture for a Transparency Service to concurrently monitor the security properties of one or more cloud infrastructures by multiple parties, both internal and external to the the infrastructure provider. Previously, experts drafted Transparency Service architectures for monitoring the lifecycle of TLS certificates for encrypted communications on the World Wide Web [@laurie21] and another for heterogenous data for software supply chain use cases [@scitt25]. An industry consortium deployed an emerging de-facto standard, Sigstore and Rekor, for monitoring published open-source software used industry-wide [@rekor]. Google's Android operating system developers deployed their own implementation to verify the legitimacy of all compiled programs in their operating system releases [@androidtlog]. Although they represent similar use cases, the uniqueness of cloud infrastructure requires different design and implementation tradeoffs when compared to these other implementations for different use cases. Therefore, this specification will inventory use cases; describe the foundation and enhancements to the baseline Transparency Service architecture; the actors in a mutual monitoring network and their roles; specialized components of the architecture; and required protocols for actors to execute their roles with the architecture for given use cases.

## Use Cases

This specification addresses the needs of several use cases for mutual multi-party monitoring of security properties for cloud infrastructures.

### Monitoring System Inventory

Inventory management of a cloud infrastructure is a foundational requirement for a cloud provider as part of an information security program. Many cybersecurity frameworks used for these information security programs share this requirement. Examples include control 5.9 in ISO 27001:2022 [-@iso27001_22], control PM-5 in the Special Publication 800-53 Risk Management Framework [@sp80053r5 p. 206], the control CCC-04 in the Cloud Controls Matrix [@ccm4_24 p.79], and numerous others. For a cloud infrastructure to satisfy these control requirements, they must maintain an inventory, often incredibly dynamic due to characteristics of cloud computing, for all systems the compromise the components of that infrastructure. Cloud infrastructure providers have different actors, performing different roles, where they must produce, consume, and/or verify data about the inventory of that infrastructure.

#### Cloud Infrastructure Provider

A cloud infrastructure provider uses bespoke asset management system(s) predominantly for internal use. The provider's staff can use a Transparency Service as a high-fidelity replica of the asset management system(s) data, tracking changes over time, or as the canonical source of inventory. The provider's staff will integrate inventory management automation to create new entries into the Append-only Log of the Transparency Service, adding digitally signed records one-by-one for the provisioning and deprovisioning of all systems in the infrastructure. The most recent record embeds a linkage by hash to the previous record in the Append-only Log. Staff can check the most recent record to now the latest changes or "replay the log" with the fully exported data of the Append-only Log to understand all changes over time and compose a realistic model of the services monitored. 

#### Cloud Infrastructure Customer

A customer of a cloud infrastructure uses the cloud infrastructure provider as a dependency to build their own application services or derivative cloud infrastructure, thereby creating its own need for an asset management system and inventory. By virtue of this architecture, the customer's staff must maintain their own inventory, but the assets they manage will be instances of cloud infrastructure systems provided by the upstream cloud infrastructure provider. The customer will use the upstream cloud infrastructure provider's transparency log, consuming digitally signed records and publishing digitally signed receipts to their own transparency log, acknowledging existence of the upstream infrastructure they use to provision an instance in their own infrastructure. This customer will also generate their own records for both internal and external use for their own downstream customers to confirm accurate inventory management.

#### Auditor

An auditor, accountable to the cloud infrastructure provider, their customer, or both, must review the efficacy of security control implementations through expert review of artifacts. In the case of inventory management, it is important for the auditor to use these artifacts as evidence. The auditor compares the evidence from the provider to their own artifacts they collect independently, and verify the provider's inventory is accurate and has no anomalies. Auditors can consume the Append-only Log of the Transparency Service to ascertain contemporary or historical view of the provider's inventory and thereby the efficacy of their inventory management techniques. Auditors can also digitally sign receipts and append them the transparency log to endorse inventory records, so that customers of the cloud infrastructure provider can analyze auditor endorsements in transparency log records to acquire cloud infrastructure or continue using it.

### Monitoring Configuration Management

Configuration management of a cloud infrastructure is a foundational requirement for a cloud provider as part of an information security program. Many cybersecurity frameworks used for these information security programs share this requirement. Examples include control 8.9 in ISO 27001:2022 [-@iso27001_22], multiple controls in the Configuration Management (CM) control family for the Special Publication 800-53 Risk Management Framework [@sp80053r5 p. 96-114], the control CCC-03 in the Cloud Controls Matrix [@ccm4_24 p.77], and numerous others. For a cloud infrastructure to satisfy these control requirements, the provider's staff must have known configuration baselines for their inventory, apply them, and possibly prevent provisioning outside of approved processes and create or change assets to not conform to the baselines. Cloud infrastructure providers have different actors, performing different roles, where they must produce, consume, and/or verify data about the configuration management for that infrastructure.

#### Cloud Infrastructure Provider

A cloud infrastructure provider uses bespoke configuration management system(s) mostly for internal use. The provider's staff can use a Transparency Service as a high-fidelity replica of the configuration management system(s) data, tracking changes over time, or as the canonical source of inventory. This data will cross-reference which systems link to which configurations with both datasets on the Transparency Service. The provider's staff will integrate inventory management and configuration management automation to create new entries into the Append-only Log of the Transparency Service, adding digitally signed records one-by-one for the creation, modification, and deletion of configurations for different assets in the cloud infrastructure. The most recent record embeds a linkage by hash to the previous record in the Append-only Log. Staff can check the most recent record to now the latest changes or "replay the log" with the fully exported data of the Append-only Log to understand all changes over time and compose a realistic model of the services monitored. 

#### Cloud Infrastructure Customer

A customer of a cloud infrastructure uses the cloud infrastructure provider as a dependency to build their own application services or derivative cloud infrastructure, thereby creating its own need for an configuration management system. By virtue of this architecture, the customer's staff must maintain their own inventory and configuration management database, even the assets and their configurations are instances of systems the upstream cloud infrastructure provides. The customer will use the upstream cloud infrastructure provider's transparency log, consuming digitally signed records and publishing digitally signed receipts to their own transparency log, acknowledging existence of the upstream infrastructure they use to provision an instance in their own infrastructure. This customer will also generate their own records for both internal and external use for their own downstream customers to confirm accurate inventory management.

#### Auditor

An auditor, accountable to the cloud infrastructure provider, their customer, or both, must review the efficacy of security control implementations through expert review of artifacts. In the case of configuration management, it is important for the auditor to use these artifacts as evidence. The auditor compares the evidence from the provider to their own artifacts they collect independently, and verify the provider's inventory and related configuration management records  are accurate and without anomalies. Auditors can consume the Append-only Log of the Transparency Service to ascertain contemporary or historical view of the provider's configuration management records and thereby the efficacy of their configuration management techniques. Auditors can also digitally sign receipts and append them the transparency log to endorse inventory records, so that customers of the cloud infrastructure provider can analyze auditor endorsements in transparency log records to newly acquire cloud infrastructure or continue using it.

## Architecture

The mutual monitoring architecture specializes the architecture of a Transparency Service as defined by the IETF SCITT Working Group [@scitt25]. This architecture includes a Transparency Service; Adjacent Services, custom services deployed adjacently to the Transparency Service for log search and storage; and Relying Parties, Transparency Service clients that serve specialized use cases for processing the content of each record in the Append-only Log.

Given [the above use cases](#use-cases), a cloud infrastructure provider MAY deploy these components with logical relationships like those in the diagram below.

![](./arch_provider-only.png)

### Components

#### Transparency Service

The Transparency Service is the core component of the mutual monitoring architecture. An implementation MUST conform to the normative requirements in the current draft of the IETF SCITT Architecture [@scitt25]. These requirements document the minimally viable features, listed below, for a Transparency Service to function for the mutual monitoring use cases [documented above](#use-cases).

1. Transparency Services have an Append-Only Log of Signed Statements in order of Registration so one or more instances can maintain their integrity and prevent equivocation or other forms of misuse.
1. Transparency Services have a Registration Policy API with endpoints for any Relying Party to determine signing and Claim requirements before Registration.
1. Transparency Services have a Submissions API with endpoints for an Issuer to complete Registration of a Signed Claim.
1. Transparency Services have an Entry API with endpoints for any Relying Party to retrieve one or more entries previously registered with in the Append-only Log.

For a fully conformant implementation, Transparency Services for Mutual Monitoring MUST implement minimally required API endpoints in the [SCITT Reference API specification draft](https://www.ietf.org/archive/id/draft-ietf-scitt-scrapi-04.html) [@scrapi25].

##### Append-only Log

The foundation of the Transparency Service is the Append-Only Log. The Append-ony Log is a sequence of Signed Statements that completed Registration through the Submission API and are accessible to a Relying Party from the Entry API. The append-only characteristic is integral to providing the integrity of individual Signed Statements, but the sequence itself. To do so, a Transparency Service needs to serialized Signed Statements in the Append-Only Log with a Verifiable Data Structure.

The Verifiable Data Structure, and supporting algorithms, for serializing data MUST use allow only for Append-only updates that do not permit reordering; enforce Non-equivocation for the Append-only Log; and allow Replayability so any Relying Party can consume the Append-only Log's data and check individual Statements or the full sequence [@scitt25]. Transparency services instances for mutual monitoring MUST implement the Verifiable Data Structure the IETF COSE Working Group specifies in its draft specification for COSE Receiptis [-@cose_receipts25].

##### Registration Policy API

A Transparency Service MUST implement a Registration Policy API to identify permissible trust anchors, Issuer identity, Statement Subjects, or any other mandatory requirements for a Statement for successful Registration [@scitt25].

A Transparency MAY publish a Registration Policy with any trust anchor and no additional requirements. It MAY publish a Registration Policy that requires specific trust anchors, Issuer identities, Statement Subjects, and other custom requirements for the payload of the Statement.

A Transparency Service MUST support initialization and bootstrapping with pre-configured Registration Policy; Registration of a first Signed Statement without checks required by the Registration Policy for successive submissions; an authenticated out-of-band management interface [@scitt25].

A Transparency Service MUST publish the current Registration Policy described above via the `/.well-known/transparency-configuration` endpoint [@scrapi25].

##### Submissions API

A Transparency Service MUST implement an endpoint for Issuers' Relying Parties to submit Signed Statements to perform Registration. If the Signed Statement has a valid digital signature and conforms to Registration Policy requirements, the Transparency Service accepts submission of the Signed Statement and appends it the Append-Only log for all Relying Parties to consume and process the Signed Statement's payload.

A Transparency Service MUST implement a HTTPS endpoint at `/entries` for Issuers' Relying Parties to submit a Signed Statement for Registration with a HTTP `POST` query. The body of the query MUST be a valid and well-formed Signed Statement.

When a Relying Party submits a HTTP `POST` query, a Transparency Service SHOULD return a response to the original HTTP `POST` query. A response MAY be the Receipt of the Signed Statement with its Registration data. If Registration is incomplete, a Transparency Service MAY return a response with the HTTP `301` status code and a locator URL, so a Relying Party SHOULD query the locator for the completion of Registration operations. If Registration is complete, a Transparency Service MAY return a response with a HTTP `201` status code and a body with a Transparent Statement, a Signed Statement that also includes in its unprotected header a Receipt of Registration from the Transparency Service.

A Transparency Service MAY complete Registration of a submission of a Signed Statement with any payload that conforms to its Registration Policy. For Mutual Monitoring use cases, payloads SHOULD encode payloads with [version v1.5.0 of the Open Cybersecurity Format (OCSF) data model](https://schema.ocsf.io/1.5.0/) . The payload should use the JSON serialization, but the Transparency Service MUST complete Registration of any well-formed or valid payload with OCSF in other serializations, or payloads in other data models and serializations, if it conforms to its Registration Policy.

##### Entry API

A Transparency Service MUST implement an Entry API for Relying Parties to retrieve Signed Statements that successfully completed Registration. If the Registration for a Signed Statement is not complete, a Transparency Service MUST return a Locator URL for Relying Parties to periodically check for successful completion of Registration, per [the Registration Policy API requirements listed above](#registration-policy-api).

A Transparency Service MUST implement this functionality at the `/entries` endpoint to return responses to queries using a HTTP `GET` query. The query of the Relying Party MUST have the ID of the Signed Statement, at a minimum, to get a valid response from a Transparency Service.

#### Adjacent Services

A Transparency Service MAY implement Adjacent Services for object storage, databases, software package management APIs, and custom functionality to support the mandatory core components on a Transparency Service [@scitt25]. This specification documents two recommended, but optional, Adjacent Services recommended for mutual monitoring of cloud service providers: an Adjacent Service for Storage an Adjacent Service for Search.

##### Adjacent Service for Storage

A Transparency Service MAY implement an Adjacent Service for Storage. This service SHOULD implement persistence and retrieval for the  original Artifact, which is the basis of information in a Signed Statement's payload. When implemented, the Adjacent Service for Storage facilitates remotely signing statements, thereby permitting Transparency Service and Relying Party operates to access and validate Signed Statements of Artifacts, when properly authenticated and authorized, based upon the hash of said Artifacts.

Per [Appendix B of the current draft of the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#name-signing-statements-remotely), this approach is especially advantageous given the potentially large size of Artifacts and the growth of Append-only Log over time [@scitt25]. Therefore, a Transparency Service for mutual monitoring of cloud service providers SHOULD implement this service.

##### Adjacent Service for Search

A Transparency Service MAY implement an Adjacent Service for Search. This Adjacent Service will implement an interface to a query API. This interface MAY allow Relying Parties to query the Transparency Service for the Entry ID, Registration Policy, Issuer key ID, Subject and/or additional key-value tuples related to the specific payloads of a Signed Statement or Receipt. The Adjacent Service MAY also implement a similar ability for authenticated and authorized Relying Parties to query associated Artifacts given the hash or other properties of the Artifact derived from the Signed Statement or Receipt.

A Transparency Service for mutual monitoring of cloud service providers SHOULD implement this service.

### Actors and Roles

### Flows

#### Inventory Management Use Case Dataflow

Below is a non-normative dataflow diagram identifying recommended steps for an auditor to monitor a cloud service provider and detect inventory not reported by the provider's inventory management system using the Transparency Log and Adjacent Services.

![](./use-case_inventory.png)

#### Configuration Management Use Case Dataflow

Below is a non-normative dataflow diagram identifying recommended steps for an auditor to monitor a cloud service provider and detect configuration management updates not reported by the provider's configuration management system using the Transparency Log and Adjacent Services.

![](./use-case_configuration.png)

## Terminology

- [Adjacent Service]{#term-adjacent-service}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-5.1.4) [@scitt25].

- [Append-only Log]{#term-append-only-log}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.4.1) [@scitt25].

- [Equivocation]{#term-equivocation}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.14.1) [@scitt25].

- [Issuer]{#term-issuer}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.16.1) [@scitt25].

- [Non-equivocation]{#term-non-equivocation}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.18.1) [@scitt25].

- [Receipt]{#term-receipt}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.20.1) [@scitt25].

- [Registration]{#term-registration} This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.22.1) [@scitt25].

- [Registration Policy]{#term-registration-policy}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.24.1) [@scitt25].

- [Relying Party]{#term-relying-party}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.26.1) [@scitt25]. This term is a synonym of client in numerous IETF specifications, but connotes specifical requirements and functionalities particular to the SCITT Architecture specification. Therefore, this specification prefers the term Relying Party.

- [Replayability]{#term-replayability}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-5.1.3-2.6.1) [@scitt25].

- [Signed Statement]{#term-signed-statement}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.28.1) [@scitt25].

- [Statement]{#term-statement}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.30.1) [@scitt25].

- [Subject]{#term-subject}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.32.1) [@scitt25].

- [Transparency]{#term-transparency}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#name-definition-of-transparency) [@scitt25].

- [Transparent Statement]{#term-transparent-statement}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.36.1) [@scitt25].

- [Transparency Service]{#term-transparency-service}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.34.1) [@scitt25].

- [Verifiable Data Structure]{#term-vds}: This document uses the normative definition from [the IETF SCITT Architecture](https://www.ietf.org/archive/id/draft-ietf-scitt-architecture-12.html#section-3-4.38.1) [@scitt25].

## Appendix

### Example Statements

#### Inventory Management Records

Below are non-normative example inventory management payloads in the OCSF format. Per the [Monitoring System Inventory Use Case](#monitoring-system-inventory) and [use case dataflow](#inventory-management-use-case-dataflow), each payload represents one inventory management record a CSP, or monitoring auditor, will hash and append its signed hashed to the Append-Only Log.

[`example_inventory_csp.json`](./example_inventory_csp.json):

```json
{
  "message": "inventory new",
  "time": 1752469463715,
  "severity": "Informational",
  "resources": [
    {
      "data": "RXhhbXBsZSBwYXlsb2FkCg==",
      "name": "Example Instance Codename 1",
      "owner": {
        "name": "Cloud Service Provider Codename",
        "type": "Unknown",
        "uid": "f2c42f77-d7b9-4efd-aeee-e05be36fc0cb",
        "type_id": 0
      },
      "type": "Example Instance Type Codename",
      "ip": "4.3.2.1",
      "uid": "022664f6-6070-11f0-8d17-6aae7c2d1fdb"
    }
  ],
  "category_uid": 5,
  "activity_id": 1,
  "type_uid": 502301,
  "type_name": "Cloud Resources Inventory Info: Log",
  "category_name": "Discovery",
  "class_uid": 5023,
  "class_name": "Cloud Resources Inventory Info",
  "timezone_offset": 26,
  "activity_name": "Log",
  "severity_id": 4,
  "status_code": "accepted",
  "status_detail": "no determination made new inventory created",
  "status_id": 0,
  "metadata": {
    "version": "1.5.0",
    "product": {
      "name": "conmotion",
      "version": "0.1.0-alpha",
      "uid": "264aff4e-18ce-4c10-a670-114fc9c5e3c1",
      "feature": {
        "name": "mutual-monitoring_inventory",
        "version": "0.1.0-alpha",
        "uid": "dbd909a3-4721-4811-b54b-0d13f318ebb5"
      },
      "lang": "en",
      "cpe_name": "cpe:2.3:a:aj-stein:conmotion:0.1.0:alpha:*:*:*:*:*:*",
      "vendor_name": "github.com/aj-stein"
    },
    "profiles": [
      "cloud"
    ]
  }  
}
```

[`example_inventory_auditor.json`](./example_inventory_auditor.json)

```json
{
  "message": "inventory new",
  "time": 1752469463715,
  "severity": "Informational",
  "resources": [
    {
      "data": "RXhhbXBsZSBwYXlsb2FkCg==",
      "name": "Example Instance Codename 2",
      "owner": {
        "name": "Cloud Service Provider Codename",
        "type": "Unknown",
        "uid": "703539e3-df7c-4252-ba51-b3240c26ba2b",
        "type_id": 0
      },
      "type": "Example Instance Type Codename",
      "ip": "1.2.3.4",
      "uid": "1a4c6228-a956-4244-a77e-3aa29c98c4c4"
    }
  ],
  "category_uid": 5,
  "activity_id": 1,
  "type_uid": 502301,
  "type_name": "Cloud Resources Inventory Info: Log",
  "category_name": "Discovery",
  "class_uid": 5023,
  "class_name": "Cloud Resources Inventory Info",
  "timezone_offset": 26,
  "activity_name": "Log",
  "severity_id": 4,
  "status_code": "accepted",
  "status_detail": "no determination made new inventory created",
  "status_id": 0,
  "metadata": {
    "version": "1.5.0",
    "product": {
      "name": "conmotion",
      "version": "0.1.0-alpha",
      "uid": "264aff4e-18ce-4c10-a670-114fc9c5e3c1",
      "feature": {
        "name": "mutual-monitoring_inventory",
        "version": "0.1.0-alpha",
        "uid": "dbd909a3-4721-4811-b54b-0d13f318ebb5"
      },
      "lang": "en",
      "cpe_name": "cpe:2.3:a:aj-stein:conmotion:0.1.0:alpha:*:*:*:*:*:*",
      "vendor_name": "github.com/aj-stein"
    },
    "profiles": [
      "cloud"
    ]
  }  
}
```

#### Inventory Management Measurement

Below are non-normative example inventory management measurement payloads in the OCSF format. Per the [Monitoring System Inventory Use Case](#monitoring-system-inventory) and [use case dataflow](#inventory-management-use-case-dataflow), the payload represents one inventory management measurement record for an auditor to hash and append its signed hashed to the Append-Only Log. Given the [non-normative inventory management record examples above](#inventory-management-records) and a measurement interval of the cloud service from the epoch of first report to present, the `impact_score` of `50` indicates the auditor monitored a CSP and detectected 1/2 systems not in the cloud provider's official inventory.

[](./example_inventory-measurement_auditor.json)

```json
{
  "message": "inventory management metric since epoch",
  "status": "Updated",
  "time": 1752473191,
  "severity": "Informational",
  "severity_id": 4,
  "impact_id": 0,
  "impact_score": 50,
  "status_code": "dec",
  "status_detail": "constructed screens icon",
  "status_id": 1,  
  "resources": [
        {
      "data": "RXhhbXBsZSBwYXlsb2FkCg==",
      "name": "Example Instance Codename 1",
      "owner": {
        "name": "Cloud Service Provider Codename",
        "type": "Unknown",
        "uid": "f2c42f77-d7b9-4efd-aeee-e05be36fc0cb",
        "type_id": 0
      },
      "type": "Example Instance Type Codename",
      "ip": "4.3.2.1",
      "uid": "022664f6-6070-11f0-8d17-6aae7c2d1fdb"
    },
        {
      "data": "RXhhbXBsZSBwYXlsb2FkCg==",
      "name": "Example Instance Codename 2",
      "owner": {
        "name": "Cloud Service Provider Codename",
        "type": "Unknown",
        "uid": "703539e3-df7c-4252-ba51-b3240c26ba2b",
        "type_id": 0
      },
      "type": "Example Instance Type Codename",
      "ip": "1.2.3.4",
      "uid": "1a4c6228-a956-4244-a77e-3aa29c98c4c4"
    }
  ],
  "category_uid": 2,
  "activity_id": 1,
  "type_uid": 200401,
  "type_name": "Detection Finding: Update",
  "category_name": "Findings",
  "class_uid": 2004,
  "class_name": "Detection Finding",
  "timezone_offset": 2,
  "remediation": {
    "desc": "fairfield revelation compute"
  },
  "activity_name": "Update",
  "cloud": {
    "cloud_partition": "Example CSP Cloud Partition",
    "provider": "Example CSP Codename",
    "region": "Example CSP Region",
    "zone": "Example Zone"
  },
  "confidence": "High",
  "confidence_id": 3,
  "evidences": [
    {
      "url": {
        "version": "1.5.0",
        "url": {
          "port": 443,
          "scheme": "https",
          "path": "/entries/4869fa3b2d9f4af5bd08986af850e12b1f4268fd1a6f6f8ebbfb74a1f5d55221",
          "hostname": "ts.example-auditor.com",
          "category_ids": [
            66
          ],
          "resource_type": "transparency log inventory",
          "url_string": "https://ts.example-auditor.com//entries/4869fa3b2d9f4af5bd08986af850e12b1f4268fd1a6f6f8ebbfb74a1f5d55221"
        }
      }
    },
        {
      "url": {
        "version": "1.5.0",
        "url": {
          "port": 443,
          "scheme": "https",
          "path": "/entries/53baec839d639ce474876b81872ec492a72672b95dd8b9b85799447d30dad757",
          "hostname": "ts.example-auditor.com",
          "category_ids": [
            66
          ],
          "resource_type": "transparency log inventory",
          "url_string": "https://ts.example-auditor.com//entries/53baec839d639ce474876b81872ec492a72672b95dd8b9b85799447d30dad757"
        }
      }
    }  
  ],
  "metadata": {
    "version": "1.5.0",
    "product": {
      "name": "conmotion",
      "version": "0.1.0-alpha",
      "uid": "264aff4e-18ce-4c10-a670-114fc9c5e3c1",
      "feature": {
        "name": "mutual-monitoring_inventory",
        "version": "0.1.0-alpha",
        "uid": "dbd909a3-4721-4811-b54b-0d13f318ebb5"
      },
      "lang": "en",
      "cpe_name": "cpe:2.3:a:aj-stein:conmotion:0.1.0:alpha:*:*:*:*:*:*",
      "vendor_name": "github.com/aj-stein"
    },
    "profiles": [
      "cloud"
    ],
    "log_name": "green_hurricane_wizard",
    "log_provider": "ts.example-auditor.com",
    "log_version": "2025h1",
    "original_time": "2025-07-14T02:03:58Z",
    "tenant_uid": "c950c785-a710-4dc0-a170-05344df33f9e"
  }  
}
```

### References
