import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO)

class LLMOrchestrator:
    def __init__(self):
        self.providers = ["gemini_flash", "groq_llama3", "deepseek"]

    def truncate_payload(self, text: str, max_chars: int = 12000) -> str:
        """Prevents 413 Payload Too Large by truncating dense content."""
        if len(text) <= max_chars:
            return text
        logging.warning("Payload exceeds limit. Truncating content to prevent HTTP 413.")
        return text[:max_chars]

    async def _execute_provider_call(self, provider: str, payload: str):
        # Placeholder simulating external API call logic
        if random.random() < 0.2:  # Simulate rate limit exception
            raise Exception("429 Too Many Requests")
        return f"Processed standard extraction via {provider}"

    async def extract_with_fallback(self, prompt: str, raw_content: str):
        safe_content = self.truncate_payload(raw_content)
        
        for provider in self.providers:
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    logging.info(f"Attempting extraction using provider: {provider}")
                    response = await self._execute_provider_call(provider, safe_content)
                    return response
                except Exception as e:
                    if "429" in str(e):
                        retry_count += 1
                        backoff = (2 ** retry_count) + random.uniform(0, 1)
                        logging.warning(f"429 Rate Limit on {provider}. Retrying in {backoff:.2f}s...")
                        await asyncio.sleep(backoff)
                    else:
                        logging.error(f"Failed with provider {provider}. Moving to fallback tier.")
                        break  # Break inner retry loop to try the next provider tier
                        
        raise RuntimeError("All LLM providers failed to process payload.")