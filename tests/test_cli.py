from ai_tools_lab.cli import main

def test_cli_inspect_json(capsys):
    assert main(["inspect", "Write JSON output for this task.", "--json"]) == 0
    assert '"words"' in capsys.readouterr().out

def test_cli_template_error(capsys):
    assert main(["template", "Hello {name}"]) == 2
    assert "missing template values" in capsys.readouterr().err
