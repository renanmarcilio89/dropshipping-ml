import re
import unicodedata


STOPWORDS = {'de', 'do', 'da', 'para', 'com', 'sem', 'e', 'a', 'o'}


def normalize_title(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9 ]+', ' ', value.lower())
    tokens = [token for token in value.split() if token not in STOPWORDS and len(token) > 1]
    return ' '.join(tokens)
