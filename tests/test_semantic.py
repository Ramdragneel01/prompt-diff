from prompt_diff.semantic import change_ratio, lexical_similarity, overlap_ratio, token_jaccard


def test_lexical_similarity_identical():
    assert lexical_similarity("abc", "abc") == 1.0


def test_jaccard_partial_overlap():
    score = token_jaccard("hello world alpha", "hello beta")
    assert 0 < score < 1


def test_change_ratio_bounds():
    score = change_ratio("a", "b")
    assert 0 <= score <= 1


def test_overlap_ratio_lists():
    score = overlap_ratio(["a", "b", "c"], ["b", "c", "d"])
    assert score == 2 / 3
