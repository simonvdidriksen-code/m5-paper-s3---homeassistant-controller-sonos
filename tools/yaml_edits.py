"""List (and optionally reverse) the edits made to m5paper-areas.yaml after a given time.

usage: yaml_edits.py <transcript.jsonl> <since-iso> [<yaml-in> <yaml-out>]
Lists Edit/Write/PowerShell-script changes to the YAML since <since-iso>. With
<yaml-in>/<yaml-out>, undoes the Edit calls (newest first) and writes the result.
"""
import json
import sys

path, since = sys.argv[1], sys.argv[2]
edits = []
others = []
with open(path, encoding="utf-8") as f:
    for line in f:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("type") != "assistant":
            continue
        ts = rec.get("timestamp", "")
        if ts < since:
            continue
        for c in rec.get("message", {}).get("content", []) or []:
            if c.get("type") != "tool_use":
                continue
            name, inp = c.get("name"), c.get("input", {})
            fp = inp.get("file_path", "")
            if name in ("Edit", "Write", "MultiEdit") and fp.endswith("m5paper-areas.yaml"):
                edits.append((ts, name, inp))
            elif name in ("PowerShell", "Bash") and "m5paper-areas.yaml" in inp.get("command", "") and (
                "Set-Content" in inp["command"] or "WriteAllText" in inp["command"] or "gen_" in inp["command"] or "> " in inp["command"]
            ):
                others.append((ts, name, inp.get("command", "")[:300]))

for ts, name, inp in edits:
    if name == "Edit":
        print(ts, "Edit", repr(inp.get("old_string", "")[:70]), "->", repr(inp.get("new_string", "")[:70]),
              "(all)" if inp.get("replace_all") else "")
    else:
        print(ts, name)
for ts, name, cmd in others:
    print(ts, name, "SCRIPT:", cmd.replace("\n", " ")[:200])

if len(sys.argv) > 4:
    text = open(sys.argv[3], encoding="utf-8", newline="").read()
    for ts, name, inp in reversed(edits):
        if name != "Edit":
            sys.exit(f"cannot undo {name} at {ts}")
        old, new = inp["old_string"], inp["new_string"]
        n = text.count(new)
        if n == 0:
            sys.exit(f"undo failed at {ts}: new_string not found: {new[:80]!r}")
        if inp.get("replace_all"):
            text = text.replace(new, old)
        else:
            if n > 1:
                sys.exit(f"undo ambiguous at {ts}: {n} matches")
            text = text.replace(new, old, 1)
    open(sys.argv[4], "w", encoding="utf-8", newline="").write(text)
    print("undone", len(edits), "edits ->", sys.argv[4])
