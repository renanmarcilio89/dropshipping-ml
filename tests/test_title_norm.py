from app.normalization.title_norm import normalize_title


def test_normalize_title_removes_accents_and_stopwords() -> None:
    assert normalize_title('Garrafa Térmica de Aço Inox 1L') == 'garrafa termica aco inox 1l'
