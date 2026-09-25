# BobAccess: The Voice-First Enterprise AI Accessibility & Technical Knowledge Suite

> **Official Project Blueprint & System Architecture**  
> **Event:** IBM Bob 2.0 Hackathon (LabLab.ai | Remote 48 Hours | September 25–27, 2026)  
> **Prize Pool:** $12,000  
> **Development Setup:** Pair Programming with Antigravity (Lead Architect & Co-pilot) + IBM Bob Standalone IDE (Agentic Engine & Enterprise Tier)

---

## 1. Executive Summary

**BobAccess** is an enterprise-grade, multimodal assistive AI platform designed for visually impaired engineers, analysts, executives, and students. It bridges the critical accessibility gap in corporate knowledge management by transforming complex technical documents, architecture diagrams, compliance audits, and codebases into an interactive, voice-driven, audio-first experience.

Unlike conventional screen readers that stumble over complex diagrams, tables, and nested technical syntax, **BobAccess** harnesses the agentic intelligence of **IBM Bob**, **IBM watsonx.ai (Granite 3.0)**, **watsonx Orchestrate**, and **IBM Watson Speech Services** to synthesize, contextualize, and narrate complex enterprise knowledge conversationally and hands-free.

---

## 2. Problem Statement & Market Reality

### The Accessibility Barrier in Modern Enterprises
1. **Screen Readers Fail on Visual & Technical Data:** Tools like JAWS, NVDA, and VoiceOver read syntax literally (`"curly brace, colon, indentation level 4..."`), making technical codebases, schemas, and complex tables tedious and cognitively exhausting.
2. **The "Black Box" of Diagrams & Flowcharts:** Over 65% of enterprise documentation relies on visual artifacts—cloud architecture diagrams, sequence flows, ERDs, charts, and process diagrams. For visually impaired professionals, these are completely inaccessible black boxes.
3. **Information Overload in Massive Reports:** Navigating 100-page regulatory filings, SOC2 compliance reports, or technical RFCs requires rapid skimming, context-switching, and synthesis—capabilities screen readers cannot provide without AI summarization.
4. **Enterprise Compliance Demands:** Global mandates (European Accessibility Act 2025/2026, ADA Title III, Section 508) require enterprises to provide genuinely accessible tools for internal employees and external users.

---

## 3. Product Vision & Core Value Proposition

| Dimension | Legacy Accessibility (Screen Readers) | BobAccess with IBM Bob & watsonx |
| :--- | :--- | :--- |
| **Document Processing** | Reads raw text top-to-bottom sequentially | Multimodal parsing (Text, Tables, Flowcharts, Code) into structured semantics |
| **Interaction Model** | Keyboard hotkeys reading static text lines | Natural, bi-directional voice conversation & hands-free drilldowns |
| **Complex Diagrams** | Ignored or reads generic alt-text (`"image.png"`) | Conversational visual-to-audio architectural narration |
| **Cognitive Load** | High; user must reconstruct context mentally | Low; provides executive audio summaries with voice-guided deep-dives |
| **Enterprise Integration**| Disconnected desktop software | Seamlessly connected with IBM Cloud, enterprise repos, and watsonx |

---

## 4. Deep IBM Ecosystem Integration

### A. IBM Bob (The Hackathon Star & Agentic Engine)
* **Custom Model Context Protocol (MCP) Server (`bob-a11y-mcp`):**
  We build a custom MCP server connecting IBM Bob to the knowledge base and document processor. Bob acts as an autonomous agent able to search documents, inspect schemas, and formulate multi-step answers.
* **Audio Semantic Representation (ASR) Engine:**
  IBM Bob specializes in repository and structural comprehension. It converts complex code blocks, JSON schemas, SQL queries, and architecture diagrams into natural, conversational verbal explanations rather than raw symbol reading.
* **Autonomous Task Execution (Plan & Code Modes):**
  When a user asks: *"Bob, compare our quarterly cloud spend in Appendix B with our budget in Section 1 and explain the deviation,"* Bob autonomously executes the reasoning plan across multiple document chunks and delivers an audio-ready summary.
* **Enterprise Bob Coins Utilization:**
  The project utilizes the Enterprise tier allocation to power deep agentic reasoning, cross-document indexing, and high-context multi-turn conversational sessions.

### B. IBM watsonx.ai (Granite 3.0 Models)
* **Audio-Optimized RAG Summarization:**
  Powers the semantic retrieval and text generation. Prompts are specifically engineered to produce punchy, conversational, audio-first responses free of markdown tables or formatting that sound unnatural when spoken.
* **Enterprise Governance & Hallucination Guardrails:**
  Ensures that generated compliance, financial, or technical summaries remain strictly grounded in uploaded source documents.

### C. IBM watsonx Orchestrate
* **Workflow Automation & Connector Layer:**
  Orchestrates background tasks: pulling newly published enterprise reports from repositories (GitHub, Box, SharePoint), triggering OCR and vectorization, and dispatching accessible audio alerts to users.

### D. IBM Watson Speech Services (STT & TTS)
* **Watson Speech-to-Text (STT):** High-accuracy, low-latency speech recognition allowing complete hands-free navigation.
* **Watson Text-to-Speech (TTS):** Natural, expressive neural voice synthesis providing clear, fatigue-free audio playback.

---

## 5. System Architecture

```
                      ┌────────────────────────────────────────┐
                      │    Visually Impaired Professional      │
                      │       (Voice Input & Audio Out)        │
                      └──────────────────┬─────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ACCESSIBLE FRONTEND APPLICATION                                 │
│  - WCAG 2.1 AAA Compliant Design (High-Contrast, Pure Monochrome/Amber options)        │
│  - Voice-First Controls & Global Keyboard Shortcuts (Space to talk, Esc to pause)     │
│  - Real-Time Audio Waveform & Sound Effect Feedback Cues                               │
│  - Live Transcript & Audio Player with Variable Speed (1x - 3x)                        │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ WebSocket / REST API
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          FASTAPI BACKEND CORE SERVICE                                  │
│  ├── Voice Controller: Speech-to-Text & Text-to-Speech Streaming                      │
│  ├── Document Processor: PDF Parser, Layout Analyzer, OCR (Tesseract / Vision AI)     │
│  ├── Diagram & Chart Explainer: Visual elements converted to semantic Markdown         │
│  └── Vector Memory Engine: ChromaDB / Milvus + Embeddings                              │
└───────────────────────┬────────────────────────────────────────┬───────────────────────┘
                        │                                        │
                        ▼                                        ▼
┌────────────────────────────────────────┐  ┌────────────────────────────────────────────┐
│      IBM BOB AGENTIC ENGINE            │  │           IBM WATSONX PLATFORM             │
│  (Custom MCP Server: bob-a11y-mcp)     │  │  - watsonx.ai (Granite 3.0 LLMs)           │
│  - Multi-step Query Planner            │  │  - RAG Semantic Chunking & Grounding       │
│  - Code & Architectural Explainer      │  │  - watsonx Orchestrate Workflow Automation │
│  - Audio-First Semantic Formatter      │  │  - Watson Neural Speech Synthesis          │
└────────────────────────────────────────┘  └────────────────────────────────────────────┘
```

---

## 6. Key Features & Capabilities

1. **Smart Voice Navigator (Zero-Click Mode):**
   * Users can navigate files, folders, and sections purely using conversational voice instructions: *"Read Section 2", "Skip to conclusions", "Summarize findings".*
2. **Diagram-to-Audio (D2A) Explainer:**
   * When an architecture diagram, workflow chart, or data graph is encountered, the system interprets the visual components, relationships, and arrows, converting them into an intuitive verbal walkthrough: *"This is a 3-tier microservices architecture where client requests hit an API Gateway, which forwards to..."*
3. **Structured Table Verbalizer:**
   * Instead of reading every cell left-to-right, BobAccess summarizes table trends, highlights anomalies, and allows the user to query rows conversationally (*"Which department had the highest budget overrun?"*).
4. **Interactive Document Drill-Down:**
   * Users can interrupt the audio playback at any moment to ask follow-up questions without losing their reading position.
5. **Multilingual Speech Synthesis:**
   * Supports enterprise-wide global accessibility with on-the-fly translation and native-accent voice synthesis.

---

## 7. Pair-Programming Division of Labor

To maximize speed and quality within the 48-hour hackathon timeframe:

| Responsibility | Antigravity (Co-pilot & Architect) | IBM Bob Standalone IDE (Builder Engine) |
| :--- | :--- | :--- |
| **System Design** | Architecture diagrams, schemas, API contracts, folder scaffolding | Reviews repository context, implements codebase structure |
| **Coding Tasks** | Writes prompt templates, frontend components, and test cases | Implements backend routes, executes tests in terminal, refactors code |
| **MCP Integration** | Designs MCP server specification and JSON schema | Hosts and runs the MCP server, binds tools into Bob's agentic loop |
| **Submission** | Demo video scripting, pitch deck structure, README documentation | Stars in live demo video showing agentic Plan and Code modes |

---

## 8. Hackathon Execution Roadmap (48 Hours)

### Milestone 1: Foundation & Scaffold (Hours 0 – 10)
- [x] Project architecture blueprint finalized (`PROJECT_BLUEPRINT.md`).
- [ ] Initialize repository structure (`/backend`, `/frontend`, `/mcp-server`).
- [ ] Set up Python FastAPI backend with healthcheck and basic configuration.
- [ ] Set up Accessible Next.js / React frontend with audio wave visualizer.

### Milestone 2: Document Ingestion & Vision/OCR (Hours 10 – 20)
- [ ] Implement PDF text extraction and layout chunking.
- [ ] Add image/diagram extraction and semantic image description pipeline.
- [ ] Build vector store integration (ChromaDB) for document embeddings.

### Milestone 3: IBM Bob MCP Server & watsonx Integration (Hours 20 – 32)
- [ ] Build `bob-a11y-mcp` (Model Context Protocol server) exposing search and document tools.
- [ ] Integrate IBM watsonx.ai Granite 3.0 prompt templates for audio-first summarization.
- [ ] Connect IBM Watson Text-to-Speech (TTS) and Speech-to-Text (STT) streaming endpoints.

### Milestone 4: Frontend Accessibility & Voice UX (Hours 32 – 40)
- [ ] Implement WCAG 2.1 AAA high-contrast theme, keyboard navigation, and audio feedback chimes.
- [ ] Implement real-time voice recording, streaming response, and playback speed control.
- [ ] End-to-end testing with sample enterprise documents (System Architecture PDF, Financial Report, SOC2 Audit).

### Milestone 5: Demo Video, Pitch & Submission (Hours 40 – 48)
- [ ] Record 2–3 minute submission video showcasing IBM Bob Standalone IDE in action.
- [ ] Deploy live prototype (or showcase rock-solid local demo).
- [ ] Finalize GitHub documentation, architecture diagrams, and submit on LabLab.ai.

---

## 9. Deliverables for Judges

1. **Live Working Prototype:** A fully responsive, accessible web app with voice navigation and real-time audio reading.
2. **Clean GitHub Repository:** Well-organized code with architecture diagrams, setup instructions, and clean commit history.
3. **Demo Video (2–3 Minutes):** Highlighting the problem, showing the accessible UI, and recording IBM Bob Standalone IDE actively reasoning, planning, and coding.
4. **LabLab.ai Project Page:** Engaging pitch, team details, technology stack overview, and future roadmap.
