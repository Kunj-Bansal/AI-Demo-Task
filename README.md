# GraphOne / FrontierAtlas - Data Engineering Pipeline

A resilient, scalable ingestion pipeline built to extract, process, resolve, and structure venture intelligence and AI ecosystem data at scale.

## Core Features
- **Massive Ingestion Engine**: Asynchronous web scraping via `asyncio` and `aiohttp`.
- **24-Hour Signal Ingestion**: Automatic parsing and normalization of publication timestamps using relative date heuristics.
- **Resilient LLM Engine**: Multi-tier fallback (Gemini Flash → Groq Llama 3 → DeepSeek) with dynamic payload truncation to prevent 413s and 429 backoff handling.
- **Deterministic Entity Resolution**: String normalization combined with fuzzy string matching (`rapidfuzz`) to map messy startup names to canonical forms.

## Project Structure
```text
.
├── src/
│   ├── ingestion/       # Async crawlers & scraping engines
│   ├── processing/      # Date normalization & text cleaning
│   ├── llm/             # Fallback engine & payload chunking
│   ├── resolution/      # Entity resolution & mapping logic
│   └── pipeline.py      # Master orchestrator script
├── requirements.txt     # Python dependencies
├── architecture.pdf     # 3-Page System Architecture Overview
└── README.md            # Setup and execution guide