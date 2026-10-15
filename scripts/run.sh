#!/bin/bash
# usage: run.sh script args...  (ensures server is up)
cd /home/claude/psych
curl -s -o /dev/null localhost:8123/index.html || { setsid nohup python3 scripts/serve.py work/export/release/html5/bin >/dev/null 2>&1 < /dev/null & sleep 2; }
timeout 280 python3 -I "$@" 2>&1
