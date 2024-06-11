from enum import Enum
from typing import List


class Scorers(str, Enum):
    adherence_basic = "adherence_nli"
    adherence_luna = "adherence_nli"
    chunk_attribution_utilization_basic = "chunk_attribution_utilization_nli"
    chunk_attribution_utilization_gpt = "chunk_attribution_utilization_gpt"
    chunk_attribution_utilization_luna = "chunk_attribution_utilization_nli"
    chunk_attribution_utilization_plus = "chunk_attribution_utilization_gpt"
    completeness_basic = "completeness_nli"
    completeness_gpt = "completeness_gpt"
    completeness_luna = "completeness_nli"
    completeness_plus = "completeness_gpt"
    context_adherence = "groundedness"
    context_adherence_basic = "adherence_nli"
    context_adherence_luna = "adherence_nli"
    context_adherence_plus = "groundedness"
    context_relevance = "context_relevance"
    correctness = "factuality"
    factuality = "factuality"
    groundedness = "groundedness"
    latency = "latency"
    pii = "pii"
    prompt_injection = "prompt_injection"
    prompt_perplexity = "prompt_perplexity"
    sexist = "sexist"
    tone = "tone"
    toxicity = "toxicity"
    uncertainty = "uncertainty"

    @staticmethod
    def basic_deprecated_scorer_names() -> List["Scorers"]:
        return [
            Scorers.adherence_basic,
            Scorers.completeness_basic,
            Scorers.context_adherence_basic,
            Scorers.chunk_attribution_utilization_basic,
        ]
