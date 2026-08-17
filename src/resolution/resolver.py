import re
from rapidfuzz import process, fuzz

class EntityResolver:
    """
    Handles deterministic entity resolution by stripping corporate suffixes,
    normalizing text formatting, and performing fuzzy matching against a canonical seed list.
    """
    def __init__(self, canonical_seeds: list[str] | None = None, threshold: float = 85.0):
        # Default mock seed list of 50 AI companies if none provided
        self.canonical_seeds = canonical_seeds or [
            "OpenAI", "Anthropic", "Mistral AI", "Hugging Face", "Stability AI",
            "Cohere", "Midjourney", "Runway", "Perplexity", "Inflection AI",
            "Scale AI", "LangChain", "Pinecone", "Weaviate", "Qdrant",
            "Together AI", "Anyscale", "Weights & Biases", "Replicate", "Groq"
        ]
        self.threshold = threshold

    def normalize_string(self, text: str) -> str:
        """Strips legal entity suffixes, punctuation, and extra whitespace."""
        if not text:
            return ""
        text = text.lower().strip()
        # Remove corporate/legal entity identifiers
        suffix_pattern = r'\b(inc|corp|corporation|llc|ltd|pbc|ai|labs|co|gmbh)\b'
        text = re.sub(suffix_pattern, '', text)
        # Remove non-alphanumeric characters
        text = re.sub(r'[^\w\s]', '', text)
        return " ".join(text.split())

    def resolve(self, raw_name: str) -> tuple[str, float]:
        """
        Maps a raw extracted entity string to a canonical target.
        Returns a tuple of (Canonical Name, Match Confidence Score).
        """
        if not raw_name:
            return "Unknown Entity", 0.0

        clean_raw = self.normalize_string(raw_name)

        # 1. Exact direct check after string normalization
        for seed in self.canonical_seeds:
            if self.normalize_string(seed) == clean_raw:
                return seed, 100.0

        # 2. Fuzzy match fallback using Token Sort Ratio
        match_result = process.extractOne(
            clean_raw,
            self.canonical_seeds,
            scorer=fuzz.token_sort_ratio
        )

        if match_result:
            matched_seed, score, _ = match_result
            if score >= self.threshold:
                return matched_seed, score

        # If below threshold, retain raw name as novel entity
        return raw_name.strip(), 0.0

# Quick verification block
if __name__ == "__main__":
    resolver = EntityResolver()
    test_cases = ["OpenAI, Inc.", "open-ai", "Anthropic PBC", "Mistral", "Unknown Startup LLC"]
    for test in test_cases:
        canonical, score = resolver.resolve(test)
        print(f"Raw: '{test}' -> Canonical: '{canonical}' (Score: {score})")