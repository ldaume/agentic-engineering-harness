# Compliance Vocabulary

The terms control and assurance practitioners use to judge a product's
compliance integration, so a review names the gap the way NIST, PCI SSC, ENISA,
and ENX name it and points at something visible in a mapping, config, plan, or
report. Authors and check scripts use it; reviews do not load it by default.
Application-security terms (least privilege, provenance) live in
`shift-left-security`. ISO/IEC 27001 pages return 403 to automated fetches, so
no ISO term is admitted (Statement of Applicability, risk treatment, and
management review stay with the framework reference). Terms need a registered
source and a marker; evidence is in `sources.json`. Check: `exact` (a pattern a
script can match; none ships here yet, so no rule ids), `jev` (a typed
question), `judge` (a person or model decides).

| Term | Definition | Source | Marker | Check |
|---|---|---|---|---|
| Control | A safeguard named in a catalog, grouped in a family, applied inside the organization's risk process. | [SRC-COMP-003] | A requirement without a control id, or a control id nobody owns. | exact |
| Control assurance | Confidence that a control delivers its capability, separate from the control existing. | [SRC-COMP-003] | A claim of "implemented" with no test or assessment result behind it. | judge |
| Control baseline | A named starting set of controls for an impact level. | [SRC-COMP-004] | A control list copied wholesale with no baseline named. | judge |
| Control tailoring | Adjusting a baseline to the system's assumptions, with overlays for a community or environment. | [SRC-COMP-004] | A baseline adopted unchanged, or trimmed with no recorded reason. | judge |
| Common control | A control provided once and inherited by several systems, with accountability for inheriting it. | [SRC-COMP-006] | A product that restates a platform control instead of referencing it. | judge |
| Continuous monitoring | Ongoing evidence that controls still work within risk tolerance, not a periodic snapshot. | [SRC-COMP-005] | Evidence collected only in the weeks before an audit. | judge |
| Machine-readable controls | Catalog, profile, and results held as structured data (OSCAL: XML, JSON, YAML). | [SRC-COMP-001] | Control text only in Word, wiki, or PDF with no structured form. | exact |
| Control catalog | A framework's controls expressed as data. | [SRC-COMP-002] | A mapping that cites controls by prose title. | exact |
| Control profile | A selected and tailored set of catalog controls forming a baseline. | [SRC-COMP-002] | A profile file with no import of its catalog. | exact |
| Component definition | The security configuration of one component, reusable in a system plan. | [SRC-COMP-002] | Each system describing the same component's controls by hand. | judge |
| System security plan | How one system implements the controls of its baseline. | [SRC-COMP-002] | A plan that lists controls but no implementation statement. | judge |
| Assessment results | Findings, evidence, and scope produced by one assessment. | [SRC-COMP-002] | Evidence with no scope, time, or finding attached. | judge |
| Plan of action and milestones | The list of findings the owner must fix, with milestones. | [SRC-COMP-002] | A finding with no owner or date. | exact |
| Risk management framework step | Categorize, select, assess, authorize, monitor: the order controls are chosen and proven. | [SRC-COMP-006] | Controls selected before data and impact are categorized. | judge |
| Cardholder data environment | People, processes, and systems that handle card data, plus anything with unrestricted connectivity to them. | [SRC-COMP-007] | A system with card data in logs or tickets, or linked to the CDE, absent from the scope list. | judge |
| Segmentation | Separating card-data systems from the rest to shrink scope. | [SRC-COMP-007] | A flat network or shared admin path between in-scope and out-of-scope systems. | judge |
| Customized approach | Meeting a PCI requirement's objective by an own control, shown by a targeted risk analysis. | [SRC-COMP-007] [SRC-COMP-008] | A deviation from a defined control with no recorded objective or analysis. | judge |
| Targeted risk analysis | A risk analysis for one requirement, justifying a flexible frequency or a customized control. | [SRC-COMP-007] | A custom review interval with no analysis attached. | judge |
| Official validation form | The ROC, AOC, or SAQ template that PCI SSC requires for validation. | [SRC-COMP-009] | An internal summary or certificate presented as the validation. | exact |
| Compliance-accepting entity | The party (acquirer or brand) that sets and accepts a merchant's reporting route. | [SRC-COMP-010] | A route or SAQ chosen with no confirmation from that party. | judge |
| Assessment objective | The partner-driven target (data type) that decides which ISA requirements apply. | [SRC-COMP-011] | A TISAX label claimed with no objective named. | judge |
| Assessment level | How deeply the auditor verifies: AL 1 existence, AL 2 plausibility and evidence, AL 3 on-site. | [SRC-COMP-011] | A customer-required level that differs from the one planned. | exact |
| Assessment scope | The locations and parts assessed, inside the ISMS scope and possibly smaller. | [SRC-COMP-011] | A new site or system handling partner data missing from the scope. | judge |
| ISA catalog version | The yearly ISA release that fixes which questions an assessment ordered then uses. | [SRC-COMP-012] [SRC-COMP-013] | A self-assessment built on a version other than the one ordered. | exact |
| EU assurance level | The basic, substantial, or high level an EU cybersecurity certification scheme assigns by the risk of the intended use. | [SRC-COMP-014] | A claim of EU certification that names no scheme (such as EUCC) or level. | judge |
| Secure development practice | A task of the NIST SSDF a development process performs and can show. | [SRC-SEC-018] | An SSDF claim naming no practice id or artifact. | judge |

## Not admitted

- A certificate as proof of validation: PCI SSC accepts only its official
  forms [SRC-COMP-009]; ask for them.
- SAQ eligibility as a scoping guide for a Report on Compliance: only with the
  compliance-accepting entity's agreement [SRC-COMP-010].
- AL 1 as trust evidence: the auditor does not assess its content and TISAX
  does not use it [SRC-COMP-011].
- Compliance as a yearly audit sprint: monitoring is continuous
  [SRC-COMP-005].
- Copying a whole control catalog without scoping: baselines are tailored
  [SRC-COMP-004] and TISAX scope is chosen [SRC-COMP-011].
