# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Tests for rpmlint-codeclimate
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import io
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from rpmlint_codeclimate import parser

HERE = Path(__file__).parent.relative_to(Path.cwd())
EXAMPLE_SPEC = HERE / "example.spec"
EXAMPLE_JSON = [
    {
        'categories': [
            'Style',
        ],
        'check_name': 'unversioned-explicit-obsoletes',
        'content': {
            'body': 'The specfile contains an unversioned Obsoletes: token, which will match all\nolder, equal and newer versions of the obsoleted thing.  This may cause update\nproblems, restrict future package/provides naming, and may match something it\nwas originally not inteded to match -- make the Obsoletes versioned if\npossible.'
        },
        'description': 'Unversioned explicit obsoletes other-example-package',
        'fingerprint': 'f20db46605ba2cc06c7bffd5f91d7a09f49c0c59',
        'location': {
            'lines': {
                'begin': 36,
                'end': 36,
            },
            'path': str(EXAMPLE_SPEC),
        },
        'severity': 'minor',
        'type': 'issue',
    },
    {
        'categories': [
            'Style',
        ],
        'check_name': 'superfluous-%clean-section',
        'content': {
            'body': 'The spec section %clean should not be used any longer. RPM provides its own\nclean logic.',
        },
        'description': 'Superfluous %clean section',
        'fingerprint': '1a0180ca74582903568189cbdd62fa0cdc0859d5',
        'location': {
            'lines': {
                'begin': 54,
                'end': 54,
            },
            'path': str(EXAMPLE_SPEC),
        },
        'severity': 'major',
        'type': 'issue',
    },
    {
        'categories': [
            'Style',
        ],
        'check_name': 'no-buildroot-tag',
        'content': {
            'body': "The BuildRoot tag isn't used in your spec. It must be used in order to allow\nbuilding the package as non root on some systems. For some rpm versions (e.g.\nrpm.org >= 4.6) the BuildRoot tag is not necessary in specfiles and is ignored\nby rpmbuild; if your package is only going to be built with such rpm versions\nyou can ignore this warning.",
        },
        'description': 'No buildroot tag',
        'fingerprint': '7c2b27925803f04fcaab9c69bcee4af93b0bbbf4',
        'location': {
            'lines': {
                'begin': 1,
                'end': 1,
            },
            'path': str(EXAMPLE_SPEC),
        },
        'severity': 'minor',
        'type': 'issue',
    },
    {
        'categories': [
            'Style',
        ],
        'check_name': 'hardcoded-packager-tag',
        'content': {
            'body': "The Packager tag is hardcoded in your spec file. It should be removed, so as\nto use rebuilder's own defaults."
        },
        'description': 'Hardcoded packager tag Duncan Macleod <macleoddm@cardiff.ac.uk>',
        'fingerprint': '9bf0a84c9f1e0f84adad31639dd36de4048564f2',
        'location': {
            'lines': {
                'begin': 15,
                'end': 15,
            },
            'path': str(EXAMPLE_SPEC),
        },
        'severity': 'minor',
        'type': 'issue',
    },
]


@pytest.fixture()
@patch.object(sys, "argv", ["rpmlint", "--info", str(EXAMPLE_SPEC)])
def rpmlint_report(capsys):
    """Run rpmlint and return the output as a stream.
    """
    from rpmlint.cli import lint
    with pytest.raises(SystemExit):
        lint()
    stream = io.StringIO()
    stream.write(capsys.readouterr()[0])
    stream.seek(0)
    return stream


def test_parse(rpmlint_report):
    result = parser.parse(
        rpmlint_report,
        spec=EXAMPLE_SPEC,
    )
    # check that the expected result is a subset of what we got back
    for entry in EXAMPLE_JSON:
        assert entry in result
