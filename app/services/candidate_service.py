from app.core.text_normalization import normalize_term


class CandidateService:
    def build_from_terms(self, terms: list[str]) -> list[str]:
        unique_terms: list[str] = []
        seen: set[str] = set()

        for term in terms:
            normalized = normalize_term(term)
            if not normalized:
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            unique_terms.append(term)

        return unique_terms
