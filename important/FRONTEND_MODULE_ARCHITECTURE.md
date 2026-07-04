# FRONTEND_MODULE_ARCHITECTURE.md

> **Document Classification:** Frontend Architecture — Source of Truth  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0 · SYSTEM_ARCHITECTURE.md v1.0.0 · BACKEND_MODULE_ARCHITECTURE.md v1.0.0  
> **Status:** Approved — Foundation Release  
> **Version:** 1.0.0  
> **Scope:** Complete frontend architecture — all modules, all layers, all interaction patterns, all state ownership, all rendering strategies  
> **Authority:** Every frontend implementation decision must be consistent with the architecture defined here. This document is the frontend engineering constitution.

---

## Table of Contents

1. [Frontend Philosophy](#1-frontend-philosophy)
2. [Overall Frontend Architecture](#2-overall-frontend-architecture)
3. [Frontend Layers](#3-frontend-layers)
4. [Module Architecture](#4-module-architecture)
5. [Component Strategy](#5-component-strategy)
6. [Routing Strategy](#6-routing-strategy)
7. [State Management](#7-state-management)
8. [Chat Experience](#8-chat-experience)
9. [Workspace Architecture](#9-workspace-architecture)
10. [UI Layout Strategy](#10-ui-layout-strategy)
11. [Frontend Service Layer](#11-frontend-service-layer)
12. [Performance Strategy](#12-performance-strategy)
13. [Accessibility](#13-accessibility)
14. [Theme Architecture](#14-theme-architecture)
15. [Error Experience](#15-error-experience)
16. [Frontend Extension Strategy](#16-frontend-extension-strategy)
17. [Frontend Validation Checklist](#17-frontend-validation-checklist)
18. [Frontend Freeze Rules](#18-frontend-freeze-rules)

---

## 1. Frontend Philosophy

### 1.1 Purpose

The ArchitectIQ frontend is the instrument through which a Data Solution Architect conducts their work. It is not a dashboard. It is not a form. It is not an admin panel. It is a professional workspace — a spatially organized, session-aware, real-time collaborative environment in which an architect and an AI pipeline produce governed architecture artifacts together.

The frontend's purpose is to make complex, long-running, multi-step AI workflow feel simple, clear, and in control. At every moment, the architect must know: where they are in the engagement, what the AI has produced, what decisions they need to make, and what outputs are available. The interface is the transparency layer between the AI pipeline and the human architect.

### 1.2 Core Responsibilities

The frontend is exclusively responsible for:

- Rendering the three-panel workspace (Sessions | Chat | Workspace) as the canonical interaction model
- Managing GitHub OAuth authentication flow on the client side
- Persisting and restoring session state across logins without requiring the architect to re-submit their work
- Receiving and progressively rendering streaming pipeline output from the backend
- Presenting the human review gate with all agent outputs, validation findings, and citations consolidated for architect decision
- Displaying generated outputs — architecture diagrams, Markdown documents, interactive HTML, JSON — in their appropriate renderers
- Managing client-side state with strict ownership boundaries per domain
- Communicating with the backend exclusively through the API service layer

### 1.3 Design Goals

**Clarity over complexity.** The architect should never feel lost. At every moment, the application's state is visible — which session is active, which engagement is running, which pipeline stage is executing, which sections are ready for review. Information architecture is the primary design concern.

**Progressive disclosure.** The application reveals detail proportional to the architect's current need. A pipeline in progress shows a compact stage summary. A completed stage expands its output on demand. A review gate presents all evidence in a structured, navigable format — not all at once, but contextually available.

**Streaming as the default.** The frontend is designed for streaming-first rendering. Every section of the workspace panel updates progressively as pipeline output arrives. The architect never stares at an empty workspace waiting for a complete result — they see output building in real time.

**Session continuity as a professional requirement.** The frontend treats session restoration as a first-class feature. An architect who closes their browser and returns the next day resumes exactly where they left off — same conversation, same workspace sections, same engagement state. Losing context between sessions is a professional failure mode.

**Enterprise quality without enterprise friction.** The application should feel as immediate and fluid as a consumer product while meeting the quality bar of enterprise software: keyboard navigable, screen-reader compatible, high contrast, and responsive across professional screen sizes.

### 1.4 Boundaries

The frontend renders state — it does not enforce business rules. All business logic, all governance enforcement, and all AI execution belongs to the backend. The frontend's job is to make the backend's outputs visible, navigable, and actionable.

The frontend communicates with one system: the API Gateway. It does not communicate directly with any backend service, any agent, or any infrastructure component. It does not know that agents exist — it knows that a pipeline is executing and that outputs arrive progressively.

---

## 2. Overall Frontend Architecture

### 2.1 Architectural Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BROWSER RUNTIME                                    │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        APPLICATION SHELL                               │  │
│  │    Router · Auth Guard · Theme Provider · Global Error Boundary         │  │
│  │    Notification Manager · Streaming Connection Manager                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                     THREE-PANEL WORKSPACE                             │   │
│  │                                                                       │   │
│  │  ┌─────────────┐   ┌─────────────────────┐   ┌──────────────────┐  │   │
│  │  │   SESSIONS   │   │        CHAT          │   │    WORKSPACE     │  │   │
│  │  │    PANEL     │   │       PANEL          │   │     PANEL        │  │   │
│  │  │  (Left)      │   │    (Center)          │   │    (Right)       │  │   │
│  │  │             │   │                      │   │                  │  │   │
│  │  │ Session List │   │ Conversation Thread  │   │ Requirements     │  │   │
│  │  │ History      │   │ Streaming Messages   │   │ Architecture     │  │   │
│  │  │ Search       │   │ Progress Indicators  │   │ Validation       │  │   │
│  │  │ New Session  │   │ Input Area           │   │ Review Gate      │  │   │
│  │  │             │   │ Attachment Handling   │   │ Outputs          │  │   │
│  │  └─────────────┘   └─────────────────────┘   └──────────────────┘  │   │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                      STATE MANAGEMENT LAYER                           │   │
│  │  Auth Store · Session Store · Chat Store · Workspace Store           │   │
│  │  Engagement Store · Streaming Store · Notification Store             │   │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                       SERVICE LAYER                                   │   │
│  │  ApiClient · AuthService · SessionService · ChatService               │   │
│  │  EngagementService · OutputService · StreamingService                │   │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │ HTTPS / WebSocket
                                     ▼
                              API GATEWAY (backend)
```

### 2.2 Communication Architecture

The frontend communicates with the backend through two channels:

**HTTP (REST):** State-changing operations and data retrieval. Used for: authentication, session creation and retrieval, engagement commands (create, approve, refine, reject), output file retrieval, conversation history pagination. All HTTP calls pass through the `ApiClient` base class which attaches authentication tokens, correlation IDs, and handles response normalization.

**Streaming (WebSocket or Server-Sent Events):** Real-time pipeline progress and workspace section updates. Used for: agent stage progress events, workspace section content delivery, typing indicators, pipeline completion signals, and human review gate triggers. The `StreamingService` manages the connection lifecycle, reconnection, and event dispatch to the appropriate stores.

**Separation invariant:** HTTP calls update persistent state (server-authoritative data). Streaming events update ephemeral display state (what is currently visible in the workspace). On session restore, HTTP calls reconstruct the full state from the server. Streaming reconnects deliver missed events since the last known position.

---

## 3. Frontend Layers

### Layer 1 — Presentation Layer

**Purpose:** The visible surface of the application. Renders UI components into the DOM. Responds to user interactions. Displays state provided by the Feature Layer.

**Responsibilities:**
- Render all visible UI components (panels, messages, workspace sections, review gates, output viewers)
- Handle user interaction events and delegate them to stores or services
- Apply visual theming through design tokens
- Manage focus, keyboard navigation, and ARIA attributes
- Render streaming content progressively as it arrives

**Allowed dependencies:** Feature Layer components (via composition), Shared Component Layer, State Management Layer (read-only access to store state), Theme Layer.

**Forbidden dependencies:** Service Layer (direct API calls from components are forbidden — all API calls originate from hooks that delegate to the Service Layer), business logic beyond presentation concerns.

---

### Layer 2 — Feature Layer

**Purpose:** Contains the domain-specific UI logic for each product feature. Feature modules own the connection between the UI and the state stores for their domain.

**Responsibilities:**
- Implement all feature-specific container components
- Connect store state to presentational components through custom hooks
- Handle feature-specific user interactions and dispatch to stores
- Manage feature-specific loading, error, and empty states
- Coordinate multi-step user flows within a feature boundary

**Allowed dependencies:** Shared Component Layer, State Management Layer (read and write), Service Layer hooks, Utility Layer.

**Forbidden dependencies:** Other feature modules' internal implementations (features communicate through stores, not through direct import). A feature module may import from the Shared Component Layer but never from another feature module's private components.

---

### Layer 3 — Shared Component Layer

**Purpose:** A library of domain-neutral, reusable UI components that are shared across all feature modules. No business logic. No API calls. No store access.

**Responsibilities:**
- Provide the design system component library (Button, Card, Modal, Badge, Spinner, Tooltip, etc.)
- Provide layout primitives (Panel, Container, Grid, Stack, Divider)
- Provide display utilities (Icon, Avatar, StatusIndicator, ProgressBar, EmptyState)
- Ensure all shared components meet accessibility requirements
- Apply design tokens from the Theme Layer

**Allowed dependencies:** Theme Layer (for design tokens), Utility Layer (for formatting helpers), Accessibility utilities.

**Forbidden dependencies:** Feature modules, State Management Layer, Service Layer. Shared components receive everything they need through props. They never access global state.

---

### Layer 4 — State Management Layer

**Purpose:** The client-side data model. Manages all application state with strict ownership boundaries — each domain owns its own store with no cross-store direct dependency.

**Responsibilities:**
- Maintain the authoritative client-side state for each domain (auth, session, chat, workspace, engagement, streaming, notifications)
- Provide reactive state subscriptions to UI components
- Coordinate state updates triggered by user interactions, API responses, and streaming events
- Manage state persistence (session storage for page-refresh survival, secure storage for auth tokens)
- Implement optimistic updates where appropriate with rollback on failure

**Allowed dependencies:** Service Layer (for triggering API calls that update state), Utility Layer.

**Forbidden dependencies:** Presentation Layer components, Feature Layer components, direct DOM manipulation. Stores are pure data with actions — they have no rendering concern.

---

### Layer 5 — Service Layer

**Purpose:** All communication with the backend API. The only layer that makes HTTP calls or manages streaming connections.

**Responsibilities:**
- Issue HTTP requests through the `ApiClient` with authentication, correlation IDs, and error normalization
- Manage the streaming connection lifecycle through the `StreamingService`
- Translate HTTP responses and streaming events into typed domain models
- Handle retries, timeouts, and network-level error recovery
- Provide typed async functions that stores invoke to fetch or mutate server state

**Allowed dependencies:** Utility Layer (for request building and response parsing), Type Layer (for request and response type definitions).

**Forbidden dependencies:** State Management Layer (services do not write to stores — they return results that the store's action handler writes), Presentation Layer, Feature Layer. Services are pure communication functions.

---

### Layer 6 — Utility Layer

**Purpose:** Domain-neutral utility functions for common operations.

**Responsibilities:**
- Date and timestamp formatting (all UTC to local display conversion)
- Markdown rendering utilities
- Diagram source rendering coordination (Mermaid, Graphviz)
- Error parsing and user-friendly message extraction
- Text truncation and search highlighting utilities
- Type guard utilities

**Allowed dependencies:** Standard browser APIs, approved utility libraries only.

**Forbidden dependencies:** All other frontend layers. If a utility requires state or API access, it belongs in a different layer.

---

### Layer 7 — Configuration Layer

**Purpose:** All frontend configuration values in one location. No magic numbers, no hardcoded strings that change between environments.

**Responsibilities:**
- Environment-specific API base URL configuration
- WebSocket endpoint configuration
- Feature flag values (propagated from the backend configuration API on startup)
- Timeout and retry configuration for the Service Layer
- Theme default configuration
- Route path constants

**Allowed dependencies:** None — configuration values are primitive constants.

**Forbidden dependencies:** No runtime logic. Configuration is loaded at application startup and is read-only thereafter.

---

### Layer 8 — Theme Layer

**Purpose:** Design tokens, typography, spacing scale, color system, and icon library that define the visual identity of the application.

**Responsibilities:**
- Define the complete design token set (colors, spacing, typography, border radius, elevation, motion)
- Manage the active theme (light, dark, system-preference)
- Provide CSS custom properties that all components consume
- Define the responsive breakpoint system
- Provide the icon set with consistent sizing

**Allowed dependencies:** None — the theme layer is consumed by all other layers but consumes nothing.

---

## 4. Module Architecture

Modules are organized by feature domain. Each module owns a cohesive set of components, hooks, and types for one user-facing capability.

### 4.1 `auth` Module

**Single Responsibility:** Manages the GitHub OAuth authentication flow on the client side.

**Owns:**
- The Login page (rendered when no valid session token exists)
- The OAuth redirect handler (receives the code, exchanges via the backend, stores the platform token)
- The auth state (token presence, expiry, identity display)
- The token storage strategy (secure, httpOnly where possible)
- The authenticated identity display (avatar, name in the application shell)

**What it never owns:** Business logic about what the user can do after login. Post-login navigation. Session restoration (owned by the `sessions` module).

**Interaction pattern:** On application load, the auth module checks for a valid platform token. If absent, it renders the Login page. If present, it validates the token and hands control to the session restoration flow. OAuth callback handling is a transient page that completes the exchange and redirects to the workspace.

---

### 4.2 `sessions` Module

**Single Responsibility:** Manages the Sessions Panel — the left sidebar that displays the architect's engagement history and enables session navigation and restoration.

**Owns:**
- The Sessions Panel container and its collapsed/expanded state
- The session list (grouped by recency: Today, Yesterday, Previous 7 Days, Previous 30 Days, Older)
- The session card (showing session name, last active timestamp, engagement count, status indicator)
- The new session trigger (creates a new session and initializes a blank workspace)
- The session search (filters the session list by name or content keyword)
- The session rename interaction (inline editing of session name)
- The session deletion interaction (with confirmation)
- Session loading state (skeleton while history is fetching)
- Session restore coordination (triggers workspace reconstruction on session click)

**What it never owns:** Chat content rendering, workspace content, engagement execution, output display.

**Interaction pattern:** The session list is loaded on authentication. Clicking a session card triggers session restoration — the Chat Panel scrolls to the bottom of the conversation history, and the Workspace Panel reconstructs the last known workspace state for that session's active engagement.

---

### 4.3 `chat` Module

**Single Responsibility:** Manages the Chat Panel — the center panel that is the primary conversational interaction surface between the architect and the platform.

**Owns:**
- The Chat Panel container with its message thread and input area
- The user message component (architect's text input rendered as a message bubble)
- The assistant message component (AI pipeline response rendered as a structured message)
- The streaming message component (progressively renders the current streaming assistant message)
- The typing indicator (shown while the pipeline is executing and no content has yet streamed)
- The agent stage progress indicator (shows which pipeline stage is currently active with its status badge)
- The pipeline completion notice (signals that the workspace has been updated with new output)
- The human review gate notice in the chat (a prompt that draws the architect's attention to the workspace panel for review)
- The chat input area: text input, file attachment trigger, submit button, character count, keyboard shortcuts
- The conversation history scroll management (infinite scroll upward for history, auto-scroll to bottom for new messages)
- The attachment preview (shows uploaded document before submission)
- The empty state (shown before the first message in a new session)

**What it never owns:** Workspace content rendering, session navigation, output display, diagram rendering. The chat module knows that a pipeline is running and can display its progress — it does not know what agents are or what they produce. It displays what the streaming service delivers.

**Interaction model:** The input area is the architect's primary interaction point. Text is submitted by Enter (or Shift+Enter for newline). File attachments (requirement documents) are attached via a dedicated trigger. On submission, the user's message renders immediately (optimistic), the assistant streaming message begins rendering as pipeline output arrives, and the workspace panel updates progressively in parallel.

---

### 4.4 `workspace` Module

**Single Responsibility:** Manages the Workspace Panel — the right panel that displays the evolving architecture artifact, all agent outputs, the human review gate, and generated deliverables.

**Owns:**
- The Workspace Panel container and its section navigation
- The workspace section tabs (Requirements, Architecture, Validation, Review, Outputs, Ledger)
- The workspace section header (section name, status badge, last updated timestamp)
- The workspace empty state (shown before pipeline execution begins)
- The workspace loading state (section-level skeletons during streaming)
- The workspace completion state (all sections populated, review gate open or outputs available)
- The workspace version selector (for engagements with multiple approved versions)
- The workspace section-level error state (individual section fails without affecting other sections)

**What it never owns:** Rendering of specific content types — that is delegated to the `artifacts`, `diagram-viewer`, `output-viewer`, and `review` modules, which the workspace panel hosts through composition.

**Section ownership map:**

| Tab | Hosting Module | Renders |
|-----|---------------|---------|
| Requirements | `artifacts` module | Structured requirements, ambiguity flags, confidence scores |
| Architecture | `artifacts` module | Candidate architecture cards with trade-off rationale |
| Validation | `artifacts` module | Security findings, TCO model, compliance checklist, risk register |
| Review | `review` module | Complete review gate with decision controls |
| Outputs | `output-viewer` module | Generated documents and diagrams with download and preview |
| Ledger | `ledger-viewer` module | Decision audit trail for the current engagement |

---

### 4.5 `artifacts` Module

**Single Responsibility:** Renders structured AI-generated content in the workspace panel's Requirements, Architecture, and Validation tabs.

**Owns:**
- Requirements artifact renderer (structured requirement fields, ambiguity flag badges, confidence meters)
- Candidate architecture card (architecture pattern name, rationale, trade-off table, component list)
- Architecture comparison view (side-by-side comparison of multiple candidates)
- Validation finding renderers: threat model summary, TCO model table, compliance checklist, risk register table
- Confidence score display (visual indicator with score and source explanation)
- Citation display (expandable source reference with knowledge base entry details)
- Agent output metadata (agent ID, version, execution time, token count — collapsed by default)

**What it never owns:** Diagram rendering (owned by `diagram-viewer`), document file rendering (owned by `output-viewer`), review controls (owned by `review`), chat messages.

---

### 4.6 `diagram-viewer` Module

**Single Responsibility:** Renders architecture diagrams in all supported formats within the Workspace Panel.

**Owns:**
- Mermaid diagram renderer (renders Mermaid source into SVG in the browser)
- Graphviz DOT diagram renderer (renders DOT source via server-side or browser-side rendering)
- Diagram toolbar (zoom in/out, fit-to-screen, fullscreen, copy source, download SVG/PNG)
- Diagram source toggle (switch between rendered view and source view)
- Diagram loading state (spinner during render computation)
- Diagram error state (render failure with source fallback)
- Diagram fullscreen overlay (expanded view for complex diagrams)

**What it never owns:** Diagram content generation (owned by the backend Documentation Agent), workspace section management.

---

### 4.7 `review` Module

**Single Responsibility:** Renders the human review gate in the Workspace Panel's Review tab — the structured interface through which an architect reviews the AI-generated proposal and makes their governance decision.

**Owns:**
- Review gate container (visible only when engagement is in PENDING_HUMAN_REVIEW state)
- Proposal summary header (engagement ID, pipeline version, timestamp of generation)
- Review checklist (structured list of findings requiring architect acknowledgment: governance violations, low-confidence recommendations, open ambiguities)
- Decision controls: Approve button, Request Refinement button, Reject button — with confirmation dialogs for non-approve actions
- Refinement feedback input (structured text area for refinement guidance, with scope selector: which aspect to refine)
- Rejection reason input (required text before rejection confirmation)
- Override controls (inline editing for direct component-level overrides within the workspace artifacts)
- Review iteration tracker (shows current review cycle number and prior cycles with their decisions)
- Approval confirmation overlay (name, timestamp, and commitment statement before final approval)

**What it never owns:** The underlying artifact rendering (hosted from the `artifacts` module within the review context), decision execution (delegated to the Engagement Store which calls the API), workspace navigation.

**Critical UX constraint:** The Approve button is visually prominent but never the default focus. The architect must actively navigate to it. The review module ensures the architect has had the opportunity to inspect all sections before the approval controls are fully enabled — a progress indicator shows which sections have been scrolled/viewed.

---

### 4.8 `output-viewer` Module

**Single Responsibility:** Renders and enables access to all generated output artifacts in the Workspace Panel's Outputs tab.

**Owns:**
- Output bundle display (list of available output files with format badges)
- Markdown document preview (rendered Markdown with table of contents navigation)
- Interactive HTML preview (sandboxed iframe rendering of interactive HTML outputs)
- PDF viewer link (opens PDF in browser native viewer or triggers download)
- JSON explorer (collapsible tree view of machine-readable architecture state)
- Output download controls (individual file download, full bundle download)
- Output version selector (access prior approved architecture versions' outputs)
- Output regeneration trigger (re-trigger output generation when an approved architecture changes)
- Empty state (shown before architecture approval)

**What it never owns:** Diagram rendering (delegated to `diagram-viewer`), document generation (backend responsibility), review controls.

---

### 4.9 `ledger-viewer` Module

**Single Responsibility:** Renders the Decision Ledger audit trail for the current engagement in the Workspace Panel's Ledger tab.

**Owns:**
- Ledger entry list (chronological, with event type icons, timestamps, and actor attribution)
- Ledger entry detail panel (expanded view of a specific entry: full payload, hash, predecessor reference)
- Event type filter (filter entries by type: proposal, approval, refinement, override, rejection)
- Entry integrity indicator (visual confirmation that hash chain verification passed)
- Entry attribution display (architect name, identity, timestamp for human-action events)

**What it never owns:** Ledger data writing (backend responsibility), business decisions based on ledger content.

---

### 4.10 `notifications` Module

**Single Responsibility:** Manages in-application notifications — transient alerts and persistent notification history.

**Owns:**
- Toast notification system (transient, auto-dismissing alerts positioned in the application shell)
- Notification types: success, info, warning, error — each with distinct visual treatment
- Notification queue (manages simultaneous notifications with stacking and FIFO dismissal)
- Notification center (persistent dropdown accessible from the application shell, showing notification history)
- Notification for pipeline completion (architect attention signal when a pipeline stage completes while they are in another context)
- Notification for review gate open (proactive signal when the workspace review tab is ready)

**What it never owns:** Application alerts that are part of specific module flows (those are module-level error states, not global notifications).

---

### 4.11 `settings` Module

**Single Responsibility:** User preferences and application configuration accessible to the architect.

**Owns:**
- Settings page container and navigation
- Profile settings (display name, notification preferences)
- Workspace preferences (default panel widths, default diagram format, dark/light theme toggle)
- Session preferences (session expiry settings, auto-restore behavior)
- Output format preferences (which output formats are generated by default)
- Keyboard shortcut reference panel
- API usage display (token consumption summary for the current billing period — future capability)

**What it never owns:** System configuration (backend responsibility), user management (admin capability), knowledge base curation.

---

### 4.12 `history` Module

**Single Responsibility:** A dedicated full-page history view for searching and navigating across all past engagements beyond what the Sessions Panel displays.

**Owns:**
- Full engagement history table (paginated, sortable by date, status, domain)
- Engagement status filter (completed, in-review, failed, rejected)
- Date range filter
- Domain/type filter
- Engagement search (by requirement input keyword)
- Engagement detail preview (hoverable card showing engagement summary without navigating away)
- Engagement restore action (navigate to the session containing the selected engagement)

**What it never owns:** Session sidebar management (owned by `sessions` module), workspace rendering.

---

### 4.13 `shared` UI Module

**Single Responsibility:** The application's design system component library. Domain-neutral, composable, accessible UI primitives.

**Owns all shared components:**

| Component | Purpose |
|-----------|---------|
| `Button` | Primary, secondary, ghost, destructive, icon variants |
| `Badge` | Status, count, label with color and size variants |
| `Card` | Container with header, body, footer regions |
| `Modal` | Overlay dialog with focus trap and escape handling |
| `Drawer` | Side panel overlay (used for detail views) |
| `Spinner` | Loading indicator with size variants |
| `Skeleton` | Content placeholder during loading |
| `Tooltip` | Contextual label on hover/focus |
| `Popover` | Inline overlay for contextual content |
| `Tabs` | Horizontal and vertical tab navigation |
| `Accordion` | Collapsible content sections |
| `ProgressBar` | Linear and radial progress indicators |
| `StatusIndicator` | Colored dot with status label |
| `Avatar` | User identity display with fallback initials |
| `EmptyState` | Structured empty content placeholder with action |
| `ErrorBoundary` | React error boundary wrapper with recovery UI |
| `MarkdownRenderer` | Safe Markdown-to-HTML rendering |
| `CodeBlock` | Syntax-highlighted code display with copy |
| `Table` | Sortable, paginated data table |
| `Divider` | Horizontal and vertical separators |
| `Icon` | Icon wrapper with consistent sizing from the icon set |
| `ConfidenceBar` | Visual indicator for agent confidence scores |
| `CitationTag` | Linked citation reference display |

---

## 5. Component Strategy

### 5.1 Component Classification

Every component in the frontend is classified into exactly one of four categories. The category determines its allowed dependencies and its design constraints.

**Container Components**
- Manage state connections and data fetching (via hooks)
- Compose presentational components with data
- Handle user interactions and dispatch to stores or services
- Live in feature module directories
- Have no visual styling of their own — they render presentational components

**Presentational Components**
- Receive all data through props — no store access, no service calls
- Are pure rendering functions
- Are the testable, reusable visual units of the application
- Live in the `shared` module (if domain-neutral) or the feature module (if domain-specific)
- Apply design tokens from the Theme Layer

**Layout Components**
- Manage spatial arrangement — the three-panel layout, panel resize behavior, responsive collapse
- Have no domain knowledge
- Accept children through composition slots
- Live in `components/layouts/`

**Utility Components**
- Provide non-visual behavior: error boundaries, focus managers, intersection observers, portal mounts
- Have no visual rendering of their own
- Wrap other components to add behavior

### 5.2 Composition Strategy

The frontend uses composition as the primary pattern for building complex UI from simple parts. Feature modules do not create complex monolithic components — they compose smaller, specialized components from the `shared` module and their own domain-specific presentational components.

**Slot-based composition:** Layout components accept named slot props for their regions (e.g., the three-panel layout accepts `sessionsPanel`, `chatPanel`, `workspacePanel` as slot props). This makes the layout testable independently of its content and makes the content replaceable without modifying the layout.

**Hook-based behavior injection:** Container components do not implement their data-fetching logic inline. They use custom hooks that encapsulate the state access and service delegation. The hook is the unit of behavior; the component is the unit of rendering.

**No prop drilling beyond two levels.** If a prop must pass through more than two component levels to reach its consumer, that prop belongs in a store, not in the prop chain.

### 5.3 Component Naming Convention

| Pattern | Example | Usage |
|---------|---------|-------|
| `{Domain}{Role}` | `SessionCard`, `ChatMessage`, `WorkspacePanel` | Domain-specific components |
| `{Concept}{Variant}` | `ButtonPrimary`, `BadgeStatus`, `InputText` | Shared component variants |
| `use{Domain}{Behavior}` | `useSessionRestore`, `useChatStreaming`, `useWorkspaceState` | Custom hooks |
| `{Domain}Store` | `SessionStore`, `ChatStore`, `EngagementStore` | State store names |
| `{Domain}Service` | `SessionService`, `ChatService`, `OutputService` | Service names |

---

## 6. Routing Strategy

### 6.1 Route Architecture

The application uses a client-side routing strategy with the following route structure:

```
/login                          — Unauthenticated entry point
  └── OAuth callback handler   — Completes GitHub OAuth exchange

/workspace                      — Main application (requires authentication)
  ├── (default)                 — Restores the most recent session or creates a new one
  ├── /workspace/:sessionId     — Specific session workspace
  └── /workspace/:sessionId/engagement/:engagementId  — Specific engagement in session

/history                        — Full engagement history view (requires authentication)

/settings                       — User settings (requires authentication)

/404                            — Not found fallback
```

### 6.2 Route Protection

**Authentication guard:** All routes except `/login` and the OAuth callback path require a valid platform token. An unauthenticated request to any protected route is redirected to `/login` with the original route preserved as a post-login redirect target.

**Engagement ownership guard:** Navigating to a specific engagement ID validates that the authenticated user owns that engagement. An unauthorized engagement ID results in a 404 display (not a 403 — existence of another user's engagement is not disclosed).

### 6.3 Navigation Philosophy

**URL reflects workspace state.** The session ID in the URL is the primary workspace identity. An architect can bookmark a session URL and return to it. The URL is shareable with colleagues (if they have appropriate access — future capability).

**Navigation does not lose work.** A user navigating to the history page from an active chat does not lose the chat state — the chat continues and the streaming connection is maintained. Navigation between sections within the workspace panel does not reload data.

**Session switching does not reload the page.** Clicking a different session in the Sessions Panel updates the URL and reconstructs the workspace from the new session's state — it does not do a full page reload.

### 6.4 Workspace Navigation Flow

```
User opens application
    ↓
Auth guard validates token
    ↓ (valid)
Session restore: check for last active session
    ↓ (session found)
Navigate to /workspace/:sessionId
    ↓
Workspace reconstructed from session state
    ↓ (engagement active in PENDING_HUMAN_REVIEW)
Workspace opens to Review tab automatically
    ↓ (engagement COMPLETED with outputs)
Workspace opens to Outputs tab automatically
    ↓ (new session or blank engagement)
Workspace shows empty state with input prompt
```

---

## 7. State Management

### 7.1 State Ownership Principles

**One store per domain.** Each domain has one store that owns all state for that domain. No domain state is split across two stores. No store reaches into another store's state — stores communicate through action sequences, not through direct state access.

**Server state and client state are separated.** Server-authoritative data (session records, engagement state, generated outputs, ledger entries) is managed through a server state cache. Client-only state (panel widths, which workspace tab is active, streaming buffer content) is managed in client state stores.

**Stores do not call each other.** If an action in Store A needs to trigger an update in Store B, the triggering component's handler dispatches to both stores sequentially. Stores do not import other stores.

### 7.2 Store Definitions

#### `AuthStore`

**Owns:** The authenticated identity, the platform token reference (not the token value — stored securely), the token expiry time, and the authentication status.

**State shape:** `{ status: 'loading' | 'authenticated' | 'unauthenticated' | 'expired', identity: Identity | null, tokenExpiresAt: Timestamp | null }`

**Actions:** `login(identity)`, `logout()`, `refreshToken()`, `setExpired()`.

---

#### `SessionStore`

**Owns:** The session list (for the Sessions Panel), the active session reference, the session loading state, and session metadata.

**State shape:** `{ sessions: Session[], activeSessionId: string | null, loadingState: LoadingState, searchQuery: string }`

**Actions:** `loadSessions()`, `setActiveSession(sessionId)`, `createSession()`, `renameSession(sessionId, name)`, `deleteSession(sessionId)`, `updateSessionActivity(sessionId)`.

---

#### `ChatStore`

**Owns:** The conversation messages for the active session (paginated), the streaming state (is content currently streaming, what is the streaming buffer), the input area state (current input text, attached files, submission state), and the conversation scroll position.

**State shape:** `{ messages: Message[], streamingMessage: StreamingMessage | null, inputText: string, attachments: File[], isSubmitting: boolean, hasMore: boolean, scrollPosition: 'bottom' | 'scrolled-up' }`

**Actions:** `addUserMessage(content, attachments)`, `startStreaming(messageId)`, `appendStreamChunk(chunk)`, `finalizeStreaming()`, `loadMoreHistory()`, `setInputText(text)`, `addAttachment(file)`, `removeAttachment(fileId)`, `clearInput()`.

---

#### `EngagementStore`

**Owns:** The active engagement's current lifecycle state, the pipeline execution status (which stage is running, which are complete, which have failed), and the engagement metadata.

**State shape:** `{ engagementId: string | null, lifecycleState: EngagementLifecycleState | null, pipelineStatus: PipelineStatus | null, isAwaitingReview: boolean, isCompleted: boolean, isFailed: boolean, version: number }`

**Actions:** `setEngagement(engagement)`, `updateLifecycleState(newState)`, `updatePipelineStage(stageId, status, output)`, `setAwaitingReview()`, `setCompleted()`, `setFailed(error)`, `clearEngagement()`.

---

#### `WorkspaceStore`

**Owns:** The workspace panel's display state — which tab is active, which sections have content, which sections are loading, and the workspace content for each section (populated progressively by streaming events).

**State shape:** `{ activeTab: WorkspaceTab, sections: { requirements: SectionState, architecture: SectionState, validation: SectionState, review: SectionState, outputs: SectionState, ledger: SectionState }, panelWidth: number, isCollapsed: boolean }`

Where `SectionState = { status: 'empty' | 'loading' | 'partial' | 'complete' | 'error', content: SectionContent | null, lastUpdated: Timestamp | null, reviewedByUser: boolean }`

**Actions:** `setActiveTab(tab)`, `updateSection(tab, content, status)`, `setRequirementsContent(content)`, `setArchitectureContent(content)`, `appendValidationFinding(finding)`, `setReviewContent(proposal)`, `setOutputsContent(bundle)`, `markSectionReviewed(tab)`, `setLoading(tab)`, `setError(tab, error)`, `resetWorkspace()`, `setPanelWidth(width)`.

---

#### `StreamingStore`

**Owns:** The state of the streaming connection and in-flight streaming events.

**State shape:** `{ connectionStatus: 'connected' | 'connecting' | 'disconnected' | 'error', activeStreamId: string | null, pendingEvents: StreamEvent[], lastEventId: string | null }`

**Actions:** `setConnected()`, `setDisconnected()`, `setError(error)`, `setActiveStream(streamId)`, `queueEvent(event)`, `processEvent(eventId)`, `setLastEventId(eventId)`.

---

#### `NotificationStore`

**Owns:** Active toast notifications and notification history.

**State shape:** `{ toasts: Toast[], history: NotificationRecord[], unreadCount: number }`

**Actions:** `showToast(notification)`, `dismissToast(id)`, `addToHistory(record)`, `markAllRead()`, `clearHistory()`.

---

### 7.3 State Persistence Strategy

| State | Persistence Strategy | Duration |
|-------|---------------------|---------|
| Platform auth token reference | Secure cookie (HttpOnly preferred) | Until explicit logout or expiry |
| Active session ID | `sessionStorage` | Until browser tab close |
| Panel width preferences | `localStorage` | Permanent (until cleared) |
| Theme preference | `localStorage` | Permanent |
| Conversation history | Server-authoritative, client cache | Session lifetime |
| Workspace sections | Server-authoritative, reconstructed on restore | Session lifetime |
| In-flight streaming buffer | In-memory only | Until stream completes |
| Input area text (draft) | `sessionStorage` | Until browser tab close |

### 7.4 Streaming State Management

Streaming is managed as a distinct concern from persistent state. The `StreamingService` receives events from the backend and dispatches them to stores through a typed event dispatcher. The sequence:

```
Backend emits streaming event
    ↓
StreamingService receives on WebSocket/SSE connection
    ↓
EventDispatcher routes by event type:
    ├── AgentStageProgress → EngagementStore.updatePipelineStage()
    ├── WorkspaceSectionUpdate → WorkspaceStore.updateSection()
    ├── ChatMessageChunk → ChatStore.appendStreamChunk()
    ├── ReviewGateReady → EngagementStore.setAwaitingReview() + WorkspaceStore.setActiveTab('review')
    └── PipelineComplete → EngagementStore.setCompleted()
```

On reconnection, the StreamingService sends the `lastEventId` to the backend, which replays missed events. The stores process replay events idempotently — a section update with the same content as the current state is a no-op.

---

## 8. Chat Experience

### 8.1 Interaction Model

The Chat Panel is the primary interaction surface. Its design follows ChatGPT-style conventions — which architects familiar with modern AI interfaces will recognize — while extending them with ArchitectIQ-specific patterns for pipeline progress, workspace updates, and review gate signals.

**Conversational flow:** Messages alternate between user (right-aligned, distinct background) and assistant (left-aligned, platform brand treatment). The conversation is vertical and time-ordered, with the most recent message at the bottom. The input area is pinned to the bottom of the panel.

**Message types in the chat thread:**

| Message Type | When Shown | Visual Treatment |
|-------------|------------|-----------------|
| User message | After submission | Right-aligned, user avatar, text bubble |
| Pipeline initiation signal | After user message | System line: "Starting architecture analysis…" |
| Stage progress card | As each pipeline stage begins | Compact card with stage name and spinner → checkmark on completion |
| Assistant streaming message | During pipeline execution | Left-aligned, platform avatar, text renders progressively |
| Workspace update notice | When a workspace section updates | Inline system notice: "Requirements extracted → Workspace updated" |
| Review gate notice | When review is ready | Prominent card with "Review ready" call-to-action linking to workspace Review tab |
| Refinement confirmation | After refinement is submitted | System line: "Refinement submitted. Re-running affected analysis…" |
| Approval confirmation | After architect approves | System line: "Architecture approved. Generating outputs…" |
| Completion notice | After outputs are ready | Compact card with output summary and link to Outputs tab |
| Error notice | On pipeline failure | Error card with failure stage, reason, and retry action |

### 8.2 Streaming Message Rendering

The streaming assistant message renders in real time as content arrives. Rendering strategy:

- **Plain text:** Renders immediately as received, character by character with a blinking cursor at the current position.
- **Markdown:** Buffered by paragraph — a paragraph renders completely before the next begins, preventing mid-paragraph re-renders.
- **Structured data (JSON objects):** Buffered completely before rendering — JSON is not rendered partially.
- **Code blocks:** Rendered complete (buffered) — partial code blocks are not syntax-highlighted mid-stream.

The streaming cursor (blinking pipe character) indicates active streaming. Its disappearance signals stream completion. A final checkmark badge confirms successful completion.

### 8.3 Pipeline Progress Visualization

Pipeline execution progress is visualized directly in the chat thread as a compact, expandable progress card. The card shows:

- **Pipeline stage track:** A horizontal sequence of stage indicators (circles with stage names below). Each circle transitions from empty → spinner → checkmark (success) or X (failure) as the stage progresses.
- **Current stage detail:** The actively executing stage shows the specific step within the stage (e.g., "Architecture Design: Generating candidate 2 of 3").
- **Elapsed time:** A running timer shows how long the pipeline has been executing.
- **Estimated completion:** A progress percentage derived from stage completion (updated as each stage completes).

The progress card is compact by default. Clicking it expands to show per-stage timing detail and agent output summaries for completed stages.

### 8.4 Input Area

The input area at the bottom of the Chat Panel has the following components:

- **Text area:** Auto-resizing from single line up to a configured maximum height. Beyond the maximum, it scrolls internally. Placeholder text guides the architect: "Describe your architecture requirement…"
- **Attachment button:** Opens a file picker for document upload (PDF, DOCX, TXT). Accepted file types are validated client-side before upload.
- **Attachment previews:** Uploaded files appear as chips above the text area with a remove button.
- **Submit button:** Active when text is not empty or an attachment is present. Disabled during pipeline execution to prevent simultaneous submissions.
- **Submission shortcuts:** Enter submits (with Shift+Enter for newline). Cmd+Enter as an alternative on Mac.

**Input disabled state:** The input area is disabled with a clear visual explanation while a pipeline is actively executing. The architect can still scroll the chat history and navigate the workspace. The input re-enables when the pipeline reaches PENDING_HUMAN_REVIEW or COMPLETED or FAILED state.

### 8.5 Session Restore in Chat

On session restoration (loading a prior session), the chat panel:
1. Renders the conversation history from the bottom (most recent messages visible first).
2. Displays a "Load earlier messages" trigger at the top of the visible history.
3. If the session's active engagement is in PENDING_HUMAN_REVIEW, the review gate notice is rendered at the bottom of the chat thread (in its original chronological position) and the workspace Review tab is highlighted.
4. If the session is COMPLETED, the completion notice is rendered at the bottom.

The architect resumes from exactly the state they left — they do not need to re-read the entire conversation from the beginning.

---

## 9. Workspace Architecture

### 9.1 Workspace Philosophy

The Workspace Panel is the artifact surface of the platform. Where the Chat Panel shows process (what is happening), the Workspace Panel shows output (what has been produced). The two panels are complementary: the chat provides narrative context for the workspace content.

The workspace is organized as a tabbed surface where each tab corresponds to a pipeline stage output or a governance action. Tabs are progressive — they become active (content-bearing) as the pipeline advances. An empty tab indicates that its pipeline stage has not yet completed.

### 9.2 Workspace Tab System

**Tab states:**

| State | Visual Treatment | Meaning |
|-------|-----------------|---------|
| Inactive | Grayed label, disabled | Pipeline stage has not started |
| Loading | Label + spinner | Pipeline stage is actively executing |
| Partial | Label + progress ring | Stage executing, some content available |
| Ready | Label + green dot | Stage complete, content available |
| Attention | Label + orange dot | Requires architect action (review gate) |
| Error | Label + red icon | Stage failed, content unavailable |

**Tab navigation rules:**
- Tabs are reachable by keyboard (Tab key to focus tab bar, arrow keys between tabs).
- The active tab state persists in `WorkspaceStore` — switching between chat and workspace does not reset the active tab.
- When a stage completes, the corresponding tab transitions to Ready state but does not auto-activate (except the Review tab when the gate opens, which auto-activates and highlights in the chat thread).
- Switching to a tab does not trigger data fetching — all content is delivered through streaming and stored in the `WorkspaceStore`.

### 9.3 Requirements Tab Content

The Requirements tab renders the Requirement Intelligence Agent's structured output:

- **Functional requirements section:** Numbered list with requirement type, description, and source attribution (which part of the architect's input this was extracted from)
- **Non-functional requirements section:** Organized by NFR category (availability, performance, security, compliance, data residency, retention)
- **Ambiguity flags panel:** Each ambiguity is a card with: the ambiguous statement, the agent's interpretation, the confidence score, and an inline clarification input (architect can correct misinterpretations in the chat)
- **Constraint summary:** Technical and organizational constraints extracted
- **Confidence overview:** Overall extraction confidence score with per-section breakdown

### 9.4 Architecture Tab Content

The Architecture tab renders the Design Stage output — candidate architectures with comparison capability:

- **Candidate card:** Each candidate architecture renders as an expandable card with: pattern name, pattern classification (e.g., Medallion, Lambda, Kappa, Data Mesh), technology stack summary, and a one-paragraph rationale.
- **Trade-off table:** A comparison matrix showing each candidate against shared evaluation criteria (complexity, cost tier, scalability, operational burden, time to implement).
- **Diagram preview:** A compact architecture diagram (Mermaid or Graphviz rendered) within the card, with a full-screen expand option handled by the `diagram-viewer` module.
- **Selected candidate highlight:** The architect can mark a preferred candidate — this preference is passed as context to the refinement flow if they request changes.

### 9.5 Validation Tab Content

The Validation tab renders the four Validation Stage agents' outputs in a consolidated view:

- **Security findings panel:** Collapsible list of threat model findings. Each finding has: severity badge (Critical/High/Medium/Low), finding description, affected component, control recommendation. Blocking findings are visually emphasized.
- **Cost model panel:** TCO breakdown table with cost per architecture component, total monthly estimate, optimization opportunities as a ranked list.
- **Compliance checklist panel:** Regulatory framework selection (only applicable frameworks shown), control checklist with pass/fail/needs-review status per control, coverage percentage.
- **Risk register panel:** Prioritized risk table with: risk category, probability (High/Medium/Low), impact (High/Medium/Low), risk score, suggested mitigation, and resolution status.
- **Validation summary banner:** A top-level summary showing the count of blocking and advisory findings across all four agents.

### 9.6 Review Tab — Review Gate

Described fully in Section 4.7 (`review` module). The key workspace-level consideration:

- The Review tab is the only tab that requires architect interaction — all other tabs are read-only display.
- The Review tab is scroll-locked to the top when it first opens — the architect reads from the top of the review package, not from the bottom.
- The decision controls (Approve, Refine, Reject) are anchored to the bottom of the Review tab, always visible regardless of scroll position.
- An "All sections reviewed" indicator shows how many workspace tabs the architect has visited since the review gate opened — not a hard gate, but a soft prompt to ensure complete review.

### 9.7 Outputs Tab Content

Described fully in Section 4.8 (`output-viewer` module). The workspace-level organization:

- Outputs are organized by category: Design Documents (HLD, LLD), Summary Documents (Executive Summary, Assumptions Log), Risk Documents (Risk Register), Diagrams (Architecture Overview, Data Flow), Machine Readable (JSON Architecture State).
- Each output is represented as a file card with: format badge, file size, generation timestamp, template version used.
- The file card has two actions: Preview (renders inline in the workspace) and Download.
- Multiple output versions are accessible through the version selector in the workspace header.

### 9.8 Workspace Version History

For engagements with multiple approved architecture versions (created through the refine → approve cycle):

- A version selector in the workspace panel header allows the architect to navigate between versions.
- All tabs reflect the state of the selected version.
- Switching versions does not make a new API call if the version's content is already in the `WorkspaceStore`.
- A "Latest" indicator marks the current approved version. Prior versions are labeled with their version number and approval date.

---

## 10. UI Layout Strategy

### 10.1 Application Shell

The application shell is the persistent structural container that surrounds all page content. It contains:

- **Top bar (minimal):** Application logo/wordmark, active session name (editable inline), connection status indicator (streaming connected/disconnected), user avatar with profile menu (profile, settings, logout).
- **Main content area:** Hosts the active page's content (the three-panel workspace for the workspace route, the history table for the history route, the settings form for the settings route).
- **Global notification zone:** Toast notifications appear in the top-right corner, stacked from the top.

The top bar is intentionally minimal — it does not contain navigation controls (navigation is through the Sessions Panel and the route-level pages). The workspace is the application, not a page within a larger navigation structure.

### 10.2 Three-Panel Layout

The three-panel layout is the canonical workspace view. It occupies the full viewport below the top bar.

**Panel dimensions and behavior:**

| Panel | Default Width | Minimum Width | Maximum Width | Collapsible |
|-------|-------------|--------------|--------------|-------------|
| Sessions (Left) | 260px | 200px | 360px | Yes — collapses to 48px icon strip |
| Chat (Center) | Remaining space (flex-grow) | 480px | — | No |
| Workspace (Right) | 480px | 360px | 720px | Yes — collapses to 48px icon strip |

**Panel resize:** The left and right panels are resizable by dragging their border. Panel widths are persisted in `localStorage` and restored on next visit. The center chat panel always fills the remaining space between the two side panels.

**Panel independence:** Each panel scrolls independently. Scrolling the session list does not affect the chat position. Scrolling the workspace does not affect the chat position.

### 10.3 Responsive Behavior

The three-panel layout is designed for professional desktop workspaces (1280px+). On narrower viewports:

| Viewport | Layout Behavior |
|----------|----------------|
| ≥ 1280px | Full three-panel layout |
| 1024px–1279px | Sessions panel collapsed to icon strip by default |
| 768px–1023px | Single-panel mode: Chat panel fullscreen; sessions and workspace accessible as overlays (drawers) |
| < 768px | Mobile mode: Not a primary use case. Chat panel fullscreen with bottom-sheet access to workspace |

On collapse to icon strip: The left panel collapses to a narrow strip showing session avatars/initials. Hovering expands a compact session selector. The workspace panel collapses to a strip of workspace tab icons with an expand-on-click behavior.

### 10.4 Panel Responsibilities (Layout-Level)

- The Sessions Panel is responsible for the left panel's visual treatment and collapse state.
- The Chat Panel owns the center panel's full height and scroll behavior.
- The Workspace Panel owns the right panel's tab system and content rendering.
- The three-panel layout container owns only the spatial arrangement — it does not know about sessions, chat, or workspace content.

---

## 11. Frontend Service Layer

### 11.1 Service Layer Philosophy

The service layer is the translation layer between the frontend's domain model and the backend's HTTP API. Services are pure functions — they receive inputs, communicate with the backend, and return typed results. They have no side effects on application state.

Stores invoke services. Services never invoke stores. Services never access the DOM, never manipulate application state, and never make routing decisions.

### 11.2 `ApiClient` — Base HTTP Client

The `ApiClient` is the foundation of all HTTP communication. It provides:

- **Authentication injection:** Attaches the current platform token to every request's Authorization header. If the token is expired, it attempts a refresh before the request. If the refresh fails, it dispatches a session expiry event to the `AuthStore`.
- **Correlation ID injection:** Generates and attaches a unique correlation ID to every request's headers for distributed tracing.
- **Request timeout:** All requests have a configured default timeout. Long-running requests (output retrieval, file download) have an extended timeout.
- **Response normalization:** All responses are parsed into a consistent envelope `{ data, error, status }`. Service functions receive the normalized envelope, not raw Response objects.
- **Error classification:** HTTP error responses are classified into typed frontend error objects by status code (400 → ValidationError, 401 → AuthError, 403 → ForbiddenError, 404 → NotFoundError, 429 → RateLimitError, 5xx → ServiceError).

### 11.3 Service Definitions

#### `AuthService`

Responsibilities: OAuth flow initiation (returns the GitHub authorization URL), OAuth callback completion (sends the code to the backend, receives and stores the platform token), token refresh, logout (revokes the token on the backend and clears the client-side reference).

---

#### `SessionService`

Responsibilities: Load the session list for the Sessions Panel (paginated), load a specific session's full context for workspace restoration, create a new session, rename a session, delete a session, update the session's last-active timestamp.

---

#### `ChatService`

Responsibilities: Submit a new user message with optional attachments (initiates a new pipeline execution), load conversation history (paginated, older messages), load a specific message's full content.

---

#### `EngagementService`

Responsibilities: Get the current engagement state for an active session, submit a review decision (approve, refine, reject) with the decision payload, submit a direct component override, get the engagement's version history.

---

#### `OutputService`

Responsibilities: Get the output bundle manifest for a completed engagement, get a specific output file's content for preview, trigger output regeneration for a new approved version.

---

#### `KnowledgeService` (Read-only)

Responsibilities: Get the details of a knowledge base citation (for the citation detail panel in the artifacts module). This is the only knowledge service the frontend consumes — it is read-only and limited to citation lookup.

---

#### `LedgerService` (Read-only)

Responsibilities: Get the Decision Ledger entries for a specific engagement (paginated), get the details of a specific ledger entry for the expanded view.

---

### 11.4 `StreamingService`

The `StreamingService` is distinct from the other services — it manages a persistent connection rather than discrete requests.

**Responsibilities:**
- Establish and maintain the WebSocket or SSE connection to the backend's streaming endpoint
- Authenticate the streaming connection (attach the session token on connection initiation)
- Send the `lastEventId` on connection or reconnection to receive missed events
- Parse incoming events into typed `StreamEvent` objects
- Dispatch events to the `EventDispatcher` which routes them to the appropriate stores
- Handle connection drops with exponential-backoff reconnection (max 5 attempts before switching to a "connection lost" UI state)
- Expose connection status to the `StreamingStore`

**Event types received:**

| Event Type | Dispatched To | Effect |
|------------|--------------|--------|
| `agent.stage.started` | `EngagementStore`, `ChatStore` | Stage progress card update in chat |
| `agent.stage.completed` | `EngagementStore`, `WorkspaceStore` | Stage marked complete; workspace section updated |
| `workspace.section.update` | `WorkspaceStore` | Section content updated progressively |
| `chat.message.chunk` | `ChatStore` | Streaming message buffer appended |
| `chat.message.complete` | `ChatStore` | Streaming finalized |
| `engagement.review.ready` | `EngagementStore`, `WorkspaceStore` | Review gate open; workspace auto-navigates to Review tab |
| `engagement.completed` | `EngagementStore` | Engagement COMPLETED; outputs available |
| `engagement.failed` | `EngagementStore`, `ChatStore` | Pipeline failure notification in chat |

### 11.5 Retry Strategy

| Scenario | Retry Behavior |
|----------|---------------|
| HTTP 429 (rate limited) | Wait for `Retry-After` header duration, then retry once |
| HTTP 5xx (server error) | 3 retries with exponential backoff (1s, 2s, 4s) |
| Network timeout | 2 retries with the same timeout value |
| Streaming connection drop | Reconnect with last-event-ID, up to 5 attempts with exponential backoff |
| Auth token expired | Refresh token, then retry the original request once |

---

## 12. Performance Strategy

### 12.1 Code Splitting

The application is code-split at the route level — each route is a separate bundle loaded only when the route is visited. The main bundle contains only the application shell, the auth module, and the routing configuration. Feature modules are loaded lazily on first navigation to their route.

Within the workspace, the diagram rendering library (Mermaid, Graphviz) is loaded lazily on first diagram display — these are large libraries that should not be in the initial bundle.

### 12.2 Lazy Loading

| Resource | Lazy Load Trigger |
|----------|------------------|
| History page module | First navigation to `/history` |
| Settings page module | First navigation to `/settings` |
| Mermaid library | First diagram rendered in workspace |
| Graphviz library | First Graphviz diagram rendered |
| PDF viewer | First PDF output displayed |
| Markdown renderer | First Markdown content displayed |

### 12.3 Memoization Strategy

**Component memoization:** Presentational components that receive complex object props are wrapped in React's memo boundary. The memo comparison is shallow — complex objects must be stable references for memoization to be effective (stores must return stable references for unchanged data).

**Hook memoization:** Computed values derived from store state within hooks use stabilized selectors to prevent unnecessary re-renders when unrelated store state changes.

**Conversation history virtualization:** The chat message thread uses virtual scrolling for long conversation histories (typically hundreds of messages across multiple sessions). Only the messages within the visible viewport are rendered to the DOM. Scrolling loads more messages lazily.

### 12.4 Caching Strategy

**Service response caching:** Infrequently changing data (session list, output bundle manifests, ledger entries for completed engagements) is cached client-side with explicit TTLs. Cache invalidation is triggered by specific user actions (new message sent, review decision submitted) or by streaming events that signal state changes.

**Workspace section caching:** Once a workspace section is fully loaded into the `WorkspaceStore`, it is not re-fetched when the architect navigates between tabs. The content is stable within a session. Re-fetching is triggered only on explicit refresh or on streaming events.

**Image and diagram caching:** Rendered diagram images (SVG/PNG) are cached using browser caching headers. The cache key includes the architecture version — a new architecture version produces a new diagram cache entry.

---

## 13. Accessibility

### 13.1 Foundational Requirements

All components in the frontend must meet WCAG 2.1 AA as the minimum standard. The following are not optional enhancements — they are architectural requirements:

- **Keyboard navigability:** All interactive elements are reachable and operable by keyboard. Focus order follows the logical reading order. Modal dialogs trap focus. Drawers and overlays manage focus correctly on open and close.
- **ARIA semantics:** All interactive components have correct ARIA roles, states, and properties. Dynamic content changes (streaming message updates, workspace section updates) use `aria-live` regions with appropriate politeness levels.
- **Color independence:** No information is conveyed by color alone. Status indicators (pipeline stage states, validation finding severities, engagement statuses) combine color with icon and text labels.
- **Screen reader compatibility:** All functional UI elements have accessible names. Images and icons that convey meaning have alt text or ARIA labels. Decorative icons are hidden from assistive technology.

### 13.2 Streaming Content and Live Regions

Streaming content poses an accessibility challenge — progressively revealed content must be announced to screen readers without overwhelming them.

**Strategy:**
- The streaming message area is an `aria-live="polite"` region. Screen readers announce content when the user is not interacting.
- Stage progress updates are announced as discrete sentences, not as continuous character streams.
- Workspace section updates are announced with a brief summary (e.g., "Requirements section updated") via a visually hidden live region in the application shell.
- The review gate opening is announced via an `aria-live="assertive"` region (interrupting) because it requires immediate architect attention.

### 13.3 Focus Management

- On session load, focus is set to the chat input area.
- On modal open, focus moves to the modal's first focusable element.
- On modal close, focus returns to the element that triggered the modal.
- On tab switch within the workspace panel, focus moves to the new tab's content heading.
- On streaming completion, focus remains on the element the user last interacted with — streaming does not steal focus.

### 13.4 Motion and Animation

All motion in the application respects the `prefers-reduced-motion` media query. When reduced motion is preferred:
- Transitions are replaced with instant state changes
- Spinning indicators are replaced with static indicators
- Auto-scrolling behavior is disabled

---

## 14. Theme Architecture

### 14.1 Design Token System

The frontend's visual language is defined entirely through design tokens — named values for every visual property. No component contains hardcoded color values, spacing values, or font sizes. All visual properties are referenced by token name.

**Token categories:**

| Category | Examples |
|----------|---------|
| **Color — Brand** | `--color-brand-primary`, `--color-brand-secondary` |
| **Color — Semantic** | `--color-success`, `--color-warning`, `--color-error`, `--color-info` |
| **Color — Surface** | `--color-surface-base`, `--color-surface-elevated`, `--color-surface-overlay` |
| **Color — Text** | `--color-text-primary`, `--color-text-secondary`, `--color-text-disabled`, `--color-text-inverse` |
| **Color — Border** | `--color-border-default`, `--color-border-strong`, `--color-border-focus` |
| **Spacing** | `--space-1` (4px) through `--space-16` (64px) on a 4px base grid |
| **Typography — Size** | `--text-xs` through `--text-3xl` |
| **Typography — Weight** | `--font-normal`, `--font-medium`, `--font-semibold`, `--font-bold` |
| **Typography — Family** | `--font-sans` (UI font), `--font-mono` (code font) |
| **Border Radius** | `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-full` |
| **Elevation (Shadow)** | `--shadow-sm`, `--shadow-md`, `--shadow-lg` |
| **Motion — Duration** | `--duration-fast` (100ms), `--duration-normal` (200ms), `--duration-slow` (400ms) |
| **Motion — Easing** | `--ease-in`, `--ease-out`, `--ease-in-out` |
| **Z-Index** | `--z-base`, `--z-dropdown`, `--z-modal`, `--z-toast` |

### 14.2 Dark and Light Themes

The application supports both dark and light themes, with system preference as the default. Theme is stored in `localStorage` and applied through a class on the document root that switches the active token set.

**Theme token strategy:** Semantic color tokens (e.g., `--color-surface-base`) have different resolved values in the light theme and the dark theme. All components reference semantic tokens — never raw color values. Switching the theme updates the semantic token values, and all components update automatically.

**Default theme for ArchitectIQ:** The default design aesthetic reflects a professional, focused workspace — not a consumer product. The preferred default is dark mode (consistent with professional developer and architect tools: VS Code, GitHub, Linear, Vercel). Light mode is a first-class supported variant, not an afterthought.

### 14.3 Typography

The application uses two typeface roles:

**UI Typeface (sans-serif):** Used for all interface labels, conversation messages, workspace content, and navigation. Selected for readability at small sizes and professional neutrality.

**Monospace Typeface:** Used for code blocks, JSON output, architecture source (Mermaid/DOT), and any technical content that benefits from character-width consistency.

**Type scale:** The scale follows a minor-third progression (1.25 ratio) anchored at a 14px base for interface labels and 16px for reading-length content (workspace documents, conversation history).

### 14.4 Icon System

A single icon library is used throughout the application. Icons are rendered as SVG — no icon fonts (icon fonts create accessibility and rendering quality issues). All icons are sized proportionally to the surrounding text using em units. Custom icons specific to ArchitectIQ (agent stage icons, architecture pattern icons, engagement state icons) extend the base icon library without replacing it.

---

## 15. Error Experience

### 15.1 Error Philosophy

Errors are normal. The frontend is designed to handle them visibly, specifically, and gracefully. An error state is not a failure of the application — it is information about the current system state, presented in a way that tells the architect what happened and what they can do next.

Every error state has three elements: what happened (in plain language), why it happened (if knowable), and what to do next (a concrete action or a reassurance).

### 15.2 Error Classification and Handling

| Error Type | Scope | Display Treatment | Recovery Action |
|-----------|-------|-----------------|-----------------|
| Network connectivity loss | Global | Persistent banner at top of application: "Connection lost. Reconnecting…" | Auto-reconnect with status update |
| Streaming connection lost | Chat/Workspace | Inline notice in chat thread and workspace header: "Live updates paused. Reconnecting…" | Auto-reconnect; replay missed events on reconnect |
| Authentication expired | Global | Modal overlay: "Your session has expired. Please sign in again." | Redirect to login, preserving session context for post-login restore |
| Pipeline stage failure | Engagement | Chat error card (stage name, failure reason, retry option) + affected workspace tabs show error state | Retry the engagement from the failed stage |
| LLM provider unavailable | Engagement | Specific message: "AI analysis temporarily unavailable. Your work is saved. Please try again in a moment." | Retry trigger available in the chat error card |
| Output generation failure | Workspace Outputs tab | Outputs tab error state: "Some outputs could not be generated. [Retry]" | Retry output generation independently of the pipeline |
| Feature load failure | Feature module | Module-level error boundary with: "This section encountered an error. [Reload section]" | Reload just the failed module, not the whole application |
| API validation error | Form/Input | Inline validation messages adjacent to the invalid input | Correct and resubmit |
| Not Found (404) | Route | Friendly not-found page with navigation back to workspace | Navigate back |

### 15.3 Global Error Boundary

The React application root is wrapped in a global error boundary. If an unhandled rendering error occurs (rare but possible), the error boundary catches it and renders a full-page error state with:

- A clear indication that something unexpected happened
- An option to refresh the application
- The correlation ID of the last known request (for support reference)
- Preservation of the session — the session is not lost due to a rendering error

The error is also emitted to the observability layer through a frontend error tracking integration.

### 15.4 Empty States

Empty states are distinct from error states. An empty state indicates that content is not yet available — not that something went wrong.

Every workspace tab has a designed empty state that explains: what this tab will show (once the pipeline reaches the relevant stage), the current pipeline status (how far along we are), and what the architect should do next (if anything — often just "wait").

---

## 16. Frontend Extension Strategy

### 16.1 Adding a New Module

A new feature module is added without touching existing modules:

1. Create the module directory under `src/frontend/src/components/{module-name}/`.
2. Create the module's container components, hooks, and types within the directory.
3. Create the module's store (if it requires global state) in `src/frontend/src/stores/`.
4. Create the module's service (if it requires API communication) in `src/frontend/src/services/`.
5. Register the module's route in the `AppRouter` (if it is a new page).
6. If the module adds a new workspace tab, register it in the `WorkspacePanel`'s tab configuration.

**No existing modules are modified** for a new module addition (except the router for new routes, and the workspace panel tab configuration for new workspace tabs — both are additive changes, not modifications).

### 16.2 Adding a New Workspace Tab

New workspace tabs are registered in the `WorkspaceStore`'s tab configuration — a typed list of tab specifications that includes the tab ID, label, icon, and the module component that renders its content. The `WorkspacePanel` renders tabs dynamically from this configuration.

### 16.3 Adding a New Output Format

New output formats appear in the `output-viewer` module's format-to-renderer map. Adding a new format (e.g., PPTX preview) requires: adding the renderer component to the `output-viewer` module, adding the format type to the output type definitions, and registering the renderer in the format map. No other modules change.

### 16.4 Adding a New Notification Type

New notification types are additions to the `NotificationStore`'s event type enum and the `notifications` module's rendering map. New event types from the streaming service are mapped to notification types in the `EventDispatcher`. All existing notification rendering is unaffected.

### 16.5 Feature Flags in the Frontend

Features that are in progressive rollout are controlled by feature flags loaded from the backend's configuration API at startup. New feature flags are added to the `FeatureFlagService` in the Configuration Layer. Feature flag checks in components use a `useFeatureFlag(flagName)` hook. Removing a feature flag once a feature is fully rolled out requires deleting the flag and the hook call — no structural changes.

---

## 17. Frontend Validation Checklist

Use this checklist to validate any new module, component, or feature addition against the architecture.

### Module Design

- [ ] The module has exactly one stated responsibility.
- [ ] The module does not import from other feature modules' internal components.
- [ ] All inter-module communication goes through stores, not through direct component import.
- [ ] The module's public interface (exported components, hooks, types) is minimal — only what other modules need.

### Component Design

- [ ] Every component is classified as Container, Presentational, Layout, or Utility.
- [ ] Presentational components receive all data through props — no store access.
- [ ] Container components contain no visual styling — they compose presentational components.
- [ ] No prop drilling beyond two levels — if needed, use a store.
- [ ] Components do not call services directly — they use hooks that delegate to services.

### State Management

- [ ] Every piece of state has a clearly identified owning store.
- [ ] No two stores own the same data.
- [ ] Stores do not import from other stores.
- [ ] Streaming state is managed through the `StreamingStore` and dispatched via `EventDispatcher`.
- [ ] Persistent state uses the correct storage mechanism (localStorage, sessionStorage, or server-authoritative).

### Service Layer

- [ ] All HTTP calls originate from service files — never from components or stores directly.
- [ ] Services return typed result objects — never raw `Response` objects.
- [ ] Services do not access or modify stores.
- [ ] Error responses are normalized to typed frontend error objects before leaving the service.

### Accessibility

- [ ] All interactive elements are keyboard navigable and have visible focus indicators.
- [ ] Dynamic content changes use appropriate `aria-live` regions.
- [ ] Color is not the sole conveyor of information.
- [ ] New icons used to convey meaning have ARIA labels.
- [ ] New modal dialogs trap focus and return focus on close.

### Performance

- [ ] New libraries over 50KB are lazy-loaded, not added to the main bundle.
- [ ] Components that render lists of 50+ items use virtualization.
- [ ] Presentational components that receive complex object props are memoized.
- [ ] Streaming rendering uses the correct buffering strategy for the content type.

### Theme

- [ ] No hardcoded color values, spacing values, or font sizes — all design tokens.
- [ ] Component renders correctly in both dark and light themes.
- [ ] Animation respects `prefers-reduced-motion`.

---

## 18. Frontend Freeze Rules

The following rules are immutable. No implementation decision, design preference, or scope pressure may violate them. Changes require an ARB-approved ADR.

| # | Frontend Freeze Rule |
|---|---------------------|
| **FFR-01** | The three-panel layout (Sessions | Chat | Workspace) is the canonical workspace interface. No feature may replace this layout or reorder its panels without an ARB-approved ADR. Adding panels or collapsing existing panels is permitted; replacing the model is not. |
| **FFR-02** | All communication with the backend passes through the Service Layer. Components and stores never issue direct HTTP calls or WebSocket messages. |
| **FFR-03** | Feature modules do not import from other feature modules' internal implementations. Inter-module data flow uses stores exclusively. |
| **FFR-04** | Presentational components do not access stores, issue API calls, or produce side effects beyond rendering. They receive all data through props. |
| **FFR-05** | The Approve action in the Review Gate is never triggered programmatically. It requires an explicit, deliberate user interaction (click or keyboard activation) with a confirmation step. No timer, no auto-advance, no "skip review" path. |
| **FFR-06** | Session restoration is unconditional. On login, the application always attempts to restore the most recent session. There is no "fresh start" default. A new session is an explicit architect choice, not the default behavior. |
| **FFR-07** | No design token value is hardcoded in any component. All visual properties (color, spacing, typography, shadow, radius) are resolved through design tokens from the Theme Layer. |
| **FFR-08** | The streaming connection is managed exclusively by the `StreamingService`. No component, store, or service other than `StreamingService` opens, closes, or reads from the streaming connection. |
| **FFR-09** | The chat input area is disabled (with visible explanation) while a pipeline is actively executing. The architect cannot submit a new message during active pipeline execution. There is no override for this constraint. |
| **FFR-10** | All WCAG 2.1 AA accessibility requirements are production requirements, not enhancement requests. A component that fails keyboard navigation, lacks appropriate ARIA attributes, or conveys information through color alone is a defect, not a design preference. |

---

> **End of FRONTEND_MODULE_ARCHITECTURE.md**  
> **Version 1.0.0 — Foundation Release**  
> **Parent Documents:** ARCHITECTURE_VISION.md v1.0.0 · REPOSITORY_MASTER_STRUCTURE.md v1.0.0 · SYSTEM_ARCHITECTURE.md v1.0.0 · BACKEND_MODULE_ARCHITECTURE.md v1.0.0  
> **Classification:** Frontend Architecture — Source of Truth  
> **Next Document:** AGENT_ARCHITECTURE.md
