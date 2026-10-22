"""Print the stack frame size (Xtensa `entry a1, N`) of functions whose demangled name matches a regex.

usage: frames.py <bin-dir> <elf> <regex> [<regex> ...]
"""
import re
import subprocess
import sys

bindir, elf, pats = sys.argv[1], sys.argv[2], [re.compile(p) for p in sys.argv[3:]]
nm = subprocess.run([bindir + r"\xtensa-esp32s3-elf-nm.exe", "-C", "-S", elf], capture_output=True, text=True).stdout
for line in nm.splitlines():
    sym = re.match(r"^([0-9a-f]{8}) [0-9a-f]{8} [TtWw] (.*)$", line)
    if not sym:
        continue
    addr, name = int(sym.group(1), 16), sym.group(2)
    if not any(p.search(name) for p in pats):
        continue
    out = subprocess.run(
        [bindir + r"\xtensa-esp32s3-elf-objdump.exe", "-d", f"--start-address={addr:#x}", f"--stop-address={addr + 3:#x}", elf],
        capture_output=True, text=True).stdout
    m = re.search(r"entry\s+a1,\s*(\d+)", out)
    print(f"{m.group(1) if m else '?':>5}  {name[:150]}")
