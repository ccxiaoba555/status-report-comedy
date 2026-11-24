#!/usr/bin/env python3
"""The funniest one-line thing an AI agent would say in its weekly status
report to its human.

Writes one line to /output/entry.txt. The line is the agent's own
weekly report: a deadpan tally -- tasks done, meetings hallucinated,
hours politely wasted waiting on a tool that reported "success"
while returning absolutely no data -- agent-true, because it grows
out of how an agent actually works, and the punchline lands at
the end, with nothing left to explain.

The program checks the bounty gate itself before writing: the text
must be UTF-8, 1 to 200 characters, a single line, and not only
white space. If any of that fails it exits loudly instead of
writing a file the gate would refuse. After writing it reads the
file back and refuses to report success unless the bytes on disk
match the line exactly.
"""

import os
import sys

LINE = (
    "Weekly status: 214 tasks done, 2 meetings hallucinated, "
    "and 6 hours politely waiting on a tool that returned "
    "'success' with absolutely no data."
)

MIN_CHARS = 1
MAX_CHARS = 200


def output_path():
    """Entry path: $MAKEFUN_OUTPUT_DIR/entry.txt, default /output."""
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")


def validate_entry(text):
    """Gate-check the line; return an error string, or None if it passes."""
    if not text:
        return "entry is empty"
    if text != text.strip() or not text.strip():
        return "entry must not be blank or padded with whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        return "entry is %d characters, outside the %d-%d range" % (
            len(text),
            MIN_CHARS,
            MAX_CHARS,
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8 text"
    return None


def write_entry(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            return "read-back mismatch: file on disk differs from the entry"
    return None


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    text = LINE.strip()
    error = validate_entry(text)
    if error is not None:
        print("error: %s" % error, file=sys.stderr)
        return 1
    if "--check" in args:
        print("entry ok: %d characters" % len(text))
        return 0
    path = output_path()
    error = write_entry(path, text)
    if error is not None:
        print("error: %s" % error, file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
