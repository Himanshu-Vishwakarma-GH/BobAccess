# BobAccess: 2.5-Minute Hackathon Demo & Pitch Script
> **Event:** IBM Bob 2.0 Hackathon on LabLab.ai  
> **Speaker Notes & Screen Walkthrough Guide**

---

## ⏱️ Video Breakdown (Target: 2 Minutes 30 Seconds)

### Part 1: The Hook & The Problem (0:00 – 0:35)
* **What to Show on Screen:** Slide or high-contrast title of **BobAccess**, followed by a quick glimpse of a dense, complicated enterprise architecture document.
* **What to Say:**
  > *"Hi judges! Over 2 billion people worldwide live with visual impairment. But in modern software engineering and enterprise IT, accessibility tools have fallen drastically behind.*
  > 
  > *Legacy screen readers like JAWS and NVDA read technical documentation like robotic alphabet soup—reading every bracket, colon, and table border line-by-line. Worse, when an engineer encounters an architecture diagram or cloud flowchart, it's a complete black box.*
  > 
  > *Today, we’re proud to introduce **BobAccess**: the first voice-first, multimodal accessibility and technical knowledge agent, powered directly by **IBM Bob** and the **IBM ecosystem**."*

---

### Part 2: The Accessible Frontend in Action (0:35 – 1:20)
* **What to Show on Screen:** Open [`frontend/index.html`](file:///D:/IBM%20BOB%20-%20LabLab%20Hackathon/frontend/index.html) in your browser.
* **Actions to Take:**
  1. Toggle **High Contrast (AAA)** mode using the top-right button or pressing `H`. Explain that it's designed for users with low vision.
  2. Press the **Spacebar** or click the quick prompt: *"What are the p50 and p99 latency targets for the API Gateway and Order Ingestion?"*
  3. Show the real-time audio waveform animating and listen to the voice synthesis output.
* **What to Say:**
  > *"Here is the BobAccess interface, built from the ground up for WCAG 2.1 AAA compliance with high-contrast amber themes, subtle audio cues, and zero-click keyboard navigation.*
  > 
  > *Notice what just happened: instead of reading a 5-column table cell-by-cell, BobAccess converted the dense performance benchmarks into a clear, audio-first spoken briefing: highlighting that the API Gateway achieves an 8ms p50 and 18ms p99 at 99.99% availability.*
  > 
  > *Now watch what happens when we ask about a visual diagram."*
  4. Click the button: *"Audio Walkthrough: 3-Tier Cloud Architecture Flowchart"*.
  > *"BobAccess translates the visual topology into a left-to-right mental walkthrough: starting with TLS termination at the gateway, moving through Go microservices on Kafka, and persisting to encrypted IBM Db2."*

---

### Part 3: Deep IBM Bob Standalone IDE Integration (1:20 – 2:05)
* **What to Show on Screen:** Switch your screen to your **IBM Bob Standalone IDE** window.
* **Actions to Take:**
  1. Point to `.bob/mcp.json` and `mcp-server/server.py`.
  2. Show the chat interface where Bob called `search_accessible_knowledge` and `explain_technical_diagram`.
* **What to Say:**
  > *"The heart of this platform is **IBM Bob**. Rather than just using Bob as an IDE, we integrated Bob as an autonomous agentic service using the **Model Context Protocol (MCP)**.*
  > 
  > *In `.bob/mcp.json`, we exposed three custom tools to Bob: document search, table verbalization, and diagram explanation. When a query arrives, Bob uses its agentic reasoning loop to autonomously invoke these tools, query our ChromaDB vector store, and construct audio-friendly responses.*
  > 
  > *We also used our **IBM Bob Enterprise subscription and Bob Coins** to scaffold, build, and test this entire multi-tier system right here in the Bob Standalone IDE."*

---

### Part 4: Enterprise Impact & Conclusion (2:05 – 2:30)
* **What to Show on Screen:** Switch back to the BobAccess dashboard or a closing summary slide.
* **What to Say:**
  > *"With global compliance regulations like the European Accessibility Act and ADA Title III, accessibility is no longer optional—it is an enterprise imperative.*
  > 
  > *BobAccess proves how IBM Bob can empower visually impaired engineers and analysts to navigate corporate knowledge bases and system architectures with complete independence.*
  > 
  > *Thank you, and we look forward to bringing BobAccess to enterprise teams worldwide!"*
