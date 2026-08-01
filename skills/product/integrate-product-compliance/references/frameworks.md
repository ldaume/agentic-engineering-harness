# Product Compliance Framework Reference

## Contents

- [Currentness Rule](#currentness-rule)
- [Shared Method](#shared-method)
- [ISO/IEC 27001](#isoiec-27001)
- [TISAX and VDA ISA](#tisax-and-vda-isa)
- [PCI DSS](#pci-dss)
- [Human Authority](#human-authority)
- [Primary Sources](#primary-sources)

## Currentness Rule

Checked on 2026-08-01. This is routing guidance, not the licensed standards,
legal advice, certification advice, or an assessor's interpretation. Re-open
the official sources and the target's licensed materials whenever a framework
affects scope, controls, evidence, or release.

Record:

- framework and exact version
- official source and check date
- target assessment or reporting period
- named internal owner and qualified external role where needed
- superseded or future-effective requirements
- local interpretation and decision record

## Shared Method

All three frameworks benefit from the same product-engineering pattern:

```text
confirmed scope and obligation
-> risk and data-flow understanding
-> control impact
-> built-in implementation and deterministic checks
-> attributable evidence from normal delivery
-> risk-based release
-> effectiveness, finding, and incident feedback
-> continual improvement
```

Shared technical controls do not make the schemes interchangeable. Preserve
their distinct scope, objectives, evidence, assessment, and assurance paths.

## ISO/IEC 27001

Current official baseline: ISO/IEC 27001:2022, with Amendment 1:2024 climate
action changes. ISO/IEC 27001 defines requirements for an information security
management system and a risk-management process across people, process, and
technology.

Product-engineering integration should connect:

- organization and interested-party context to product and trust requirements
- information-security risk assessment to discovery and bet risk
- risk treatment and the Statement of Applicability to controls and owners
- change and supplier management to delivery and platform workflows
- competence and awareness to team enablement
- operational evidence, audits, incidents, and management review to continual
  improvement

Do not infer that implementing individual Annex A controls establishes an ISMS
or certification. The organization owns scope, risk criteria, risk acceptance,
control selection, the Statement of Applicability, internal audit, management
review, and certification-body engagement.

## TISAX and VDA ISA

TISAX is an assessment and exchange mechanism. Applicable assessment objectives
determine which ISA criteria catalogs, control questions, and requirements
apply.

Current transition at the check date:

- ISA 6.0.3 remains the current basis for assessments ordered in 2026.
- ISA2027 was published on 2026-07-01 and becomes mandatory for newly ordered
  TISAX assessments from 2027-01-01.
- Existing label validity and the applicable catalog depend on the ENX lifecycle
  rules and the specific assessment order.

Confirm:

- participant, locations, and assessment scope
- customer-requested assessment objectives
- applicable information-security, prototype-protection, and data-protection
  criteria
- protection needs, assessment level, and applicable ISA version
- evidence, maturity, findings, corrective action, and exchange obligations

The ISA self-assessment workbook and its implementation/document references are
part of the TISAX assessment path. Git-owned controls and evidence can feed
those references, but do not replace the required assessment input or the audit
provider's evidence process.

Do not let an agent choose assessment objectives or claim TISAX readiness.
Security, compliance, the TISAX audit provider, and the target's owners resolve
scope and interpretation.

## PCI DSS

Current official baseline: PCI DSS v4.0.1. Requirements that were best practices
until 2025-03-31 are effective at the check date. Use the current PCI SSC
standard, reporting templates, FAQs, and targeted guidance.

Start with scope reduction and verified data flows:

- cardholder data and sensitive authentication data
- cardholder data environment and connected-to or security-impacting systems
- payment service providers and third-party service providers
- segmentation and shared services
- payment-page scripts and e-commerce eligibility
- storage, processing, transmission, logging, and administrative access

Do not infer SAQ eligibility, applicability, compensating controls, customized
approach acceptability, ROC requirements, or compliance status. Involve the
merchant or service-provider compliance owner and a QSA or other qualified PCI
expert where the reporting route or scope requires it.

PCI SSC requires its official validation forms for the applicable reporting
route. Internal Git evidence, CI results, configurations, and audit records can
support the assessment, but an internal certificate or custom summary does not
replace an official ROC, AOC, SAQ, or other required form.

## Human Authority

| Decision | Required accountable role |
|---|---|
| Product outcome and investment | product or business owner |
| Technical implementation | engineering owner |
| Security risk and control design | security and engineering owners |
| Framework interpretation | compliance or security owner, with assessor or legal input as needed |
| TISAX objective and scope | participant owner and qualified TISAX stakeholders |
| PCI scope and reporting route | PCI owner and QSA or qualified expertise as required |
| Risk acceptance | documented risk owner |
| Certification, assessment, or compliance claim | authorized organization and assurance party |
| Release exception | approved risk and release authority |

Agents support these decisions with attributable evidence and options. They do
not manufacture authority by completing a template.

## Primary Sources

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [ISO/IEC 27001:2022/Amd 1:2024](https://www.iso.org/standard/88435.html)
- [ENX TISAX downloads and current ISA lifecycle](https://www.enx.com/en-US/TISAX/downloads/)
- [ENX TISAX Participant Handbook](https://portal.enx.com/handbook/tisax-participant-handbook.html)
- [ENX ISA2027 announcement](https://portal.enx.com/en-US/news/isa2027/)
- [PCI SSC PCI DSS document library](https://www.pcisecuritystandards.org/document_library/?class=pcidss&doc=pci_dss)
- [PCI SSC PCI DSS v4.0.1 publication notice](https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1)
- [PCI SSC FAQ 1220: official validation documentation](https://www.pcisecuritystandards.org/faqs/1220/)
- [PCI SSC FAQs](https://www.pcisecuritystandards.org/faqs/all/)
