from wappy import resolve_version
import re


def test_resolve_version_ternary():
    assert "Community" == resolve_version(
        "\\1?Enterprise:Community",
        re.compile("skin/frontend/(?:default|(enterprise))", re.I),
        "/skin/frontend/default"
    )

    assert "Enterprise" == resolve_version(
        "\\1?Enterprise:Community",
        re.compile("skin/frontend/(?:default|(enterprise))", re.I),
        "/skin/frontend/enterprise"
    )


def test_resolve_version():

    assert "3.3" == resolve_version(
        "\\1",
        re.compile("([\\d.]+)?/mathjax\\.js", re.I),
        "3.3/mathjax.js"
    )
