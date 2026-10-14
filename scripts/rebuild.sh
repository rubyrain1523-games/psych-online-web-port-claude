#!/bin/bash
source /home/claude/tools/env.sh
cd /home/claude/psych/work
timeout 580 haxelib run lime build html5 -Dweb -nolaunch 2>&1 | grep -v "^\s*$\|web font\|^Called from\|Uncaught exception - Could not find lime\|Called from macro\|Warning" | awk '!seen[$0]++' | head -${1:-30}
cd export/release/html5/bin && mkdir -p mods && cp -rn /home/claude/psych/work/example_mods/* mods/ 2>/dev/null; cp -rn /home/claude/psych/test_mods/* mods/ 2>/dev/null
python3 -I /home/claude/psych/scripts/postbuild.py . ; python3 -I /home/claude/psych/scripts/make_manifest.py . >/dev/null
