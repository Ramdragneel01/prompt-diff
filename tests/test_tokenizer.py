from prompt_diff.tokenizer import extract_placeholders, sentence_chunks, tokenize


def test_tokenize_basic():
    tokens = tokenize("Hello, SYSTEM_prompt! Keep API_KEY safe.")
    assert "hello" in tokens
    assert "system_prompt" in tokens
    assert "api_key" in tokens


def test_extract_placeholders():
    text = "Use {customer_id} and {{session_id}} then {customer_id} again"
    out = extract_placeholders(text)
    assert "{customer_id}" in out
    assert "{{session_id}}" in out
    assert out.count("{customer_id}") == 1


def test_sentence_chunks_fallback_single():
    out = sentence_chunks("No punctuation text")
    assert len(out) == 1
