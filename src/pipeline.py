import asyncio
import logging
import json
from datetime import datetime, timezone
import pandas as pd

from ingestion.scraper import DataScraper
from processing.clean_dates import parse_and_validate_freshness
from llm.orchestrator import LLMOrchestrator
from resolution.resolver import EntityResolver

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class MasterPipeline:
    def __init__(self):
        self.scraper = DataScraper(concurrency_limit=20)
        self.llm_engine = LLMOrchestrator()
        self.resolver = EntityResolver()

    async def run_entity_pipeline(self):
        logging.info("Starting Master Intelligence Data Ingestion Pipeline...")
        
        # 1. Mock Raw Extracted Payloads (Simulating Scraper output)
        raw_startups = ["OpenAI, Inc.", "Anthropic PBC", "Mistral AI Corp", "Perplexity AI"]
        raw_news = [
            {"title": "New LLM Benchmark Released", "date_str": "2 hours ago", "url": "https://news.example.com/1"},
            {"title": "Old AI News Article", "date_str": "3 days ago", "url": "https://news.example.com/2"}
        ]

        # 2. Process & Resolve Entities
        startup_records = []
        entity_logs = []

        for raw in raw_startups:
            canonical, score = self.resolver.resolve(raw)
            startup_records.append({
                "schemaVersion": "1.0",
                "recordType": "STARTUP",
                "source.name": "Directory Crawler",
                "source.url": f"https://example.com/startup/{raw.lower().replace(' ', '-')}",
                "content.entityName": canonical,
                "content.data.employeeCount": 150,
                "collectedAt": datetime.now(timezone.utc).isoformat()
            })
            entity_logs.append({
                "Raw Extracted Name": raw,
                "Canonical Resolved Name": canonical,
                "Match Score / Method": f"{score}% Fuzzy Match" if score > 0 else "Exact / Retained"
            })

        # 3. Process Freshness Filter for Signals
        fresh_news = []
        for item in raw_news:
            iso_date, is_fresh = parse_and_validate_freshness(item["date_str"])
            if is_fresh:
                fresh_news.append({
                    "schemaVersion": "1.0",
                    "recordType": "NEWS",
                    "source.name": "Tech Engine",
                    "source.url": item["url"],
                    "content.title": item["title"],
                    "content.published_date": iso_date,
                    "collectedAt": datetime.now(timezone.utc).isoformat()
                })

        # 4. LLM Processing Test
        sample_prompt = "Extract key startup details."
        sample_raw_html = "<html<body><h1>OpenAI</h1><p>Leading AI research organization.</p></body></html>"
        llm_output = await self.llm_engine.extract_with_fallback(sample_prompt, sample_raw_html)
        logging.info(f"LLM Processing Result: {llm_output}")

        # 5. Export Data to Local CSVs (Ready for Google Sheets Copy/Paste)
        pd.DataFrame(startup_records).to_csv("data_startups.csv", index=False)
        pd.DataFrame(fresh_news).to_csv("data_news.csv", index=False)
        pd.DataFrame(entity_logs).to_csv("data_entity_mapping.csv", index=False)
        logging.info("Pipeline execution completed. Processed files written to CSV.")

if __name__ == "__main__":
    pipeline = MasterPipeline()
    asyncio.run(pipeline.run_entity_pipeline())