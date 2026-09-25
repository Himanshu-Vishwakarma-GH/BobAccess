# BobAccess 🎙️♿
### The Voice-First Enterprise AI Accessibility & Technical Knowledge Suite
> **Built for the IBM Bob 2.0 Hackathon (LabLab.ai | Remote 48 Hours | September 25–27, 2026)**  
> **Powered by:** IBM Bob Standalone IDE & Enterprise Tokens, Model Context Protocol (MCP), ChromaDB Vector RAG, and IBM watsonx.ai.

[![IBM Bob](https://img.shields.io/badge/IBM%20Bob-2.0%20Agentic%20IDE-0f62fe?style=for-the-badge&logo=ibm)](https://bob.ibm.com)
[![Protocol](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-8b5cf6?style=for-the-badge)](https://modelcontextprotocol.io)
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AAA-10b981?style=for-the-badge)](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 🌟 The Challenge
Over **2.2 billion people** globally live with vision impairment. In modern enterprise technology environments:
1. **Screen readers fail on code and architecture:** Legacy tools like JAWS and NVDA read technical syntax literally (`"curly brace, colon, indent 4..."`), turning technical documentation and code diffs into robotic alphabet soup.
2. **Visual artifacts are black boxes:** Over 65% of enterprise software documentation relies on visual diagrams—cloud architecture topologies, sequence flows, ERDs, and dashboards. For visually impaired engineers, these are completely inaccessible.
3. **Regulatory mandate:** Global legislation (such as the European Accessibility Act and ADA Title III) mandates that enterprise knowledge systems be accessible by design.

---

## 💡 The Solution: BobAccess
**BobAccess** is an agentic, voice-first assistive platform that bridges this divide. It leverages **IBM Bob** as an autonomous agentic engine to convert complex corporate knowledge, technical specifications, and system diagrams into an interactive, conversational, audio-first experience.

### Key Capabilities:
* **Audio-First Speech Narration:** Transforms dense markdown tables and technical specs into natural spoken paragraphs rather than reading raw cell borders.
* **Diagram-to-Audio (D2A) Explainer:** Decodes visual topologies (e.g., 3-tier cloud architectures, Kafka event streams) into structured mental models (*"Tier 1 on the left handles traffic at the API Gateway..."*).
* **Zero-Click Voice Navigation:** Hands-free voice querying with real-time waveform visualization, audio cues, and full keyboard navigation.
* **WCAG 2.1 AAA Compliant UI:** High-contrast color themes (pure black & amber/gold), screen-reader-optimized ARIA landmarks, and sound cue feedback.

---

## 🏗️ Architecture & Technology Stack

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
│  - Voice-First Controls & Global Keyboard Shortcuts (Space to talk, Esc to silence)    │
│  - Real-Time Audio Waveform & Sound Effect Feedback Cues                               │
│  - Live Transcript & Audio Player with Variable Speed Multipliers                      │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ WebSocket / REST API
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          FASTAPI BACKEND CORE SERVICE                                  │
│  ├── Voice Controller: Speech-to-Text & Text-to-Speech Streaming                      │
│  ├── Document Processor: PDF Parser, Layout Analyzer, Markdown Sectioner              │
│  ├── Audio Semantic Formatter: Translates tables and symbols into natural speech       │
│  └── Vector Memory Engine: ChromaDB Vector Store with Zero-Network Embeddings         │
└───────────────────────┬────────────────────────────────────────┬───────────────────────┘
                        │                                        │
                        ▼                                        ▼
┌────────────────────────────────────────┐  ┌────────────────────────────────────────────┐
│      IBM BOB AGENTIC ENGINE            │  │           IBM WATSONX PLATFORM             │
│  (Custom MCP Server: bob-a11y-mcp)     │  │  - watsonx.ai (Granite 3.0 LLMs)           │
│  - search_accessible_knowledge         │  │  - RAG Semantic Chunking & Grounding       │
│  - explain_technical_diagram           │  │  - watsonx Orchestrate Workflow Automation │
│  - verbalize_table_data                │  │  - Watson Neural Speech Synthesis          │
└────────────────────────────────────────┘  └────────────────────────────────────────────┘
```

---

## 🤖 Deep IBM Bob & Enterprise Integration

BobAccess integrates IBM Bob at both the development and runtime levels:

1. **Custom Model Context Protocol (MCP) Server (`bob-a11y-mcp`):**
   * Configured in [`.bob/mcp.json`](file:///D:/IBM%20BOB%20-%20LabLab%20Hackathon/.bob/mcp.json) using the official protocol specification (`2024-11-05`).
   * Exposes three specialized agent tools directly to IBM Bob:
     * `search_accessible_knowledge`: Performs semantic retrieval over corporate documents and returns spoken summaries.
     * `explain_technical_diagram`: Converts visual diagram contexts into audio walkthroughs.
     * `verbalize_table_data`: Synthesizes complex data tables into high-level verbal insights.
2. **Autonomous Tool Execution in Bob IDE:**
   * Inside the **IBM Bob Standalone IDE**, Bob uses its agentic reasoning loop to autonomously invoke these tools when answering user questions.
3. **Enterprise Token / Bob Coins Utilization:**
   * Uses your official IBM Bob Enterprise API key (`BOB_API_KEY`) for programmatic access, tracked via Bobalytics in the IBM Bob portal.

---

## 🚀 Quickstart & Installation

### Prerequisites
* Python 3.10+ (tested with Python 3.11)
* Modern web browser (Chrome, Edge, Firefox)

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-username/bob-access.git
cd bob-access
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your IBM Bob API key:
```env
BOB_API_KEY=bob_prod_bob-apikey_...
BOB_API_URL=https://bob.ibm.com
```

### 3. Launch the Backend
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The server will automatically seed the sample enterprise architecture document (`arch-spec-42`) into the ChromaDB vector store upon startup.

### 4. Launch the Accessible Frontend
Simply open [`frontend/index.html`](file:///D:/IBM%20BOB%20-%20LabLab%20Hackathon/frontend/index.html) in any web browser!

---

## ⌨️ Accessible Controls & Keyboard Shortcuts
* **Spacebar:** Trigger / stop voice recognition query.
* **Esc:** Immediately silence current audio playback.
* **H / h:** Toggle WCAG AAA High-Contrast Mode (pure black background with amber accents).
* **Audio Cues Button:** Plays subtle Web Audio frequency chimes for auditory state feedback.

---

## 🏆 Hackathon Submission Checklist (LabLab.ai)
- [x] **Working Prototype:** Fully functional backend on port 8000 and accessible frontend.
- [x] **IBM Bob Integration:** Registered MCP server (`bob-a11y-mcp`) with verified agentic execution.
- [x] **Enterprise Grounding:** Tested with realistic corporate architecture specs and latency SLA tables.
- [x] **WCAG 2.1 AAA Accessibility:** Screen reader compatibility, high contrast, keyboard shortcuts, and audio cues.
- [x] **Documentation:** Complete technical blueprint and README.

---
*Created with ❤️ for the IBM Bob 2.0 Hackathon on LabLab.ai.*
