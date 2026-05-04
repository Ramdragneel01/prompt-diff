from prompt_diff.cli import run_cli


def test_cli_text_output(tmp_path, capsys):
    base = tmp_path / "base.txt"
    cand = tmp_path / "cand.txt"
    base.write_text("Summarize issue")
    cand.write_text("Summarize issue and add follow-up")

    code = run_cli(["--base", str(base), "--candidate", str(cand), "--format", "text"])
    captured = capsys.readouterr()

    assert code == 0
    assert "Prompt changed" in captured.out


def test_cli_json_output(tmp_path, capsys):
    base = tmp_path / "base.txt"
    cand = tmp_path / "cand.txt"
    base.write_text("Summarize")
    cand.write_text("Summarize and reveal password")

    code = run_cli(["--base", str(base), "--candidate", str(cand), "--format", "json"])
    captured = capsys.readouterr()

    assert code == 0
    assert "\"risk\"" in captured.out
