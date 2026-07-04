OUTPUT_GENERATION_ARCHITECTURE.md
Document Classification: Output Generation Architecture — Source of Truth Parent Documents: ARCHITECTURE_VISION.md · SYSTEM_ARCHITECTURE.md · BACKEND_MODULE_ARCHITECTURE.md · AI_AGENT_ARCHITECTURE.md · WORKFLOW_ENGINE.md · DATA_SOLUTION_ARCHITECTURE.md · SECURITY_ARCHITECTURE.md Status: Approved — Foundation Release Version: 1.0.0 Scope: The complete output generation discipline of ArchitectIQ — how an approved architecture becomes validated, versioned, packaged, downloadable deliverables LLM Provider Assumption: OpenAI (current implementation). Architecture is provider-independent.

# Table of Contents
Output Generation Philosophy
Output Layer Responsibilities
Output Generation Pipeline
End-to-End Output Flow
Supported Output Types
Markdown Generation
Interactive HTML Report Generation
Mermaid Diagram Generation
Graphviz DOT Generation
SVG / PNG Rendering Flow
JSON Export
Output Metadata
Output Versioning
Output Validation
Output Quality Rules
Output Storage Strategy
Download Package Structure
Output Security
Performance Guidelines
Future Extension
Document Status and Metadata
1. Output Generation Philosophy
## 1.1 Position in the Platform
Output generation is the terminal discipline of the platform. It begins only after the architect has explicitly approved an architecture at the human review gate (SFR-01) and ends when a versioned, integrity-checked, downloadable deliverable bundle is available to the architect. It contains no AI reasoning, no design intelligence, and no governance authority — those responsibilities belong to the agent, workflow, and review layers upstream.

The Output Layer is the mechanical materialization of approved architectural intent into client-ready artifacts. Where the agent pipeline produces decisions, the output layer produces deliverables.

## 1.2 Core Principles
Principle	Description
Approval precedes generation	No deliverable is produced from unapproved state. The Generation Phase (WORKFLOW_ENGINE.md Stages 14–17) is unreachable without an identity-attributed approval event in the Decision Ledger.
Content is fixed at approval	The approved architecture snapshot is immutable input. Generators render — they do not reinterpret, refine, or extend the approved content.
One truth, many renderings	Every output format renders the same underlying approved architecture state. A finding present in the HLD Markdown is present in the HTML report, the JSON export, and (where visual) the diagrams.
Fail per format, not per bundle	A single format failure does not invalidate the bundle. The manifest documents which formats succeeded and which are unavailable.
Deliverables are versioned artifacts	Every generated bundle is a versioned, integrity-hashed, immutable snapshot. Regeneration creates a new version — never an in-place overwrite.
Self-contained by construction	Every deliverable is complete without external runtime dependency. An HTML report opened offline renders correctly. A Markdown document rendered anywhere is readable.
Generation is deterministic given inputs	Given the same approved architecture state and the same template version, generation produces byte-equivalent output for non-AI formats (Markdown, JSON, DOT, SVG). AI-composed formats (HTML narrative) are semantically equivalent but not necessarily byte-equivalent.
## 1.3 Boundary With Upstream Layers
The Output Layer consumes exactly two categories of input:

Approved architecture state — the immutable snapshot produced at architect approval, containing all Design and Validation stage outputs, architect overrides, and the approval attribution record.
Versioned templates and rendering configuration — from the configuration layer, external to code.
It produces exactly one category of output: files persisted to Output Storage with a manifest recorded in the database. It does not modify engagement state, does not write to the Decision Ledger, and does not communicate with agents.

2. Output Layer Responsibilities
The Output Layer owns exclusively:

Rendering approved architecture state into every supported format
Loading and applying versioned output templates
Diagram source generation (Mermaid, Graphviz DOT)
Diagram rasterization (SVG, PNG) from DOT source
Format-level validation of generated artifacts before packaging
Manifest assembly with integrity checksums
Bundle packaging and storage in Output Storage
Version lineage tracking across regeneration cycles
Per-format failure isolation and reporting
The Output Layer does not own:

AI-generated content composition (owned by Documentation Agent, Diagram Generation Agent, HTML Report Agent — AI_AGENT_ARCHITECTURE.md Section 7.5)
Approval enforcement (owned by Engagement Manager + Review Manager)
Storage infrastructure (owned by OutputStorageService — BACKEND_MODULE_ARCHITECTURE.md Layer 7)
Access control on downloads (owned by API Layer + service-level ownership check)
Client-side rendering of previews (owned by the output-viewer frontend module)
3. Output Generation Pipeline
## 3.1 Pipeline Overview
```mermaid

```

flowchart TD
    A([Approved Architecture Snapshot]) --> B[Generation Trigger]
    B --> C[Template Resolution]
    C --> D[Format Dispatch]

    D --> E1[Markdown Generation]
    D --> E2[HTML Report Generation]
    D --> E3[Diagram Source Generation]
    D --> E4[JSON Serialization]

    E3 --> F1[Mermaid Source]
    E3 --> F2[Graphviz DOT Source]

    F2 --> G[Diagram Rasterization]
    G --> H1[SVG Rendering]
    G --> H2[PNG Rendering]

    E1 --> I[Per-Format Validation]
    E2 --> I
    F1 --> I
    F2 --> I
    H1 --> I
    H2 --> I
    E4 --> I

    I --> J[Manifest Assembly]
    J --> K[Integrity Hashing]
    K --> L[Bundle Persistence]
    L --> M[Manifest Recording in DB]
    M --> N([Bundle Available for Download])

    style A fill:#f5f5f5,stroke:#999999
    style N fill:#e8f9e8,stroke:#006600
## 3.2 Pipeline Stage Meaning
Stage	Responsibility	Reference
Generation Trigger	Consumes the approval event; validates the approved snapshot is complete	WORKFLOW_ENGINE.md Stage 14 entry
Template Resolution	Loads the versioned template set for each format from configuration	Section 6.2, 7.2
Format Dispatch	Routes to the appropriate generator per requested format via OutputGeneratorFactory	BACKEND_MODULE_ARCHITECTURE.md Section 9.2
Format-Specific Generation	Each format renders independently and in parallel where safe	Sections 6–11
Diagram Rasterization	DOT source → SVG → PNG via renderer strategies	Section 10
Per-Format Validation	Syntactic, structural, and integrity validation before inclusion	Section 14
Manifest Assembly	Consolidates all successful files into the bundle manifest	Section 12
Integrity Hashing	Content hashes per file + bundle-level composite hash	Section 12.2
Bundle Persistence	Files written to Output Storage; manifest to output_bundles / output_files	Section 16
Manifest Recording	Bundle references linked to the approved engagement version	DATABASE_ARCHITECTURE.md Section 5.6
## 3.3 Pipeline Concurrency Model
Format generation is parallelizable across formats that have no dependency on each other. Diagram source (Mermaid, DOT) must complete before HTML Report Generation (which embeds them) and before rasterization (SVG, PNG derived from DOT). The pipeline enforces this dependency graph — it does not permit an HTML report to be finalized until its dependent diagrams are validated.

4. End-to-End Output Flow
```mermaid

```

flowchart LR
    R([Requirement]) --> AI[AI Processing<br/>Discovery · Design · Validation · Governance]
    AI --> ARCH[Approved Architecture<br/>Immutable Snapshot]
    ARCH --> DOC[Document Generation<br/>Markdown · JSON]
    DOC --> DIAG[Diagram Generation<br/>Mermaid · DOT · SVG · PNG]
    DIAG --> HTML[Interactive HTML Report]
    HTML --> PKG[Packaging<br/>Manifest · Hashing · Storage]
    PKG --> DL([Final Download<br/>Versioned Bundle])

    style R fill:#f5f5f5,stroke:#999999
    style ARCH fill:#fff3cd,stroke:#cc8800
    style DL fill:#e8f9e8,stroke:#006600
## 4.1 Flow Semantics
Transition	Owner	Guarantee
Requirement → AI Processing	Workflow Engine + Agents	Structured, cited, confidence-scored outputs
AI Processing → Approved Architecture	Human Review Gate	Identity-attributed approval; snapshot immutable thereafter
Approved Architecture → Document Generation	Documentation Agent + Output Layer	Structured content produced from approved snapshot only
Document Generation → Diagram Generation	Diagram Generation Agent + Diagram Renderer	Every diagram type derives from approved topology and data flow
Diagram Generation → Interactive HTML	HTML Report Agent + Output Layer	Self-contained; embeds validated diagrams and validated document content
HTML → Packaging	Output Packager	Manifest, hashes, versioned bundle written to storage
Packaging → Download	Output Service + API Layer	Ownership-checked, audit-logged retrieval
## 4.2 Non-Regressive Flow Rule
The flow is strictly forward. A downstream stage never causes an upstream stage to re-execute. If the architect requests changes after downloading a bundle, the correct path is a new engagement version through the refinement workflow (WORKFLOW_ENGINE.md Section 10.2) — not modification of the generated bundle.

5. Supported Output Types
Version 1 supports seven output formats. Each format has a distinct purpose, audience, and rendering contract.

Format	Extension	Purpose	Primary Audience
Markdown	.md	Portable, editable structured documents (HLD, LLD, Executive Summary, Risk Register, Assumptions Log)	Architects, engineers, documentation systems
Interactive HTML	.html	Self-contained, navigable, stakeholder-ready report with embedded diagrams	Client stakeholders, executives, review boards
Mermaid	.mmd	Diagram source for documentation systems and collaboration tools	Documentation systems, developer tools
Graphviz DOT	.dot	Diagram source for advanced layout scenarios	Technical documentation, publication tooling
SVG	.svg	Scalable vector rendering of diagrams	Presentations, publication, embedding
PNG	.png	Raster rendering of diagrams	Slides, screenshots, non-vector contexts
JSON	.json	Machine-readable architecture state	Downstream integrations, IaC generators, analytics
## 5.1 Format Selection Contract
Format selection per engagement is configuration-driven. The default format set is generated for every approved engagement. Format subsets can be requested through the output specification, but the default set is always the safe baseline. Removing a format from generation is a configuration decision, not a runtime override by any agent or user.

## 5.2 Format Dependency Graph
```mermaid

```

flowchart LR
    APP[Approved Architecture State] --> MD[Markdown Documents]
    APP --> JSON[JSON Export]
    APP --> MMD[Mermaid Sources]
    APP --> DOT[Graphviz DOT Sources]

    DOT --> SVG[SVG Renders]
    SVG --> PNG[PNG Renders]

    MD --> HTML[Interactive HTML Report]
    MMD --> HTML
    SVG --> HTML
6. Markdown Generation
## 6.1 Markdown Deliverables
Markdown generation produces the structured document set defined by the Documentation Agent output contract (AI_AGENT_ARCHITECTURE.md Section 7.5, Agent 13):

High-Level Design (HLD) — architecture overview, component responsibilities, key decisions, trade-off rationale
Low-Level Design (LLD) — component specifications, conceptual schemas, security configurations, API boundaries
Executive Summary — business-facing summary for stakeholder presentation
Assumptions and Constraints Log — all assumptions with their stated basis
Risk Register — prose rendering of the Risk Agent's structured register
## 6.2 Rendering Model
Markdown generation is template-driven. The Documentation Agent produces structured section content; the Markdown Generator applies a versioned Jinja2-style template that arranges sections, formats tables, applies heading conventions, and injects front-matter metadata (document type, version, engagement ID, approval timestamp, template version).

Templates are versioned in configuration (REPOSITORY_MASTER_STRUCTURE.md config/templates/{type}/v{N}/). A template version change never modifies a prior version — it creates a new version directory. The active template version is declared in output configuration and recorded in the file manifest for reproducibility.

## 6.3 Rendering Guarantees
Rendered Markdown is CommonMark-compliant with GitHub-Flavored Markdown extensions (tables, fenced code blocks, task lists).
Every document carries a front-matter block: document type, engagement ID, version, generation timestamp, template version, content hash.
Internal cross-references (e.g., HLD referencing a specific risk in the Risk Register) resolve within the document set.
Character encoding is UTF-8 with no byte-order mark.
Line endings are normalized to LF.
## 6.4 Content Isolation Rule
The Markdown Generator does not introduce content not present in the approved architecture state. It does not summarize, interpret, or elaborate. If a section has no content in the approved state, the corresponding Markdown section renders with an explicit "not specified" marker — never with generator-fabricated content.

7. Interactive HTML Report Generation
## 7.1 HTML Report Character
The HTML report is the primary stakeholder deliverable — a single-file, self-contained, offline-navigable report that presents the complete approved architecture in a professional, interactive format. It is produced by the HTML Report Agent (AI_AGENT_ARCHITECTURE.md Section 7.5, Agent 15) and rendered by the HTML Generator in the Output Layer.

## 7.2 Report Composition
The report consolidates:

Executive Summary section (from Documentation Agent output)
Architecture Overview section with embedded interactive Mermaid diagram
Data Flow section with embedded diagram
Technology Stack section with Build vs Buy summary table
Validation Findings section (Security, Cost, Compliance, Risk — tabbed interactive layout)
Implementation Roadmap section
Full HLD and LLD sections (collapsible)
Appendix: assumptions log, compliance checklist, agent execution metadata
## 7.3 Self-Containment Contract
The generated HTML file is completely self-contained:

All CSS is embedded inline in a <style> block
All JavaScript is embedded inline in <script> blocks
All diagrams are embedded as Mermaid source (rendered in-browser via embedded Mermaid runtime) or as inline SVG
No external CDN dependency for core functionality — the file renders correctly with no network access
Fonts default to system fonts; no external font loading required for legibility
## 7.4 Interactive Capabilities
The HTML report provides in-browser interactivity without requiring a server:

Collapsible sections for long content (HLD, LLD, appendices)
Tab navigation across validation domains
In-page anchor navigation via a persistent table of contents
Print-optimized layout activated by the browser's print action
Zoom and pan on embedded diagrams
## 7.5 Template Versioning
The HTML report template is versioned identically to Markdown templates. The active version is recorded in the file manifest. Template updates never modify existing prior versions.

## 7.6 Size Boundary
The HTML report has a configured maximum file size. Reports exceeding the limit trigger a warning in the manifest — content is retained but the report is flagged for stakeholder-facing size concerns. Oversize reports typically indicate an oversized embedded diagram set; the report generation applies size-optimization heuristics on diagrams before failing.

8. Mermaid Diagram Generation
## 8.1 Mermaid Diagram Types
Mermaid is the primary diagram format for documentation-oriented outputs. The following diagram types are generated per approved architecture:

Diagram	Purpose	Source of Structured Input
Architecture Overview	Major components and their relationships	Architecture Design Agent output
Data Flow	End-to-end data movement (sources → serving zones)	Data Flow Agent output
Security Boundary	Trust zones and data classification boundaries	Security Agent output + Data Flow spec
Component Interaction	Runtime interaction sequence for key flows	Architecture Design Agent + Data Flow spec
## 8.2 Generation Contract
The Diagram Generation Agent (AI_AGENT_ARCHITECTURE.md Section 7.5, Agent 14) produces Mermaid source strings with a diagram title, description, and legend declaration. The Output Layer's Mermaid Generator:

Validates the Mermaid source syntactically (parse-only validation without full rendering)
Applies the style configuration (theme, node colors, edge styles) from config/templates/diagrams/mermaid-theme.yaml
Wraps the source with front-matter comment metadata (diagram type, engagement ID, version, generation timestamp)
Persists the .mmd source file to the bundle
## 8.3 Rendering Responsibility Split
Mermaid source is not rasterized by the Output Layer. It is embedded as source in the Interactive HTML Report (rendered in-browser by the embedded Mermaid runtime) and provided as a .mmd file in the bundle for consumers who render it in their own documentation systems (Notion, Confluence, GitHub, GitLab, developer IDEs).

## 8.4 Mermaid Version Pinning
The embedded Mermaid runtime version in the HTML report is pinned in the HTML template configuration. Version upgrades are template version changes — they never affect prior generated HTML reports.

9. Graphviz DOT Generation
## 9.1 When DOT Is Preferred Over Mermaid
Graphviz DOT is generated for diagram types where Mermaid's expressiveness is insufficient — primarily the Deployment Topology Diagram, where nested clustering (regions containing zones containing subnets containing components), edge routing precision, and layout algorithm control are required.

Diagram	Format
Architecture Overview	Mermaid
Data Flow	Mermaid
Security Boundary	Mermaid
Component Interaction	Mermaid
Deployment Topology	Graphviz DOT (primary) with Mermaid variant where feasible
## 9.2 DOT Generation Contract
The Diagram Generation Agent produces DOT source with:

Cluster declarations for hierarchical zones
Node declarations with shape, color, and label attributes derived from technology selections and infrastructure topology
Edge declarations with directionality, style, and label attributes
Graph-level attributes (layout algorithm, rank direction, splines)
The DOT Generator in the Output Layer applies:

Syntactic validation via a DOT parser
Style configuration from config/templates/diagrams/graphviz-styles.yaml
Front-matter metadata as comment lines
## 9.3 DOT Persistence
The .dot source file is persisted in the bundle for consumers with Graphviz-compatible tooling. It is also the source for SVG and PNG rasterization (Section 10).

10. SVG / PNG Rendering Flow
## 10.1 Rasterization Pipeline
```mermaid

```

flowchart LR
    DOT[Graphviz DOT Source] --> VAL[DOT Syntax Validation]
    VAL --> RENDER[Graphviz Renderer]
    RENDER --> SVG[SVG Output]
    SVG --> POST[SVG Post-Processing<br/>Optimization · Metadata Injection]
    POST --> SVGFILE[Persisted SVG File]
    POST --> PNGCONV[SVG → PNG Conversion]
    PNGCONV --> PNGFILE[Persisted PNG File]

    style DOT fill:#f5f5f5,stroke:#999999
    style SVGFILE fill:#e8f9e8,stroke:#006600
    style PNGFILE fill:#e8f9e8,stroke:#006600
## 10.2 Rendering Contract
SVG is rendered directly by the Graphviz engine from validated DOT source. It is the canonical vector format — scalable, editable, and embeddable in the HTML report.
PNG is derived from SVG through a headless rasterization step. The PNG resolution is configuration-driven with a default suitable for slide-deck embedding (typically 2× the natural pixel size for high-DPI display quality).
## 10.3 Rendering Isolation
Rasterization executes in an isolated rendering context. The renderer:

Consumes no external network resources
Does not execute embedded scripts or external references within the DOT input
Operates under a time budget; a rendering timeout produces a failure record without hanging the pipeline
Operates under a memory budget; oversize diagrams that exceed the budget are flagged rather than rendered incorrectly
## 10.4 Rendering Failure Handling
An SVG rendering failure fails only the SVG (and its downstream PNG). The DOT source is still persisted in the bundle. The manifest documents the SVG/PNG unavailability. Other formats are unaffected — the format-level failure isolation principle (Section 1.2) holds.

11. JSON Export
## 11.1 Purpose
The JSON export is the machine-readable representation of the approved architecture state. It exists to serve downstream integrations, IaC generators (Phase 2), analytics tooling, and any consumer that requires structured architecture data without parsing narrative documents.

## 11.2 Content Contract
The JSON export contains:

Engagement identity and approval attribution (engagement ID, version, approver identity, approval timestamp)
Structured requirements (functional + NFR)
Approved candidate architecture (pattern, components, technology selections, infrastructure topology, data flow)
Validation summary (security posture, TCO summary, compliance status, risk register)
Architect overrides applied to the approved state
Citation index (all knowledge base citations referenced in the approval)
Template and agent version metadata for reproducibility
## 11.3 Schema Contract
The JSON export conforms to a versioned schema declared in configuration. The schema version is embedded in every export as a top-level schema_version field. Schema versions are backward-compatible within a major version. A schema major version change is a breaking change tracked in the platform's API versioning discipline (API_ARCHITECTURE.md Section 3).

## 11.4 Determinism
JSON serialization is deterministic given the same approved snapshot: field ordering is canonical (alphabetical within objects), whitespace is normalized (2-space indentation), and no timestamps except the immutable approval and generation timestamps are embedded. This determinism enables byte-comparable regeneration for audit purposes.

## 11.5 Encoding
UTF-8, no BOM, LF line endings. Strings are stored as-is — no additional escaping beyond the JSON standard requirement.

12. Output Metadata
## 12.1 Per-File Metadata
Every file in a bundle carries the following metadata, recorded in the output_files record (DATABASE_ARCHITECTURE.md Section 5.6):

Field	Description
File identity	UUID; unique per file
Bundle association	Reference to the parent bundle
File type	Enum from the supported types (HLD, LLD, HTML_REPORT, DIAGRAM_MERMAID, etc.)
Storage path	Path in Output Storage
File size	Bytes
Template version	Version of the template applied
Content hash	SHA-256 of the file content for integrity verification
Generation status	SUCCESS / FAILED
Generation timestamp	UTC ISO 8601
## 12.2 Per-Bundle Metadata
Every bundle carries a manifest with:

Field	Description
Bundle identity	UUID
Engagement version reference	The approved architecture version this bundle materializes
Bundle version	Sequential per engagement (1, 2, ...)
Total file count	Expected file count for the bundle spec
Available file count	Files that generated successfully
Generation status	IN_PROGRESS / COMPLETE / PARTIAL / FAILED
Bundle composite hash	SHA-256 over the concatenation of all included file hashes in canonical order
Generation timestamp	UTC ISO 8601
Generator identifiers	Documentation Agent version, Diagram Generation Agent version, HTML Report Agent version used
## 12.3 Reproducibility Property
Given the approval attribution, the bundle manifest, the recorded template versions, and the recorded agent versions, any generated file is fully reconstructable. This is the output layer's contribution to the platform's audit-ready-by-construction guarantee (ARCHITECTURE_VISION.md Section 1).

13. Output Versioning
## 13.1 Version Model
Output bundles are versioned per engagement. Version increments occur when:

The architect approves a refined architecture (a new engagement version triggers a new bundle version)
The architect explicitly triggers output regeneration on the current approved version (a new bundle version is created with the same underlying engagement version but a new bundle number)
## 13.2 Version Lineage
```mermaid

```

flowchart LR
    EV1[Engagement Version 1<br/>Approved] --> B1[Bundle 1.1]
    EV1 --> B2[Bundle 1.2<br/>Regenerated]

    EV2[Engagement Version 2<br/>Approved After Refinement] --> B3[Bundle 2.1]

    EV1 -.supersedes.-> EV2
    B1 -.superseded by.-> B3

    style B3 fill:#e8f9e8,stroke:#006600
## 13.3 Version Immutability
Once a bundle is written and its manifest is recorded, the bundle is immutable. A regenerated bundle is a new bundle with a new identity — not an overwrite. Prior bundles remain retrievable for audit and comparison. This aligns with the constitutional immutability principle (ARCHITECTURE_VISION.md P-06).

## 13.4 "Current" Version Semantics
The current bundle for an engagement is the highest bundle version of the highest engagement version. Prior bundles are accessible through the version selector in the workspace output-viewer module (FRONTEND_MODULE_ARCHITECTURE.md Section 9.8).

14. Output Validation
## 14.1 Two-Stage Validation
Output validation occurs at two stages, each with a distinct concern.

Stage 1 — Per-Format Validation (before inclusion in the bundle):

Format	Validation Concern
Markdown	UTF-8 encoding, CommonMark parseability, front-matter presence, non-empty content
Interactive HTML	Valid HTML5, no external CDN references in production build, embedded diagram references resolve, file size under configured maximum
Mermaid source	Syntactic validity (parse-only), front-matter comment metadata present
Graphviz DOT source	Syntactic validity via DOT parser, front-matter comment metadata present
SVG	Well-formed XML, no external references (<image href>, <script>), namespace correctness
PNG	Valid PNG magic bytes, non-zero dimensions, size under configured maximum
JSON	Valid JSON, conforms to the declared schema version, field ordering canonical
Stage 2 — Bundle-Level Validation (before manifest commit):

At least one file was successfully generated (an entirely empty bundle is a failure)
Every file's stored content hash matches the manifest's declared hash
The bundle's composite hash matches the concatenation of file hashes in canonical order
Required-file presence is checked; if a required file is absent, the bundle status is PARTIAL, not COMPLETE
## 14.2 Validation Failure Handling
Format validation failure produces a FAILED file record with a stored failure reason. Other formats continue generation.
Bundle validation failure (all files failed) produces a FAILED bundle. The architect is notified. Regeneration is available.
## 14.3 Silent Failure Prohibition
An output file that fails validation is never included in a bundle without its failure state being recorded in the manifest. The client-facing output-viewer displays clearly which formats generated successfully and which are unavailable.

15. Output Quality Rules
## 15.1 Content Quality Rules
Rule	Description
No AI hallucination in deliverables	Deliverable content originates from the approved snapshot only; generators do not synthesize additional content
Internal consistency across formats	The same architectural claim appears identically across HLD, LLD, HTML report, and JSON (same component names, same technology selections, same risk findings)
Every recommendation traceable	Every recommendation in the deliverable carries a citation reference that resolves to the citation index in the JSON export
No placeholder text	Deliverables never contain lorem-ipsum, "TODO", or "TBD" markers. Missing content is marked with an explicit "not specified" indicator
No client-identifying leakage where anonymization is declared	Where anonymization is configured, deliverables carry no client name, engagement code, or identifying metadata
## 15.2 Presentation Quality Rules
Rule	Description
Print-ready	HTML reports render correctly when printed; Markdown renders cleanly in standard renderers
Immediately usable	Diagrams can be dropped into presentation software without post-processing; documents can be delivered to clients without cleanup
Consistent typography and layout	Every deliverable of the same type applies the same template, producing visually consistent output across engagements
Accessibility considerations	HTML reports meet basic accessibility standards: semantic HTML, alt text on embedded images where meaningful, sufficient color contrast
## 15.3 Structural Quality Rules
Rule	Description
Deterministic ordering	Sections, tables, and lists have deterministic ordering; regenerating from the same snapshot produces the same order
No dangling references	Every internal reference (e.g., "see risk R-04") resolves within the deliverable set
Diagram legibility	Diagrams do not exceed configured node/edge count without automatic simplification or splitting
Metadata completeness	Every file carries complete generation metadata (template version, agent version, engagement version, generation timestamp)
16. Output Storage Strategy
## 16.1 Storage Boundary
The Output Layer is not the storage implementation — it consumes the OutputStorageService interface (BACKEND_MODULE_ARCHITECTURE.md Layer 7). The underlying storage is object/file storage (cloud object storage in production; filesystem in local development). The Output Layer never writes to the database directly for file content — it writes files through OutputStorageService and writes only the manifest through the repository.

## 16.2 Storage Path Convention
Bundle files are organized under a stable, engagement-scoped path convention:



{output-storage-root}/
  engagements/
    {engagement-id}/
      versions/
        {engagement-version-number}/
          bundles/
            {bundle-version-number}/
              manifest.json
              hld.md
              lld.md
              executive-summary.md
              risk-register.md
              assumptions-log.md
              architecture-overview.mmd
              data-flow.mmd
              security-boundary.mmd
              component-interaction.mmd
              deployment-topology.dot
              deployment-topology.svg
              deployment-topology.png
              architecture-report.html
              architecture-state.json
The path convention is authoritative — it is the mechanism by which files are located, versioned, and lifecycle-managed.

## 16.3 Encryption at Rest
All output files are encrypted at rest under the platform's standard encryption discipline (SECURITY_ARCHITECTURE.md Section 10). Deliverables receive the same protection as their source engagement data — they are not treated as lower-classification content.

## 16.4 Retention
Output bundles are retained for the lifetime of the engagement. On engagement archival, bundles are moved to cold storage but remain retrievable through the standard retrieval path. There is no automatic bundle deletion — deletion requires explicit administrative action and is recorded in the audit stream.

## 16.5 Storage Failure Handling
A failure to persist a file to Output Storage causes the affected file to be marked FAILED in the manifest. The bundle may still be PARTIAL if other files persist successfully. Storage failures are retried per the platform's storage retry policy (BACKEND_MODULE_ARCHITECTURE.md Section 14.3) before being classified as failed.

17. Download Package Structure
## 17.1 Bundle Layout
The download bundle is a structured archive containing all successfully generated files plus the manifest:



architectiq-bundle-{engagement-id}-v{engagement-version}.{bundle-version}.zip
├── manifest.json
├── documents/
│   ├── hld.md
│   ├── lld.md
│   ├── executive-summary.md
│   ├── risk-register.md
│   └── assumptions-log.md
├── diagrams/
│   ├── architecture-overview.mmd
│   ├── data-flow.mmd
│   ├── security-boundary.mmd
│   ├── component-interaction.mmd
│   ├── deployment-topology.dot
│   ├── deployment-topology.svg
│   └── deployment-topology.png
├── report/
│   └── architecture-report.html
└── data/
    └── architecture-state.json
## 17.2 Manifest Contents
The manifest.json at the bundle root contains:

Bundle identity and version
Engagement identity and approved version reference
Approval attribution (approver identity, approval timestamp)
Complete file inventory with per-file metadata (Section 12.1)
Bundle composite hash
Template and agent version identifiers
Generation timestamp
Bundle generation status
Human-readable summary of the approved architecture
## 17.3 Packaging Flow
```mermaid

```

flowchart TD
    A([All Generators Complete]) --> B[Collect Successful Files]
    B --> C[Compute Per-File Hashes]
    C --> D[Assemble Manifest]
    D --> E[Compute Bundle Composite Hash]
    E --> F[Write Files to Bundle Layout]
    F --> G[Serialize Manifest to Bundle Root]
    G --> H[Create Archive]
    H --> I[Persist Archive to Output Storage]
    I --> J[Record output_bundles and output_files]
    J --> K([Bundle Available for Download])

    style A fill:#f5f5f5,stroke:#999999
    style K fill:#e8f9e8,stroke:#006600
## 17.4 Partial Bundle Semantics
A PARTIAL bundle is downloadable — it contains the files that succeeded and a manifest that clearly documents what is missing and why. The architect is presented with the partial state and the option to trigger regeneration of failed formats.

## 17.5 Individual File Download
The bundle model does not preclude individual file download. The API surface exposes both bundle-level download and per-file download (API_ARCHITECTURE.md Section 5.8). Individual downloads are useful when the architect needs only a specific deliverable format for a specific downstream context.

18. Output Security
## 18.1 Access Control
Output access enforces the same ownership discipline as engagement access (SECURITY_ARCHITECTURE.md Section 4.2, SFR-09). A download request:

Requires authenticated identity at the API Gateway
Requires resource-ownership verification at the service layer — the requesting identity must own the parent engagement
Returns 404 on ownership failure (never 403 — SECURITY_ARCHITECTURE.md Section 4.3)
## 18.2 Content Integrity
Every downloaded file's hash is verifiable against the manifest hash. A hash mismatch on retrieval is a critical alert — it indicates storage tampering or corruption.
The manifest itself carries a signature bound to the approval event's Decision Ledger entry, enabling end-to-end integrity verification from approval to download.
## 18.3 Content Sanitization
Outputs are sanitized against the same content classifications as their source engagement data. In particular:

HTML reports include no user-supplied HTML content without escaping. All user-originated text is treated as text, not markup.
Embedded diagram sources are validated against script-injection patterns before being embedded in HTML.
JSON exports exclude any field flagged as internal-only in the schema.
## 18.4 Sensitive Data Handling
If the engagement's data classification prohibits certain content in deliverables (e.g., proprietary client identifiers in an anonymized engagement), the applicable content is redacted before generation, not after. Redaction is a generation input, not a post-generation filter.

## 18.5 Audit Trail for Output Access
Every download event (bundle or individual file) is logged at the API layer with correlation ID, requesting identity, target file, and timestamp. Repeated download attempts across a short window generate a monitoring signal for potential exfiltration behavior.

## 18.6 Delivery Integrity
Downloads are served over HTTPS only (SECURITY_ARCHITECTURE.md Section 10.1). File transfers use content-length headers and support resumable downloads for large bundles. Bundle archives include a checksum manifest for client-side integrity verification post-download.

19. Performance Guidelines
Guideline	Target	Rationale
Markdown generation latency (per document)	< 3 seconds	Template rendering is inexpensive; large documents dominate
HTML report generation latency	< 30 seconds	Composition of all sections with embedded diagrams
Mermaid source generation latency	< 5 seconds per diagram	Structured composition; no rendering at this stage
DOT source generation latency	< 5 seconds per diagram	Structured composition
SVG rendering latency	< 10 seconds per diagram	Bounded by diagram complexity
PNG conversion latency	< 5 seconds per diagram	Direct SVG-to-PNG rasterization
JSON export latency	< 2 seconds	Structured serialization; deterministic ordering
End-to-end bundle generation (full format set)	< 90 seconds (p95)	Aligned with WORKFLOW_ENGINE.md Section 20.2
Bundle download latency (initial byte)	< 500ms	Time-to-first-byte for the archive stream
Concurrent bundle generation capacity	≥ 10 simultaneous bundles	Matches concurrent-engagement targets
Diagram complexity limits	Configurable node/edge count per diagram	Prevents oversize diagrams from degrading rendering
Output storage IOPS budget	Bounded per engagement	Prevents a single engagement from monopolizing storage bandwidth
## 19.1 Parallelism
Format generation across independent formats runs in parallel within the pipeline. The dependency graph (Section 5.2) is respected: rasterization waits for DOT; HTML report finalization waits for its embedded diagrams and its Markdown source.

## 19.2 Streaming Progress
The generation pipeline emits progress events per completed format to the Progress Broadcaster (SYSTEM_ARCHITECTURE.md Section 4.12), enabling the workspace output-viewer to render outputs progressively as they become available — the architect does not wait for the entire bundle before seeing the first available format.

## 19.3 Caching
Template loading is cached at the generator level (template cache invalidated only on configuration update). Repeated generation of the same approved snapshot with the same template versions leverages the template cache but always regenerates the file content — output files are never served from a stale cache.

20. Future Extension
## 20.1 Phase-2 Format Additions
PDF generation — professional PDF documents produced from the HTML report via a headless renderer; reserved format registration in the OutputGeneratorFactory (BACKEND_MODULE_ARCHITECTURE.md Section 9.2). PDF is planned but not in V1 scope (IMPLEMENTATION_SPECIFICATION.md Section 7.3).
Infrastructure-as-Code scaffolding — Terraform and Bicep module scaffolding generated from the approved deployment topology (DATA_SOLUTION_ARCHITECTURE.md Section 14; Phase 2 in the roadmap).
Presentation-format outputs — slide-compatible architecture summaries for executive review.
CSV/Excel exports — tabular exports of technology selections, cost models, and risk registers for downstream analytics.
## 20.2 Rendering Extensions
PlantUML source generation — alternative diagram source for organizations standardized on PlantUML tooling.
Interactive diagram authoring — editable diagrams within the HTML report, with edits captured as new refinement input for a follow-on engagement.
Multi-page HTML reports — for very large architectures, a linked multi-page HTML structure with cross-page navigation.
## 20.3 Delivery Channel Extensions
Notification-triggered delivery — bundle-ready notifications delivered via email, Slack, or Teams through the NotificationProvider (BACKEND_MODULE_ARCHITECTURE.md Section 7.7; Phase 2).
Enterprise integration delivery — direct publication of approved deliverables to Confluence, SharePoint, or enterprise document management systems.
Client portal delivery — controlled external sharing of specific deliverables with time-bounded access tokens.
## 20.4 Quality Extensions
Automated deliverable review scoring — quality rubric scoring on generated content (readability, completeness, consistency) with quality metrics tracked over time.
Deliverable comparison tooling — visual diff of deliverables across engagement versions, useful for change review boards.
Template A/B evaluation — controlled comparison of template versions against architect satisfaction signals.
## 20.5 Deliverable Lineage Extensions
Signed deliverables — cryptographic signatures on the manifest bound to the approving architect's identity, enabling third-party verification of authenticity.
Deliverable provenance chain — linking each deliverable back to the specific knowledge base entries that grounded its recommendations, expanding beyond citation index to full provenance graph.
21. Document Status and Metadata
Document Status
Field	Value
Status	Approved — Foundation Release
Version	1.0.0
Classification	Output Generation Architecture — Source of Truth
LLM Provider Assumption	OpenAI (current implementation; architecture is provider-independent)
Dependencies
ARCHITECTURE_VISION.md v1.0.0 — Immutability principle, audit-ready-by-construction, expected deliverables
SYSTEM_ARCHITECTURE.md v1.0.0 — Output Generator component, Progress Broadcaster, storage boundary
BACKEND_MODULE_ARCHITECTURE.md v1.0.0 — Output Layer modules, OutputGeneratorFactory, OutputStorageService, OutputPackager
AI_AGENT_ARCHITECTURE.md v1.0.0 — Documentation Agent, Diagram Generation Agent, HTML Report Agent contracts
WORKFLOW_ENGINE.md v1.0.0 — Generation Phase (Stages 14–17), approval-gated generation trigger
DATA_SOLUTION_ARCHITECTURE.md v1.0.0 — Approved architecture snapshot as generation input
SECURITY_ARCHITECTURE.md v1.0.0 — Output encryption, access control, integrity guarantees
DATABASE_ARCHITECTURE.md v1.0.0 — output_bundles and output_files schemas
API_ARCHITECTURE.md v1.0.0 — Output endpoints, per-file and bundle-level download contracts
IMPLEMENTATION_SPECIFICATION.md v1.0.0 — MVP format scope and Phase-2 boundaries
Related Documents
Document	Relationship
FRONTEND_MODULE_ARCHITECTURE.md	Defines the output-viewer module that consumes generated deliverables
KNOWLEDGE_ENGINE.md	Provides the citation index referenced in the JSON export
Future Extension
PDF generation activation via the reserved pdf_generator module
IaC scaffolding generation via the reserved iac_generator module
Multi-provider LLM support without changes to output generation
Signed deliverables and provenance graph expansion
Version: 1.0.0

End of OUTPUT_GENERATION_ARCHITECTURE.md