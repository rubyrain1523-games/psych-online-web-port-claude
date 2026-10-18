#!/bin/bash
source /home/claude/tools/env.sh
cd /home/claude/psych/work
timeout 580 haxelib run lime build html5 -Dweb -nolaunch 2>&1 | grep -v "^\s*$\|web font\|^Called from\|Uncaught exception - Could not find lime\|Called from macro\|Warning" | awk '!seen[$0]++' | head -${1:-30}
cd export/release/html5/bin && rm -rf mods && mkdir -p mods && cp /home/claude/psych/work/example_mods/readme.txt mods/ 2>/dev/null
python3 -I /home/claude/psych/scripts/postbuild.py . ; python3 -I /home/claude/psych/scripts/make_manifest.py . >/dev/null
