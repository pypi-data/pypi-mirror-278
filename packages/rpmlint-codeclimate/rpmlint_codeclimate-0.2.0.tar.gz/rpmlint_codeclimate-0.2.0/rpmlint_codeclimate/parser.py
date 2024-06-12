# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Parser for rpmlint.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import argparse
import hashlib
import json
import os
import re
import sys
from operator import itemgetter
from pathlib import Path
from string import Template

CWD = Path(os.curdir)

ITEM_REGEX = re.compile(
    r"\A(?P<package>[\w.\/-]+):"
    r"((?P<lineno>[0-9]+):)?(\s+)?"
    r"(?P<type>[A-Z]+):(\s+)?"
    r"(?P<tag>[\w%-]+)(\s+)?"
    r"(?P<desc>.*)?"
)
SUMMARY_REGEX = re.compile(
    r"\A(\s+)?[0-9]+ packages and [0-9]+ specfiles checked"
)

SEVERITY = {
    "I": "info",
    "W": "minor",
    "E": "major",
}

# tags that should only be included once (not once per binary package)
ONESHOT_TAGS = [
    "hardcoded-packager-tag",
    "invalid-license",
    "more-than-one-%changelog-section",
    "no-buildroot-tag",
    "no-group-tag",
    "strange-permission",
]
LOCATION_PATTERN = {
    "invalid-license": "^License:",
    "invalid-url": "^Source",
    "name-repeated-in-summary": r"^Summary:.*($name|%({)?(\w+)?name)",
    "no-cleaning-of-buildroot": "$desc",
    "superfluous-%clean-section": "%clean",
}


def _get_location_spec(
    stream,
    pattern,
    default=1,
):
    """Identify a line matching a pattern.
    """
    for i, line in enumerate(stream, start=1):
        if re.search(pattern, line, re.I):
            return (i, i)
    return (default, default)


def get_location(path, lineno=None, tag=None, **kwargs):
    """Attempt to identify a codeclimate 'location' for a lint entry.
    """
    def _loc(begin, end):
        return {
            "path": str(path),
            "lines": {
                "begin": int(begin),
                "end": int(end),
            }
        }

    if lineno:
        return _loc(lineno, lineno)

    pattern = Template(LOCATION_PATTERN.get(tag, "")).safe_substitute(
        tag=tag,
        **kwargs,
    )
    if pattern:
        try:
            with open(path, "r") as file:
                return _loc(*_get_location_spec(file, pattern))
        except OSError:
            pass

    # fallback
    return _loc(1, 1)


def format_issue(params, spec):
    tag = str(params["tag"])
    package = str(params["package"])
    nicetag = tag.capitalize().replace("-", " ")
    description = f"{nicetag} {params['desc']}".strip()

    # determine source file location
    location = get_location(spec, name=package.split(".", 1)[0], **params)

    # create fingerprint (excluding package name)
    fingerprint = hashlib.sha1(
        "".join(map(str, params.values())).encode("utf-8"),
    ).hexdigest()

    # construct basic codeclimate issue
    return {
        "categories": ["Style"],
        "check_name": tag,
        "description": description,
        "fingerprint": fingerprint,
        "location": location,
        "severity": SEVERITY.get(params["type"], "info"),
        "type": "issue",
    }


def unique(issues):
    """Remove duplicate issues reported in different packages.
    """
    seen = set()
    for issue in sorted(issues, key=itemgetter("check_name")):
        check = issue["check_name"]
        if check in ONESHOT_TAGS and check in seen:
            continue
        seen.add(check)
        yield issue


def parse_stream(stream, spec):
    issues = []
    info = {}
    thisinfo = ""

    def _finalise_info():
        if issues and thisinfo:
            info[issues[-1]["check_name"]] = thisinfo.strip()

    for line in stream:
        # skip comments/headers
        if line.startswith("=#") or SUMMARY_REGEX.match(line):
            continue
        match = ITEM_REGEX.match(line)
        if match:
            # finalise the info for the previous match
            _finalise_info()
            # parse the new match
            params = match.groupdict()
            issues.append(format_issue(params, spec=spec))
            thisinfo = ""
        elif not issues:  # header line
            continue
        else:
            thisinfo += line

    # finalise the info for the final match
    _finalise_info()

    # now that we've parsed everything, update issues based on the parsed info
    for issue in issues:
        check = issue["check_name"]
        if info.get(check):
            issue["content"] = {"body": info[check]}

    return list(unique(issues))


def parse(source, *args, **kwargs):
    if isinstance(source, (str, os.PathLike)):
        with open(source, "r") as file:
            return parse(file, *args, **kwargs)

    return parse_stream(source, *args, **kwargs)


def write_json(data, target):
    if isinstance(target, (str, os.PathLike)):
        with open(target, "w") as file:
            return write_json(data, file)
    return json.dump(data, target)


def _find_spec():
    spec = list(Path.cwd().glob("*.spec*"))
    if spec:
        return spec[0]


# -- command-line interface

def create_parser():
    """Create an `argparse.ArgumentParser` for this tool.
    """
    default_spec = _find_spec()

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path of rpmlint report to parse (defaults to stdin stream)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Path in which to write output JSON report.",
    )
    parser.add_argument(
        "-s",
        "--spec",
        default=default_spec,
        required=default_spec is None,
        type=Path,
        help=(
            "Path of the spec file for this project "
            "(relative to project root)"
        ),
    )
    return parser


def main(args=None):
    parser = create_parser()
    opts = parser.parse_args(args=args)
    lint = parse(
        opts.source or sys.stdin,
        spec=opts.spec,
    )
    write_json(
        lint,
        opts.output_file or sys.stdout,
    )
