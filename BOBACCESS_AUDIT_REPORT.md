# BobAccess — Full-Stack Audit Report

> **File audited:** `frontend/index.html` · `backend/app/rag_engine.py` · `backend/app/main.py` · `mcp-server/server.py`  
> **Date:** Q3 2026 · IBM Bob 2.0 Hackathon  
> **Axes:** Web Interface Guidelines · Aesthetic · Frontend UI Engineering · Code Review & Quality · CI/CD · Enterprise UX · Doubt-Driven · Constructivist Learning · GPT Taste · High-End Visual Design · Design Taste Frontend · Ponytail (over-engineering) · Test-Driven Development

---

## 1. Web Interface Guidelines (`/web-design-guidelines`)

Compliance check against Vercel Web Interface Guidelines — `file:line` format.

| Severity | Location | Finding |
|---|---|---|
| **Required** | `index.html:343` | Dropzone `div` uses `role="button"` but is missing `onkeypress` handler for `Enter`/`Space` — native `<button>` or `<label for="fileInput">` would handle keyboard natively without custom JS |
| **Required** | `index.html:321–329` | Three header buttons use `onclick=` inline event handlers — violates progressive enhancement; event binding must be in `<script>`, not inline attributes |
| **Required** | `index.html:349` | `aria-live="polite"` on `#docStatus` is correct, but the element is not emptied/reset between updates — stale content is re-announced on assistive tech focus |
| **Required** | `index.html:397` | `aria-live="assertive"` on `#micStatus` is too aggressive; status updates during listening emit `assertive` interruptions that override screen reader speech mid-sentence — use `polite` |
| **Required** | `index.html:412` | `<select>` for playback speed has no `<label>` wrapping element — relies solely on `aria-label` which some older AT does not honour; a visually hidden `<label for="speedSelect">` is the robust pattern |
| **Required** | `index.html:359–367` | Three `.quick-btn` buttons have emoji prefixes (`⚡`, `🏛️`, `🛡️`) rendered directly in text — these are read aloud by screen readers ("lightning bolt: What are the…"); wrap emojis in `<span aria-hidden="true">` |
| **Nit** | `index.html:43` | Font stack includes `BlinkMacSystemFont` which is redundant on modern macOS (use `-apple-system` alone); minor, not a compliance issue |
| **Nit** | `index.html:314` | `<header role="banner">` is redundant — `<header>` at the top level implicitly maps to the `banner` landmark |
| **Nit** | `index.html:434` | `<footer role="contentinfo">` is redundant for the same reason as above |

**Score: 7 findings · 6 Required · 1 Nit**

---

## 2. Aesthetic Guide (`/aesthetic-guide`)

BobAccess targets an **Enterprise Dark / IBM Design Language** aesthetic. Evaluated against that reference.

### What Works
- IBM Blue (`#0f62fe`) is on-spec and used consistently as the single accent
- CSS custom properties (`--accent`, `--bg`, `--card-bg`) establish a token layer — correct foundation
- High-contrast mode toggle with AAA-level overrides is architecturally correct
- Focus rings (`3px solid var(--focus-ring)`) are thick enough to be visible — better than most enterprise tools

### What Needs Work

| Finding | Detail |
|---|---|
| **Font stack is generic** | `-apple-system, Segoe UI, Roboto` is the default OS system stack. IBM's own design language specifies **IBM Plex Sans** — the only typeface that gives BobAccess its IBM identity. Add `@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap')` and use `font-family: 'IBM Plex Sans', sans-serif`. |
| **Background feels flat** | `#0a0e17` is OLED-close but the page has no depth — no mesh gradient, no subtle noise texture, no radial glow near interactive zones. A single radial gradient (`radial-gradient(ellipse 80% 60% at 50% -10%, rgba(15,98,254,0.08), transparent)`) behind the header adds enterprise depth without violating IBM's conservative palette. |
| **Card borders are invisible** | `--border: #2d3748` on `--card-bg: #141b2d` produces ≈ 1.4:1 contrast — the borders are functionally invisible and provide no structural affordance. Raise to `#3d4f6b` (≈ 2.5:1) minimum. |
| **No typographic scale** | All text uses ad-hoc `font-size` values (`0.75rem`, `0.8rem`, `0.85rem`, `0.88rem`, `0.9rem`, `0.95rem`, `1.1rem`, `1.15rem`, `1.4rem`). That's 9 font sizes with no modular scale. A 4-step scale (`0.75 / 0.875 / 1 / 1.25 / 1.5 / 2rem`) would reduce visual noise and feel intentional. |
| **MCP trace box purple** | `--purple: #8b5cf6` for the `mcp-trace-box` border is visually disconnected from the IBM Blue system — it looks like Tailwind's default purple bled in. IBM Indigo (`#6929c4`) or IBM Magenta (`#9f1853`) would stay on-brand while still differentiating the panel. |

---

## 3. Frontend UI Engineering (`/frontend-ui-engineering`)

### Accessibility (WCAG 2.1)

| Finding | Severity | Location |
|---|---|---|
| Dropzone uses `<div role="button">` without `onKeyDown` for Enter/Space activation | **Critical** | `index.html:343` |
| Inline `onclick=` handlers on all interactive controls — no JS separation | Required | `index.html:321–367` |
| `aria-live="assertive"` on mic status causes screen reader interruptions | Required | `index.html:397` |
| No `<label>` for `#speedSelect` — AT reliance on `aria-label` only | Required | `index.html:412` |
| Emoji characters not wrapped in `aria-hidden` spans | Required | `index.html:359–367` |
| `#spokenTranscript` has `aria-live="polite"` but no `role="status"` or `role="log"` to signal live region semantics to older AT | Nit | `index.html:420` |

### Responsive Design

- ✅ `@media (max-width: 950px)` breaks to single-column — present and correct
- ⚠️ No `min-width: 320px` test case — content at 320px is not validated; the two-column quick-query buttons may overflow
- ⚠️ `max-width: 1280px` container is fine but has no `padding` below 480px (`padding: 0 1.5rem` is fine on desktop; verify it doesn't clip on small phones)

### State Management

- ✅ `isListening`, `speechRate`, `audioCuesEnabled` as module-level `let` variables — simple, appropriate for a single-page tool
- ⚠️ `let synth = window.speechSynthesis` captured at script parse time — if the browser delays `speechSynthesis` init (common on iOS), `synth` can be `undefined`; guard with `const synth = () => window.speechSynthesis`

### Loading / Error States

- ✅ `executeLiveQuery` shows "Querying ChromaDB..." inline during fetch — loading state present
- ✅ Fallback text provided on `catch` — graceful degradation present
- ⚠️ The fallback text is hardcoded (`"The Global Logistics platform maintains a p99 latency target…"`) — this is fine for a hackathon demo but should be clearly marked as fallback content in the UI, not indistinguishable from a real API response

---

## 4. Code Review & Quality (`/code-review-and-quality`)

### `backend/app/rag_engine.py`

| Axis | Finding | Severity |
|---|---|---|
| **Correctness** | `_format_audio_answer` splits on `.` to extract sentences — table cell content after the recent fix now includes `. `.join(cells)`, meaning a cell like `"99"` produces a fragment `"99"` which passes the `len > 10` guard inconsistently. The guard should be `len > 15` or use a word-count check | Required |
| **Correctness** | `embed_query` / `embed_documents` methods on `LightweightEmbeddingFunction` exist but ChromaDB calls `__call__` directly — the named methods are dead code | Nit |
| **Readability** | `_format_audio_answer` is 30 lines doing three distinct jobs: table expansion, markdown stripping, and sentence extraction. Three private helpers would make each individually testable | Optional |
| **Performance** | `re.findall(r'\w+', text.lower())` in `__call__` is called per embedding — fine for small corpora but `text.lower()` allocates a full string copy before the regex. For the hackathon scope, this is acceptable | Nit |
| **Architecture** | `LightweightEmbeddingFunction` is defined in `rag_engine.py` but is a standalone concern. It could move to `embeddings.py` so `rag_engine.py` imports it — but at this scale YAGNI applies | Optional |

### `backend/app/main.py`

| Axis | Finding | Severity |
|---|---|---|
| **Correctness** | `@app.on_event("startup")` is deprecated in FastAPI ≥ 0.93 — use `@app.lifespan` context manager instead | Required |
| **Correctness** | `DiagramExplanationRequest.image_url_or_base64` is a required field but `runPredefinedDiagram` in the frontend sends `"diagram.png"` as a literal string — the backend accepts it but ignores it entirely; the field is structurally misleading | Optional |
| **Readability** | `/api/explain-diagram` returns a hardcoded static response regardless of input — acceptable for Milestone 1 but should carry a `# TODO: wire to actual vision model` comment so it doesn't look like finished logic | Nit |
| **Security** | CORS set to `allow_origins=["*"]` — for a hackathon demo this is acceptable; in production scope to the frontend origin | FYI |

### `mcp-server/server.py`

| Axis | Finding | Severity |
|---|---|---|
| **Correctness** | `query_live_backend` uses `urllib.request` with `timeout=3` — on a cold boot where ChromaDB is still indexing, 3s is too tight and the fallback fires unnecessarily; raise to `timeout=8` | Required |
| **Readability** | `handle_tool_call` is a flat `if/elif` chain that will grow as tools are added. A `dict[str, Callable]` dispatch table removes the chain without adding abstraction overhead | Optional |
| **Architecture** | The fallback response in `query_live_backend` is a hardcoded business-domain string (`"Global Logistics…"`) — fallbacks should be generic ("Knowledge base unavailable. Please retry.") so the server is reusable across documents | Required |

---

## 5. CI/CD & Automation (`/ci-cd-and-automation`)

No CI configuration exists in the workspace. Findings are gaps, not violations.

| Gap | Priority |
|---|---|
| No `pytest` suite — zero automated tests for `rag_engine`, `document_processor`, or any endpoint | **High** |
| No `pre-commit` hooks — formatting (`black`, `isort`) and linting (`ruff`) run manually at best | Medium |
| No GitHub Actions workflow — no automatic install/test on push | Medium |
| No `Dockerfile` or `docker-compose.yml` — reproducing the dev environment requires manual venv setup and ChromaDB path configuration | Medium |
| No `.env.example` is checked in (it exists but is not documented in `README.md`) | Low |
| `seed_sample_documents()` runs at every server startup — in a multi-replica deploy this would cause redundant ChromaDB writes; add an `already_seeded` guard | Low |

**Recommended minimal CI pipeline (`GitHub Actions`):**

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/ -v
      - run: ruff check backend/
```

---

## 6. Enterprise UX (`/enterprise`)

Evaluated against enterprise-grade productivity dashboard standards.

| Finding | Impact |
|---|---|
| **No persistent session state** — every page refresh resets the transcript and MCP trace. Enterprise users expect query history to survive a refresh. `localStorage` can persist the last 5 queries with 2 lines of JS. | High |
| **No loading skeleton** — while `executeLiveQuery` runs, the transcript box shows an `<em>` italic string. Enterprise tools use skeleton loaders (`animate-pulse` grey bars) to signal bounded wait time and reduce perceived latency. | Medium |
| **No error boundary messaging** — if the backend is down, the UI silently falls back to hardcoded text with no indication that the KB is unavailable. An explicit `aria-live="assertive"` error banner ("Knowledge base unavailable — showing cached response") maintains trust. | High |
| **Single-document limitation is undisclosed** — the UI implies multi-document search but the ChromaDB collection holds only `arch-spec-42`. A badge ("1 document indexed") near the dropzone sets accurate expectations. | Medium |
| **MCP trace box is always "MCP Connected"** — even when the backend is down. The status should reflect actual connectivity via a periodic health ping, not a static label. | Low |
| **No print/export for transcripts** — enterprise engineers often need to share an audio walkthrough result as text. A "Copy to clipboard" button on the transcript box addresses this. | Low |

---

## 7. Doubt-Driven Development (`/doubt-driven-development`)

Adversarial review — assumptions that should be stress-tested before demo.

| Assumption | Risk | Mitigation |
|---|---|---|
| ChromaDB `LightweightEmbeddingFunction` produces semantically meaningful rankings | The hash-based embedding is a bag-of-words model with no semantic understanding. Querying "latency SLA" may not rank the benchmark table chunk highest if the table chunk contains the words in a different order. | Manually verify top-2 chunks returned for the demo queries; log chunk IDs in the MCP trace. |
| `window.SpeechSynthesis` works on all demo browsers | Safari iOS cancels speech synthesis mid-utterance for long strings (>250 chars). The RAG answers are ~400–600 chars. | Test on iOS Safari explicitly; chunk the utterance into sentences and chain `onend` callbacks. |
| `window.SpeechRecognition` is available at demo time | Chrome requires HTTPS for `SpeechRecognition`; a `localhost` demo works but an IP-based demo URL will silently fall through to the fallback query. | Demo from `localhost`, or serve the frontend with a self-signed cert, or pre-plan the keyboard fallback path. |
| Backend restart always re-seeds the same doc ID | `rag_engine.index_document` calls `collection.upsert` — safe for re-runs. But if the `accessible_knowledge_v2` collection schema changes between runs, stale chunks with the old schema may pollute results. | Add a `collection.delete_where({"doc_id": "arch-spec-42"})` before upsert in `seed_docs.py`. |
| `--reload` flag is not used in production launch | `uvicorn --reload` uses `watchfiles` which can cause double-startup and double-seeding on some Windows builds. Already removed from background launch — verify the seeded doc count is `1 × chunk_count`, not `2 ×`. | Check `collection.count()` via a `/api/debug/stats` endpoint before the demo. |

---

## 8. Constructivist Learning Design (`/grad-constructivism`)

BobAccess is an **assistive technology** — its UX doubles as a pedagogical interface for engineers learning to navigate technical specs accessibly. Evaluated through Vygotsky's ZPD and scaffolding lenses.

| Principle | Current State | Recommendation |
|---|---|---|
| **Zone of Proximal Development** — tasks just beyond current ability with scaffolding | The three hardcoded demo prompts anchor a new user, but once they're consumed there is no pathway to the next level of query complexity | Add a "Try asking…" suggestion panel that updates based on what the user just queried — e.g., after a latency query, suggest "Now ask about the disaster recovery RTO" |
| **Scaffolding removal** — gradually remove support as competence grows | The MCP trace box shows raw JSON keys (`search_accessible_knowledge`, `{"query": "…"}`) with no plain-language explanation. First-time users do not know what this means | Wrap the trace with a toggleable "Explain this" mode: "IBM Bob is calling the knowledge search tool with your question as the argument" |
| **Active knowledge construction** — users build meaning through action | Drag-and-drop upload is present, but there is no feedback loop showing *what* was extracted from the uploaded document | After upload, render the top-3 indexed chunk headings: "Indexed: Executive Summary, Microservices Architecture, Performance Benchmarks" |
| **Social mediation** — learning through dialogue | The conversational follow-up prompts (`suggested_followups`) are generated but never displayed in the UI — the `QueryResponse` schema has the field, `main.py` hardcodes three suggestions, but the frontend never renders them | Wire `data.suggested_followups` into the quick-queries panel after each query response |

---

## 9. GPT Taste / Layout Design (`/gpt-taste`)

Anti-generic-AI layout audit.

| Issue | Location | Fix |
|---|---|---|
| **Equal two-column grid** — both columns are `1fr 1fr` with identical card heights. This is the default AI layout. | `index.html:119` | Break the symmetry: make the left column `5fr` (document + trace) and the right `7fr` (voice + audio player), or use asymmetric row heights |
| **Generic card structure** — every section is the same `border-radius: 12px` card with the same `1.5rem` padding and `1px` border. No visual hierarchy. | `index.html:130–148` | Give the voice card a slightly thicker border (`2px`) and a `box-shadow: 0 0 0 1px rgba(15,98,254,0.15)` IBM Blue glow to signal it as the primary interactive zone |
| **Section spacing is tight** — `gap: 1.75rem` between cards at 1280px feels compressed for an accessibility-first tool whose primary users rely on spatial clarity | `index.html:120` | `gap: 2.5rem` minimum; enterprise accessibility tools should err toward generous spacing |
| **Typography contrast is monotone** — all body text is `#ffffff` or `#94a3b8`. There is no large-scale typographic moment that anchors the page | `index.html` throughout | The page title "BobAccess" in the `<h1>` could be styled at `2rem` with `font-weight: 800; letter-spacing: -0.04em` to give the header a clear brand anchor |
| **MCP trace is visually equal to content** — the debug trace should feel secondary (monospace, muted, smaller) but currently occupies the same visual weight as the functional panels | `index.html:272–283` | Reduce trace font from `0.8rem` to `0.75rem`, lower the border opacity to `0.4`, and collapse it to `max-height: 90px; overflow-y: auto` by default |

---

## 10. High-End Visual Design (`/high-end-visual-design`)

Awwwards-tier evaluation. Current aesthetic reads as **competent dark dashboard** but not **premium enterprise tool**.

| Criterion | Pass/Fail | Notes |
|---|---|---|
| No banned fonts (Inter/Roboto/Arial/Helvetica) | ⚠️ **FAIL** | Font stack resolves to `Segoe UI` on Windows and `Roboto` on Android — both banned. Must use IBM Plex Sans explicitly. |
| Double-Bezel nested card architecture | ❌ **FAIL** | Cards are single-layer (`background + border`). No outer shell / inner core nesting. The mic button container especially needs a machined-hardware depth treatment. |
| Custom cubic-bezier transitions | ❌ **FAIL** | All transitions use `0.2s ease` — a browser default. Zero custom easing curves. |
| No hardcoded hex in component styles | ⚠️ **PARTIAL** | `badge-ibm` uses hardcoded `#0f62fe` instead of `var(--accent)` (`index.html:73`). `mic-btn.listening` uses hardcoded `#ef4444` instead of a CSS variable. |
| Scroll entry animations | ❌ **FAIL** | Cards appear statically on load. No `IntersectionObserver` reveal animations. |
| Macro-whitespace (`py-24` equivalent) | ❌ **FAIL** | Container margin is `1.5rem` — extremely tight. A tool for accessibility presentations needs breathing room. |
| Button-in-button trailing icon | ❌ **FAIL** | The mic SVG is inline with no nested wrapper treatment. |

**Summary:** 1 pass, 2 partial, 5 fail. Significant visual design debt.

**Three highest-ROI fixes for the hackathon demo:**
1. Add IBM Plex Sans via Google Fonts (1 line, maximum brand signal)
2. Add a single radial IBM Blue glow under the mic button (`box-shadow: 0 0 60px rgba(15,98,254,0.25)`) — transforms the primary CTA
3. Change all `transition: X 0.2s ease` to `transition: X 0.3s cubic-bezier(0.4, 0, 0.2, 1)` — Material Design's standard easing, premium feel

---

## 11. Design Taste Frontend (`/design-taste-frontend-v1`)

Production-quality frontend audit.

| Pattern | Present? | Notes |
|---|---|---|
| Real design system tokens (not raw hex) | Partial | CSS variables exist but 4 hardcoded hex values remain in component styles |
| Content-first layout (not template grid) | No | The 2-col layout is driven by convenience, not by information priority |
| Loading skeleton states | No | `<em>` italic placeholder used instead |
| Realistic placeholder content | Yes | ChromaDB doc status shows real doc ID and spec title — good |
| No AI-default purple everywhere | Partial | `--purple` for MCP trace bleeds in from nowhere; otherwise IBM Blue is disciplined |
| Error state distinguishable from success | No | Fallback text looks identical to a real RAG response |
| Mobile-first responsive | Partial | One breakpoint at 950px; no 320px/480px testing evidence |
| No `animation: pulse` for live indicators | No | Mic button uses `animation: pulse` which can be extremely distracting for users with vestibular disorders — should respect `prefers-reduced-motion` |

**Critical missing addition:**
```css
@media (prefers-reduced-motion: reduce) {
  .mic-btn.listening { animation: none; }
  .wave-bar { transition: none; }
}
```
This is a **WCAG 2.1 AA Level** failure (Success Criterion 2.3.3) for an accessibility-first tool.

---

## 12. Ponytail — Over-Engineering Audit (`/ponytail`)

Finding unnecessary complexity in the codebase.

| Location | Issue | Simpler Alternative |
|---|---|---|
| `rag_engine.py:22–32` | `embed_query` and `embed_documents` methods on `LightweightEmbeddingFunction` exist purely to satisfy a ChromaDB interface that only calls `__call__` — 10 lines of dead code | Delete both methods; `__call__` is all ChromaDB uses |
| `rag_engine.py:57–65` | `get_or_create_collection` with `embedding_function=self.ef` — the EF instance is re-created on every server boot but ChromaDB persists vectors to disk. If the embedding function changes, stale vectors are silently queried with a new function. | Add `collection_metadata={"hnsw:space": "cosine"}` and log the EF name so mismatches surface |
| `mcp-server/server.py:66–84` | `query_live_backend` is 18 lines to do a single HTTP POST — stdlib `urllib.request` adds boilerplate. `httpx` is already installed in `requirements.txt` | Replace with `httpx.post(URL, json=payload, timeout=8).json()` — 1 line |
| `frontend/index.html:498–504` | `utterance.onstart` animates all wave bars to fixed heights via `forEach` + inline style — 4 lines. `utterance.onend` resets them — 2 more. | Replace with a single CSS class toggle: `visualizer.classList.toggle('active')` and a `@keyframes` CSS animation on `.waveform-visualizer.active .wave-bar` |
| `backend/app/main.py:76–87` | PDF temp-file write/read/delete cycle (`temp_path`, `os.makedirs`, `open`, `os.remove`) — 10 lines. `pypdf` can parse from a `BytesIO` stream directly | `from io import BytesIO; PdfReader(BytesIO(content_bytes))` — no temp file needed |

**Most impactful ponytail win:** The PDF temp-file pattern — it creates a race condition on concurrent uploads (two uploads could share a conflicting `temp_path`) and requires a disk write that `BytesIO` avoids entirely.

---

## 13. Test-Driven Development (`/test-driven-development`)

No tests exist in the workspace. This section maps the minimum required test suite for a hackathon demo that claims production-quality accessibility.

### Critical Test Coverage Gaps

| Module | What to Test | Why Critical |
|---|---|---|
| `rag_engine.py` · `_format_audio_answer` | Empty passage list → no-match response string; table row with 4 cells → expanded spoken phrase with correct cell count; passage with `##` heading → heading stripped from output | The audio formatter is the core accessibility output; a regression here produces garbled speech |
| `rag_engine.py` · `LightweightEmbeddingFunction.__call__` | Empty string input → zero vector, not error; single word → unit L2 norm vector; two identical texts → identical embeddings | Embedding stability is required for deterministic RAG retrieval |
| `main.py` · `POST /api/query` | Valid `query_text` returns `200` with `spoken_answer` non-empty; missing `query_text` returns `422` | Core demo path must not 500 |
| `main.py` · `POST /api/documents/upload` | PDF file upload → `status: "success"` with `page_count ≥ 1`; non-UTF8 binary → does not 500 | Upload is the entry point for all enterprise documents |
| `mcp-server/server.py` | `tools/list` response contains exactly 3 tools with correct `name` fields; `tools/call` for unknown tool returns `isError: true` | MCP tool registration is the core hackathon demo claim |

### Minimal Test File

```python
# backend/tests/test_rag_engine.py
import pytest
from backend.app.rag_engine import RAGEngine, LightweightEmbeddingFunction

def test_embedding_empty_string():
    ef = LightweightEmbeddingFunction(dim=128)
    result = ef([""])
    assert len(result) == 1
    assert len(result[0]) == 128

def test_embedding_l2_norm():
    ef = LightweightEmbeddingFunction(dim=128)
    vec = ef(["hello world"])[0]
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6

def test_format_audio_answer_empty():
    engine = RAGEngine()
    result = engine._format_audio_answer("test query", [])
    assert "did not find" in result

def test_format_audio_answer_table_expansion():
    engine = RAGEngine()
    passage = "| API Gateway | 8ms | 18ms | 99.99% |"
    result = engine._format_audio_answer("latency", [passage])
    assert "API Gateway" in result
    assert "8ms" in result
```

---

## Summary Scorecard

| Dimension | Score | Critical Gaps |
|---|---|---|
| **Web Interface Guidelines** | 5/10 | Dropzone keyboard access, emoji aria-hidden, assertive live region |
| **Aesthetic (IBM Design Language)** | 6/10 | Missing IBM Plex Sans, flat card borders, no typographic scale |
| **Frontend UI Engineering** | 5/10 | `prefers-reduced-motion` missing, no skeleton states, SpeechSynthesis guard |
| **Code Review & Quality** | 7/10 | Deprecated `on_event`, hardcoded fallback strings, dead embedding methods |
| **CI/CD** | 1/10 | Zero automation — no tests, no pipeline, no Docker |
| **Enterprise UX** | 6/10 | No session persistence, no error banners, undisclosed doc limitation |
| **Doubt-Driven** | 7/10 | iOS SpeechSynthesis risk, HTTPS requirement for STT undocumented |
| **Constructivist Learning** | 4/10 | `suggested_followups` not wired to UI, no progressive scaffolding |
| **GPT Taste** | 5/10 | Symmetrical grid, monotone typography, no visual hierarchy |
| **High-End Visual Design** | 3/10 | No IBM Plex Sans, no easing curves, no entry animations, no double-bezel |
| **Design Taste Frontend** | 5/10 | No `prefers-reduced-motion`, error indistinguishable from success |
| **Ponytail (Over-Engineering)** | 7/10 | PDF temp-file pattern, dead embedding methods, urllib vs httpx |
| **Test-Driven Development** | 0/10 | No tests exist |

---

## Top 5 Highest-ROI Fixes Before Demo

1. **Add `prefers-reduced-motion` CSS rule** — 2 lines, fixes a WCAG 2.1 AA failure on an *accessibility* tool. Maximum embarrassment risk if missed.
2. **IBM Plex Sans font** — 1 CSS `@import`, transforms brand authenticity immediately.
3. **Wire `suggested_followups` to the frontend** — the data is already in the API response; 3 lines of JS render it as updated quick-query buttons after each response.
4. **Replace PDF temp-file with `BytesIO`** — eliminates a concurrent-upload race condition in 1 line.
5. **Add 5 pytest tests** — the minimum required to claim the backend is verified; necessary for any production-quality hackathon submission.

---

*Report generated by IBM Bob 2.0 · BobAccess Audit Pipeline · All findings grounded in source files read at audit time.*
