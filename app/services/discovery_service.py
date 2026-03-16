from dataclasses import dataclass


@dataclass(slots=True)
class QueryCandidate:
    query: str
    source: str
    priority: float


class DiscoveryService:
    def build_candidates(
        self,
        seed_terms: list[str],
        trend_terms: list[str] | None = None,
        max_queries: int = 500,
    ) -> list[QueryCandidate]:
        candidates: list[QueryCandidate] = []

        seen: set[str] = set()
        for term in trend_terms or []:
            if term not in seen:
                seen.add(term)
                candidates.append(QueryCandidate(query=term, source='trend', priority=0.95))

        for term in seed_terms:
            if term not in seen:
                seen.add(term)
                candidates.append(QueryCandidate(query=term, source='manual_seed', priority=0.70))

        return candidates[:max_queries]
