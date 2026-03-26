import unicodedata


def normalize_whitespace(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_term(value: str) -> str:
    return normalize_whitespace(value).lower()


def normalize_for_keyword_match(value: str) -> str:
    normalized = normalize_term(value)
    ascii_only = unicodedata.normalize("NFKD", normalized).encode("ascii", "ignore").decode("ascii")
    return ascii_only
